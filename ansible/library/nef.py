# Copyright 2020 Nexenta by DDN, Inc. All rights reserved.
#
#    Licensed under the Apache License, Version 2.0 (the "License"); you may
#    not use this file except in compliance with the License. You may obtain
#    a copy of the License at
#
#         http://www.apache.org/licenses/LICENSE-2.0
#
#    Unless required by applicable law or agreed to in writing, software
#    distributed under the License is distributed on an "AS IS" BASIS, WITHOUT
#    WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied. See the
#    License for the specific language governing permissions and limitations
#    under the License.

import gettext
import json
import posixpath
import time
import requests
import six

from ansible.module_utils.basic import AnsibleModule

_ = gettext.gettext


class NefException(Exception):
    def __init__(self, data=None, **kwargs):
        defaults = {
            'name': 'NexentaError',
            'code': 'EBADMSG',
            'source': 'Ansible',
            'message': 'Unknown error'
        }
        if isinstance(data, dict):
            for key in defaults:
                if key in kwargs:
                    continue
                if key in data:
                    kwargs[key] = data[key]
                else:
                    kwargs[key] = defaults[key]
        elif isinstance(data, six.string_types):
            if 'message' not in kwargs:
                kwargs['message'] = data
        for key in defaults:
            if key not in kwargs:
                kwargs[key] = defaults[key]
        message = (_('%(message)s (source: %(source)s, '
                     'name: %(name)s, code: %(code)s)')
                   % kwargs)
        self.name = kwargs['name']
        self.code = kwargs['code']
        self.source = kwargs['source']
        self.message = message
        super(NefException, self).__init__(message)


