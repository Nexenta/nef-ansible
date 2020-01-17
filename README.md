# nef-ansible
NexentaStor5 API module for Ansible

**Dependencies and supported versions**
* [Python](https://www.python.org) 2.x or 3.x
* [Python](https://www.python.org) modules: [requests](https://requests.readthedocs.io) and [six](https://pypi.org/project/six)
* [Ansible](https://docs.ansible.com/) 2.x

**Install requirements for Ubuntu/Debian Linux**
```
$ sudo apt install git ansible python python-six python-requests
```

**Install requirements for MacOS**
```
$ /usr/bin/ruby -e "$(curl -fsSL https://raw.githubusercontent.com/Homebrew/install/master/install)"
$ brew install ansible
```

**Install requirements for FreeBSD**
```
# pkg install git python27 py27-ansible py27-requests py27-six
```

**Quick start**
* Clone the [nef-ansible](https://github.com/Nexenta/nef-ansible) reporsory:
```
$ git clone https://github.com/Nexenta/nef-ansible.git
```

* Change global variables:
```
$ vi nef-ansible/ansible/global.yaml
```

* Run example playbook:
```
$ ansible-playbook nef-ansible/ansible/example.yaml

PLAY [NexentaStor5 API Examples] ********************************************************************************************************************************************************

TASK [Activate License] *****************************************************************************************************************************************************************
changed: [localhost]

TASK [Check License] ********************************************************************************************************************************************************************
changed: [localhost]

TASK [List Unused Disks] ****************************************************************************************************************************************************************
changed: [localhost]

TASK [Display Unused Disks] *************************************************************************************************************************************************************
ok: [localhost] => {
    "result": {
        "changed": true, 
        "data": [
            {
                "href": "/inventory/disks/c2t0d0", 
                "logicalDevice": "c2t0d0"
            }, 
            {
                "href": "/inventory/disks/c0t5000C500214FB0CFd0", 
                "logicalDevice": "c0t5000C500214FB0CFd0"
            }
        ], 
        "failed": false, 
        "msg": "Success"
    }
}

TASK [Set Disks List] *******************************************************************************************************************************************************************
ok: [localhost] => (item={u'href': u'/inventory/disks/c2t0d0', u'logicalDevice': u'c2t0d0'})
ok: [localhost] => (item={u'href': u'/inventory/disks/c0t5000C500214FB0CFd0', u'logicalDevice': u'c0t5000C500214FB0CFd0'})

TASK [Create Pool] **********************************************************************************************************************************************************************
changed: [localhost]

TASK [Create FileSystem] ****************************************************************************************************************************************************************
changed: [localhost]

TASK [Get FileSystem Properties] ********************************************************************************************************************************************************
changed: [localhost]

TASK [Display FileSystem Properties] ****************************************************************************************************************************************************
ok: [localhost] => {
    "result": {
        "changed": true, 
        "data": {
            "aclInherit": "passthrough", 
            "aclMode": "passthrough", 
            "allowExtendedAttributes": true, 
            "bytesAvailable": 107374084096, 
            "bytesLogicalUsed": 41472, 
            "bytesReferenced": 98304, 
            "bytesSnapshotDelta": 98304, 
            "bytesUsed": 98304, 
            "bytesUsedByChildren": 0, 
            "bytesUsedByReferencedReservation": 0, 
            "bytesUsedBySelf": 98304, 
            "bytesUsedBySnapshots": 0, 
            "caseSensitivity": "mixed", 
            "checksumMode": "on", 
            "compressionMode": "lz4", 
            "compressionRatio": 1, 
            "creationTime": "2020-01-17T16:16:41.000Z", 
            "creationTxg": "14", 
            "dataCopies": 1, 
            "dedupMode": "off", 
            "delegatedToTenant": false, 
            "guid": "7999885715494156390", 
            "iopsRate": 8192, 
            "isMounted": true, 
            "links": [
                {
                    "href": "/storage/filesystems", 
                    "rel": "collection"
                }, 
                {
                    "href": "/storage/filesystems/tank%2Fnas", 
                    "rel": "self"
                }, 
                {
                    "href": "/storage/filesystems/tank%2Fnas", 
                    "method": "PUT", 
                    "rel": "action/update"
                }, 
                {
                    "href": "/storage/filesystems/tank%2Fnas", 
                    "method": "DELETE", 
                    "rel": "action/delete"
                }, 
                {
                    "href": "/storage/filesystems/tank%2Fnas/rollback", 
                    "method": "POST", 
                    "rel": "action/rollback"
                }, 
                {
                    "href": "/storage/filesystems/tank%2Fnas/userspaceUtilization", 
                    "method": "POST", 
                    "rel": "action/userspaceUtilization"
                }, 
                {
                    "href": "/storage/filesystems/tank%2Fnas/mount", 
                    "method": "POST", 
                    "rel": "action/mount"
                }, 
                {
                    "href": "/storage/filesystems/tank%2Fnas/unmount", 
                    "method": "POST", 
                    "rel": "action/unmount"
                }, 
                {
                    "href": "/storage/filesystems/tank%2Fnas/promote", 
                    "method": "POST", 
                    "rel": "action/promote"
                }, 
                {
                    "href": "/storage/filesystems/tank%2Fnas/setOwner", 
                    "method": "POST", 
                    "rel": "action/setOwner"
                }, 
                {
                    "href": "/storage/filesystems/tank%2Fnas/rename", 
                    "method": "POST", 
                    "rel": "action/rename"
                }, 
                {
                    "href": "/storage/filesystems/tank%2Fnas/resetAcl", 
                    "method": "POST", 
                    "rel": "action/resetAcl"
                }, 
                {
                    "href": "/storage/filesystems/tank%2Fnas/acl", 
                    "method": "GET", 
                    "rel": "collection/filesystemAcl"
                }, 
                {
                    "href": "/storage/filesystems/tank%2Fnas/acl", 
                    "method": "HEAD", 
                    "rel": "collection/collhead_filesystemAcl"
                }
            ], 
            "logBiasMode": "latency", 
            "mountPoint": "/tank/nas", 
            "name": "nas", 
            "nonBlockingMandatoryMode": true, 
            "originalSnapshot": "", 
            "parent": "tank", 
            "path": "tank/nas", 
            "pool": "tank", 
            "primaryCacheMode": "all", 
            "quotaSize": 107374182400, 
            "rateLimit": 1073741824, 
            "readOnly": false, 
            "recordSize": 131072, 
            "redundantMetadata": "all", 
            "referencedCompressRatio": 1, 
            "referencedQuotaSize": 0, 
            "referencedReservationSize": 0, 
            "reservationSize": 0, 
            "secondaryCache": "all", 
            "sharedOverNfs": false, 
            "sharedOverS3": false, 
            "sharedOverSmb": false, 
            "smartCompression": true, 
            "snapshotDirectory": false, 
            "syncMode": "standard", 
            "unicodeNormalizationMode": "none", 
            "updateAccessTime": false, 
            "utf8Only": false, 
            "vscan": false, 
            "writeBackCache": false, 
            "zplMetaToMetadev": "off"
        }, 
        "failed": false, 
        "msg": "Success"
    }
}

TASK [Create NFS Share] *****************************************************************************************************************************************************************
changed: [localhost]

TASK [Get NFS Share Properties] *********************************************************************************************************************************************************
changed: [localhost]

TASK [Display NFS Share Properties] *****************************************************************************************************************************************************
ok: [localhost] => {
    "result": {
        "changed": true, 
        "data": {
            "anon": "root", 
            "filesystem": "tank/nas", 
            "links": [
                {
                    "href": "/nas/nfs", 
                    "rel": "collection"
                }, 
                {
                    "href": "/nas/nfs/tank%2Fnas", 
                    "rel": "self"
                }, 
                {
                    "href": "/nas/nfs/tank%2Fnas", 
                    "method": "PUT", 
                    "rel": "action/update"
                }, 
                {
                    "href": "/nas/nfs/tank%2Fnas", 
                    "method": "DELETE", 
                    "rel": "action/delete"
                }, 
                {
                    "href": "/nas/nfs/tank%2Fnas/referrals", 
                    "method": "GET", 
                    "rel": "collection/nfs_referrals"
                }, 
                {
                    "href": "/nas/nfs/tank%2Fnas/referrals", 
                    "method": "HEAD", 
                    "rel": "collection/collhead_nfs_referrals"
                }
            ], 
            "mountPoint": "/tank/nas", 
            "nohide": false, 
            "securityContexts": [
                {
                    "securityModes": [
                        "sys"
                    ]
                }
            ], 
            "shareState": "online"
        }, 
        "failed": false, 
        "msg": "Success"
    }
}

TASK [Create SMB Share] *****************************************************************************************************************************************************************
changed: [localhost]

TASK [Get SMB Share Properties] *********************************************************************************************************************************************************
changed: [localhost]

TASK [Display SMB Share Properties] *****************************************************************************************************************************************************
ok: [localhost] => {
    "result": {
        "changed": true, 
        "data": {
            "accessBasedEnum": false, 
            "accessList": [], 
            "clientSideCaching": "manual", 
            "continuousAvailability": false, 
            "encryption": false, 
            "filesystem": "tank/nas", 
            "guestOk": true, 
            "links": [
                {
                    "href": "/nas/smb", 
                    "rel": "collection"
                }, 
                {
                    "href": "/nas/smb/tank%2Fnas", 
                    "rel": "self"
                }, 
                {
                    "href": "/nas/smb/tank%2Fnas", 
                    "method": "DELETE", 
                    "rel": "action/delete"
                }, 
                {
                    "href": "/nas/smb/tank%2Fnas", 
                    "method": "PUT", 
                    "rel": "action/update"
                }
            ], 
            "shareDescription": "", 
            "shareName": "tank_nas", 
            "shareQuotas": false, 
            "shareState": "online"
        }, 
        "failed": false, 
        "msg": "Success"
    }
}

TASK [Create Replication Service] *******************************************************************************************************************************************************
changed: [localhost]

TASK [Enable Replication Service Properties] ********************************************************************************************************************************************
changed: [localhost]

TASK [Get Replication Service Properties] ***********************************************************************************************************************************************
changed: [localhost]

TASK [Display Replication Service Properties] *******************************************************************************************************************************************
ok: [localhost] => {
    "result": {
        "changed": true, 
        "data": {
            "bytesSentTotal": 0, 
            "creationTime": "2020-01-17T16:16:49.051Z", 
            "datasetType": "filesystem", 
            "destinationDataset": "tank/nas-dst", 
            "heartbeat": true, 
            "id": "c39b36b0-3944-11ea-8c4c-6d670e826dee", 
            "isManager": true, 
            "isRunning": false, 
            "isSource": true, 
            "isSyncing": false, 
            "links": [
                {
                    "href": "/hpr/services", 
                    "rel": "collection"
                }, 
                {
                    "href": "/hpr/services/nas-service", 
                    "rel": "self"
                }, 
                {
                    "href": "/hpr/services/nas-service", 
                    "method": "PUT", 
                    "rel": "action/update"
                }, 
                {
                    "href": "/hpr/services/nas-service", 
                    "method": "DELETE", 
                    "rel": "action/delete"
                }, 
                {
                    "href": "/hpr/services/nas-service/enable", 
                    "method": "POST", 
                    "rel": "action/enable"
                }, 
                {
                    "href": "/hpr/services/nas-service/recover", 
                    "method": "POST", 
                    "rel": "action/recover"
                }, 
                {
                    "href": "/hpr/services/nas-service/disable", 
                    "method": "POST", 
                    "rel": "action/disable"
                }, 
                {
                    "href": "/hpr/services/nas-service/start", 
                    "method": "POST", 
                    "rel": "action/start"
                }, 
                {
                    "href": "/hpr/services/nas-service/stop", 
                    "method": "POST", 
                    "rel": "action/stop"
                }, 
                {
                    "href": "/hpr/services/nas-service/clear", 
                    "method": "POST", 
                    "rel": "action/clear"
                }, 
                {
                    "href": "/hpr/services/nas-service/flip", 
                    "method": "POST", 
                    "rel": "action/flip"
                }, 
                {
                    "href": "/hpr/services/nas-service/swap", 
                    "method": "POST", 
                    "rel": "action/swap"
                }, 
                {
                    "href": "/hpr/services/nas-service/recreate", 
                    "method": "POST", 
                    "rel": "action/recreate"
                }, 
                {
                    "href": "/hpr/services/nas-service/statistics", 
                    "method": "GET", 
                    "rel": "action/statistics"
                }, 
                {
                    "href": "/hpr/services/nas-service/schedules", 
                    "method": "GET", 
                    "rel": "collection/hprServiceSchedules"
                }, 
                {
                    "href": "/hpr/services/nas-service/schedules", 
                    "method": "HEAD", 
                    "rel": "collection/collhead_hprServiceSchedules"
                }, 
                {
                    "href": "/hpr/services/nas-service/snaplists", 
                    "method": "GET", 
                    "rel": "collection/hprSnaplists"
                }, 
                {
                    "href": "/hpr/services/nas-service/snaplists", 
                    "method": "HEAD", 
                    "rel": "collection/collhead_hprSnaplists"
                }, 
                {
                    "href": "/hpr/services/nas-service/snapshots", 
                    "method": "GET", 
                    "rel": "collection/hprServiceSnapshot"
                }, 
                {
                    "href": "/hpr/services/nas-service/snapshots", 
                    "method": "HEAD", 
                    "rel": "collection/collhead_hprServiceSnapshot"
                }, 
                {
                    "href": "/hpr/services/nas-service/runHistory", 
                    "method": "GET", 
                    "rel": "collection/hprServiceRunHistory"
                }, 
                {
                    "href": "/hpr/services/nas-service/runHistory", 
                    "method": "HEAD", 
                    "rel": "collection/collhead_hprServiceRunHistory"
                }
            ], 
            "managerNodes": {
                "primary": {
                    "host": "host1", 
                    "port": 8443, 
                    "proto": "https"
                }
            }, 
            "name": "nas-service", 
            "progress": 0, 
            "recursive": true, 
            "remoteNode": {
                "host": "host2", 
                "port": 8443, 
                "proto": "https"
            }, 
            "revision": 2, 
            "runHistory": [], 
            "runNumber": 0, 
            "runtime": {
                "oneOffStart": false
            }, 
            "schedules": [
                {
                    "cron": "0 * * * *", 
                    "disabled": false, 
                    "keepDestination": 168, 
                    "keepSource": 24, 
                    "scheduleId": "c39b0fa0-3944-11ea-8c4c-6d670e826dee", 
                    "scheduleName": "hourly"
                }
            ], 
            "sendShareNfs": true, 
            "sourceDataset": "tank/nas", 
            "state": "enabled", 
            "statistics": {
                "bytesRead": 0, 
                "bytesReceived": 0, 
                "bytesSent": 0, 
                "bytesWritten": 0
            }, 
            "transportOptions": {
                "maxBufferSize": 100, 
                "throttle": 209715200, 
                "usePreallocation": false
            }, 
            "type": "scheduled", 
            "zfsOptions": {
                "autoRollback": false, 
                "forceReceive": false, 
                "ignoreProperties": [
                    "mountPoint"
                ], 
                "noChecksum": false, 
                "replaceProperties": {
                    "readOnly": true
                }, 
                "sendUserSnapshots": false
            }
        }, 
        "failed": false, 
        "msg": "Success"
    }
}

PLAY RECAP ******************************************************************************************************************************************************************************
localhost                  : ok=20   changed=13   unreachable=0    failed=0   
```

**Usage**

See the source files for documentation and examples. You may also want to refer to [Nexenta Documentation](https://nexenta.com/products/documentation).
The following example shows off some of the features of NexentaStor5 API:
```
---
- name: NexentaStor5 API Examples
  gather_facts: false
  connection: local
  hosts: localhost
  
  tasks:
  - name: Set Replication Password
    nef:
      user: "{{ nef_user }}"
      password: "{{ nef_password }}"
      host: "{{ item }}"
      method: put
      path: hpr/replicationPassword
      payload:
        password: "{{ hpr_password }}"
    with_items: "{{ nef_hosts }}"
    
  - name: Create Hosts Records
    nef:
      user: "{{ nef_user }}"
      password: "{{ nef_password }}"
      host: "{{ nef_host }}"
      method: post
      path: network/hosts
      payload:
        hostname: "{{ item.key }}"
        address: "{{ item.value }}"
    when: item.value != nef_host
    with_dict: "{{ etc_hosts }}"
    
  - name: Create iSCSI Target
    nef:
      user: "{{ nef_user }}"
      password: "{{ nef_password }}"
      host: "{{ nef_host }}"
      method: post
      path: san/iscsi/targets
      payload:
        portals:
          - address: "{{ portal }}"
          
  - name: Create FileSystem
    nef:
      user: "{{ nef_user }}"
      password: "{{ nef_password }}"
      host: "{{ nef_host }}"
      method: post
      path: storage/filesystems
      payload:
        path: tank/nas
        quotaSize: 107374182400
        rateLimit: 1073741824
        
  - name: Create NFS Share
    nef:
      user: "{{ nef_user }}"
      password: "{{ nef_password }}"
      host: "{{ nef_host }}"
      method: post
      path: nas/nfs
      payload:
        filesystem: tank/nas
        anon: root
...
```
