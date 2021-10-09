import requests
import json
from secrets import *

domains = my_domains['domains']


# get current public ip
public_ip = ip = requests.get('https://api.ipify.org').text


# godaddy API credentials for authorization
api_key = godaddy_api_details['key']
api_secret = godaddy_api_details['secret']
req_headers = {
    "Authorization": f"sso-key {api_key}:{api_secret}",
    "accept": "application/json"
    }


def get_domain_records(domain,typ,name, header):
    url = f"https://api.godaddy.com/v1/domains/{domain}/records/{typ}/{name}"
    req = requests.get(url, headers=req_headers)
    response = req.json()
    return response


def change_record_ip(domain,typ, headers, ip):
    url = f"https://api.godaddy.com/v1/domains/{domain}/records/{typ}"
    payload = json.dumps([
        {
            "data": ip,
            "port": 1,
            "priority": 0,
            "protocol": "string",
            "service": "string",
            "name": "@",
            "ttl": 600,
            "weight": 1
        }
    ])
    headers = {
        'Authorization': f'sso-key {api_key}:{api_secret}',
        'Content-Type': 'application/json'
    }
    response = requests.request("PUT", url, headers=headers, data=payload)
    return response



for domain in domains:
    rec_data = get_domain_records(domain, "A", "@", req_headers)
    if rec_data[0]['data'] != public_ip:
        #call godaddy api to change record IP
        print("changing 'A' record")
        res = change_record_ip(domain,'A', req_headers, public_ip)
        print(res)
    else:
        print('ip is the same')