class NefRequest(object):
    def __init__(self, proxy, method):
        self.proxy = proxy
        self.method = method
        self.log = self.proxy.log
        self.attempts = proxy.retries + 1
        self.payload = None
        self.error = None
        self.path = None
        self.time = 0
        self.data = []
        self.stat = {}
        self.hooks = {
            'response': self.hook
        }
        self.kwargs = {
            'hooks': self.hooks,
            'timeout': self.proxy.timeout
        }

    def __call__(self, path, payload=None):
        self.log('Start NEF request: %(method)s %(path)s %(payload)s',
                 {'method': self.method, 'path': path, 'payload': payload})
        self.path = path
        self.payload = payload
        for attempt in range(self.attempts):
            self.data = []
            if self.error:
                self.proxy.delay(attempt)
                self.log('Retry NEF request: %(method)s %(path)s %(payload)s '
                         '[%(attempt)s/%(attempts)s], reason: %(error)s',
                         {'method': self.method, 'path': path,
                          'payload': payload, 'attempt': attempt,
                          'attempts': self.attempts, 'error': self.error})
            try:
                response = self.request(self.method, self.path, self.payload)
            except Exception as error:
                if isinstance(error, NefException):
                    self.error = error
                else:
                    message = six.text_type(error)
                    self.error = NefException(message=message)
                continue
            self.log('Finish NEF request: %(method)s %(path)s %(payload)s, '
                     'total response time: %(time)s seconds, '
                     'total requests count: %(count)s, '
                     'requests statistics: %(stat)s, '
                     'response content: %(content)s',
                     {'method': self.method,
                      'path': self.path,
                      'payload': self.payload,
                      'time': self.time,
                      'count': sum(self.stat.values()),
                      'stat': self.stat,
                      'content': response.content})
            if response.ok and not response.content:
                if 'location' in response.headers:
                    location = response.headers['location']
                    name = posixpath.basename(location)
                    data = six.moves.urllib.parse.unquote_plus(name)
                    return data
                return None
            content = json.loads(response.content)
            if not response.ok:
                raise NefException(content)
            if isinstance(content, dict) and 'data' in content:
                return self.data
            return content
        self.log('Failed NEF request: %(method)s %(path)s '
                 '%(payload)s, request reached maximum retry '
                 'attempts: %(attempts)s, reason: %(error)s',
                 {'method': self.method, 'path': path,
                  'payload': payload, 'attempts': self.attempts,
                  'error': self.error})
        raise self.error

    def request(self, method, path, payload):
        if self.method not in ['get', 'delete', 'put', 'post']:
            message = (_('Request method %(method)s not supported')
                       % {'method': self.method})
            raise NefException(code='EINVAL', message=message)
        if not path:
            message = _('Request path is required')
            raise NefException(code='EINVAL', message=message)
        url = self.proxy.url(path)
        kwargs = dict(self.kwargs)
        if payload:
            if not isinstance(payload, dict):
                message = _('Request payload must be a dictionary')
                raise NefException(code='EINVAL', message=message)
            if method in ['get', 'delete']:
                kwargs['params'] = payload
            elif method in ['put', 'post']:
                kwargs['data'] = json.dumps(payload)
        self.log('Session request: %(method)s %(url)s %(data)s',
                 {'method': method, 'url': url, 'data': kwargs})
        return self.proxy.session.request(method, url, **kwargs)

    def hook(self, response, **kwargs):
        text = (_('session request %(method)s %(url)s %(body)s '
                  'and session response %(code)s %(content)s')
                % {'method': response.request.method,
                   'url': response.request.url,
                   'body': response.request.body,
                   'code': response.status_code,
                   'content': response.content})
        self.log('Start request hook on %(text)s', {'text': text})
        if response.status_code not in self.stat:
            self.stat[response.status_code] = 0
        self.stat[response.status_code] += 1
        self.time += response.elapsed.total_seconds()
        attempt = self.stat[response.status_code]
        if response.ok and not response.content:
            return response
        try:
            content = json.loads(response.content)
        except (TypeError, ValueError) as error:
            message = (_('Failed request hook on %(text)s: '
                         'JSON parser error: %(error)s')
                       % {'text': text, 'error': error})
            raise NefException(code='EINVAL', message=message)
        if response.ok and content is None:
            return response
        if not isinstance(content, dict):
            message = (_('Failed request hook on %(text)s: '
                         'no valid content found')
                       % {'text': text})
            raise NefException(code='EINVAL', message=message)
        if attempt > self.attempts and not response.ok:
            return response
        method = 'get'
        if response.status_code == requests.codes.unauthorized:
            if 'code' in content and content['code'] == 'ELICENSE':
                raise NefException(content)
            if not self.auth():
                raise NefException(content)
            request = response.request.copy()
            request.headers.update(self.proxy.session.headers)
            return self.proxy.session.send(request, **kwargs)
        elif response.status_code == requests.codes.server_error:
            if 'code' in content and content['code'] == 'EBUSY':
                raise NefException(content)
            return response
        elif response.status_code == requests.codes.accepted:
            path, payload = self.parse(content, 'monitor')
            if not path:
                message = (_('Failed request hook on %(text)s: '
                             'monitor path not found')
                           % {'text': text})
                raise NefException(code='ENODATA', message=message)
            self.proxy.delay(attempt)
            return self.request(method, path, payload)
        elif response.status_code == requests.codes.ok:
            if 'data' not in content or not content['data']:
                self.log('Finish request hook on %(text)s: '
                         'non-paginated content',
                         {'text': text})
                return response
            data = content['data']
            self.log('Continue request hook on %(text)s: '
                     'add %(count)s data items to response',
                     {'text': text, 'count': len(data)})
            self.data += data
            path, payload = self.parse(content, 'next')
            if not path:
                self.log('Finish request hook on %(text)s: '
                         'no next page found',
                         {'text': text})
                return response
            if self.payload:
                payload.update(self.payload)
            self.log('Continue request hook with new request '
                     '%(method)s %(path)s %(payload)s',
                     {'method': method, 'path': path,
                      'payload': payload})
            return self.request(method, path, payload)
        self.log('Finish request hook on %(text)s',
                 {'text': text})
        return response

    def auth(self):
        method = 'post'
        path = '/auth/login'
        payload = {
            'username': self.proxy.username,
            'password': self.proxy.password
        }
        self.proxy.delete_bearer()
        response = self.request(method, path, payload)
        content = json.loads(response.content)
        if 'token' in content:
            token = content['token']
            if token:
                self.proxy.update_token(token)
                return True
        return False

    @staticmethod
    def parse(content, name):
        if 'links' in content:
            links = content['links']
            if isinstance(links, list):
                for link in links:
                    if (isinstance(link, dict) and
                            'href' in link and
                            'rel' in link and
                            link['rel'] == name):
                        url = six.moves.urllib.parse.urlparse(link['href'])
                        payload = six.moves.urllib.parse.parse_qs(url.query)
                        return url.path, payload
        return None, None


