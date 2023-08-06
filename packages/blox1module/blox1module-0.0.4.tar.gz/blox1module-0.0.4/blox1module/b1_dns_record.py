#!/usr/bin/python
# -*- coding: utf-8 -*-

DOCUMENTATION = \
    '''
---
module: dns_view_repo
short_description: Manage your repos on Github
'''

EXAMPLES = \
    '''
- name: Create a dns_view
  dns_view_repo:
    dns_view_auth_key: "..."
    name: "amit"
  register: result

- name: Delete dns_view
  dns_view_repo:
    dns_view_auth_key: "..."
    name: "Hello-World"
    state: absent
  register: result
'''

import requests
import json
api_url = 'https://env-6.test.infoblox.com/api/'


def dns_view_present(data):

    api_key = data['dns_view_auth_key']

    del data['state']
    del data['dns_view_auth_key']

    headers = {'Authorization': 'token {}'.format(api_key)}
    url = '{}{}'.format(api_url, 'ddi/v1/dns/view')
    result = requests.post(url, json.dumps(data), headers=headers)
    #print(result.json())

    if result.status_code == 201:
        return (False, True, result.json())
    if result.status_code == 200:
        return (False, True, result.json())
    if result.status_code == 422:
        return (False, False, result.json())

    # default: something went wrong

    meta = {'status': result.status_code, 'response': result.json()}
    return (True, False, meta)


def dns_view_absent(data=None):
    headers = {'Authorization': 'token {}'.format(data['dns_view_auth_key'])}
    url = '{}{}{}'.format(api_url, 'ddi/v1/', data['name'])
    #url = '{}{}'.format(api_url, 'ddi/v1/', data['name'])
    result = requests.delete(url, headers=headers)
    print(url)

    if result.status_code == 200:
        return (False, True, {'status': 'SUCCESS'})
    if result.status_code == 404:
        result = {'status': result.status_code, 'data': result.json()}
        return (False, False, result)
    else:
        result = {'status': result.status_code, 'data': result.json(), 'url': url, 'id': data['name']}
        return (True, False, result)


def dns_view_find(data=None):

    #print(data)

    headers = {'Authorization': 'token {}'.format(data['dns_view_auth_key'])}
    url = '{}{}'.format(api_url, 'ddi/v1/dns/view')
    #url = 'https://env-6.test.infoblox.com/api/ddi/v1/dns/view'
    result = requests.get(url, headers=headers)


    print(type(result))

    if result.status_code == 200:
       print(" i am BEST")

        #return (False, True, {'status': 'SUCCESS'})

       result1 = result.json()
       #print(type(result1.values()))
       print(type(result1))
       result2=json.dumps(result1)
       print(type(result2))
       #for item in result2:
       #  print(item)
       #result2 = eval(result2)
       #print(result2)
       #print(result3)


       return (False, False, result1)
    if result.status_code == 401:
       print("I am in ERROR")
       result = {'status': result.status_code, 'data': result.json()}
       #return (False, False, result)

    print(" i am BEST2")
    #meta = {'status': result.status_code, 'response': result.json()}
    #return (True, False, meta)


def dns_zone_presnet(data):

    api_key = data['dns_view_auth_key']

    del data['state']
    del data['dns_view_auth_key']
    view = data['name']
    fqdn = data['zone_name']
    internal_secondaries = data['auth_dns_server']
    #del data['name']
    #del data['zone_name']
    #del data['auth_dns_server']
    print(fqdn)
    
    
    
    
    

    headers = {'Authorization': 'token {}'.format(api_key)}
    url = '{}{}'.format(api_url, 'ddi/v1/dns/auth_zone')
    result = requests.post(url, json.dumps(data), headers=headers)
    #print(result.json())

    if result.status_code == 201:
        return (False, True, result.json())
    if result.status_code == 200:
        return (False, True, result.json())
    if result.status_code == 422:
        return (False, False, result.json())

    # default: something went wrong

    meta = {'status': result.status_code, 'response': result.json(), 'fqdn': fqdn, 'internal_secondaries': internal_secondaries}
    return (True, False, meta)