class NefProxy(object):
    def __init__(self, module, conf):
        self.tokens = {}
        self.headers = {
            'Content-Type': 'application/json',
            'X-XSS-Protection': '1'
        }
        self.module = module
        self.scheme = conf['scheme']
        self.username = conf['user']
        self.password = conf['password']
        self.host = conf['host']
        self.port = conf['port']
        self.backoff_factor = conf['backoff_factor']
        self.retries = conf['retries']
        self.timeout = conf['timeout']
        self.session = requests.Session()
        self.session.verify = conf['validate_certs']
        self.session.headers.update(self.headers)
        if not self.session.verify:
            requests.packages.urllib3.disable_warnings()

    def __getattr__(self, name):
        return NefRequest(self, name)

    def delete_bearer(self):
        if 'Authorization' in self.session.headers:
            del self.session.headers['Authorization']

    def update_bearer(self, token):
        bearer = 'Bearer %s' % token
        self.session.headers['Authorization'] = bearer

    def update_token(self, token):
        self.tokens[self.host] = token
        self.update_bearer(token)

    def url(self, path):
        netloc = '%s:%d' % (self.host, self.port)
        components = (self.scheme, netloc, path, None, None)
        url = six.moves.urllib.parse.urlunsplit(components)
        return url

    def delay(self, attempt):
        if self.retries > 0:
            attempt %= self.retries
            if attempt == 0:
                attempt = self.retries
        interval = float(self.backoff_factor * (2 ** (attempt - 1)))
        time.sleep(interval)

    def log(self, fmt, opt):
        msg = fmt % opt
        self.module.log(msg)

    def err(self, msg):
        self.module.fail_json(msg=msg)


def main():
    spec = {
        'scheme': {
            'required': False,
            'type': 'str',
            'choices':  ['http', 'https'],
            'default': 'https'
        },
        'user': {
            'required': False,
            'type': 'str',
            'default': 'admin'
        },
        'password': {
            'required': True,
            'type': 'str'
        },
        'host': {
            'required': True,
            'type': 'str'
        },
        'port': {
            'required': False,
            'type': 'int',
            'default': 8443
        },
        'validate_certs': {
            'required': False,
            'type': 'bool',
            'default': False
        },
        'backoff_factor': {
            'required': False,
            'type': 'float',
            'default': 1
        },
        'retries': {
            'required': False,
            'type': 'int',
            'default': 5
        },
        'connect_timeout': {
            'required': False,
            'type': 'float',
            'default': 30
        },
        'read_timeout': {
            'required': False,
            'type': 'float',
            'default': 300
        },
        'method': {
            'required': True,
            'type': 'str',
            'choices':  ['delete', 'get', 'post', 'put']
        },
        'path': {
            'required': True,
            'type': 'str'
        },
        'payload': {
            'required': False,
            'type': 'dict',
            'default': {}
        }
    }

    module = AnsibleModule(argument_spec=spec)

    scheme = module.params.get('scheme')
    user = module.params.get('user')
    password = module.params.get('password')
    host = module.params.get('host')
    port = module.params.get('port')
    validate_certs = module.params.get('validate_certs')
    backoff_factor = module.params.get('backoff_factor')
    retries = module.params.get('retries')
    connect_timeout = module.params.get('connect_timeout')
    read_timeout = module.params.get('read_timeout')
    method = module.params.get('method')
    path = module.params.get('path')
    payload = module.params.get('payload')

    conf = {
        'scheme': scheme,
        'user': user,
        'password': password,
        'host': host,
        'port': port,
        'validate_certs': validate_certs,
        'backoff_factor': backoff_factor,
        'retries': retries,
        'timeout': (connect_timeout, read_timeout)
    }

    nef = NefProxy(module, conf)

    try:
        call = getattr(nef, method)
    except Exception as error:
        module.fail_json(msg=error)

    try:
        data = call(path, payload)
    except NefException as error:
        module.fail_json(msg=error.message)

    module.exit_json(msg='Success', changed=True, data=data)

if __name__ == "__main__":
    main()
