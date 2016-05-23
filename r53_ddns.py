from __future__ import print_function

import os
import sys
import socket
import boto3
import requests

# Configuration environment variables
EV_IPURL = 'R53_IP_URL'
EV_R53_ZONE_ID = 'R53_ZONE_ID'
EV_R53_A_RR = 'R53_A_NAME'
EV_R53_TTL = 'R53_TTL'

# Boto configuration environment variables
# AWS_ACCESS_KEY_ID
# AWS_SECRET_ACCESS_KEY

# Exit codes
EC_NO_ZONE_ID = 10
EC_NO_A_RR = 11

IPURL_DEFAULT = 'https://ip.appspot.com'
TTL_DEFAULT = 360


def printerr(*args, **kwargs):
    print(*args, file=sys.stderr, **kwargs)


def get_ip_from_url(url):
    r = requests.get(url)
    ip = r.text
    ip = ip.strip().strip('\n')
    socket.inet_aton(ip)
    return ip


def get_change_batch(ip, name, ttl=TTL_DEFAULT):
    change_batch = {}
    chgs = []
    chg = {}
    chg['Action'] = 'UPSERT'
    rrset = {}
    rrset['Name'] = name
    rrset['Type'] = 'A'
    rrset['TTL'] = int(ttl)
    rrset['ResourceRecords'] = [ {'Value': ip} ]
    chg['ResourceRecordSet'] = rrset
    chgs.append(chg)
    change_batch['Changes'] = chgs
    return change_batch


def update_r53(zone_id, change_batch):
    client = boto3.client('route53')
    resp = client.change_resource_record_sets(
        HostedZoneId=zone_id,
        ChangeBatch=change_batch)


if __name__ == '__main__':

    if not os.environ.get(EV_R53_ZONE_ID):
        printerr("Environment variable {} is not set".format(EV_R53_ZONE_ID))
        sys.exit(EC_NO_ZONE_ID)

    if not os.environ.get(EV_R53_A_RR):
        printerr("Environment variable {} is not set".format(EV_R53_A_RR))
        sys.exit(EC_NO_A_RR)

    url = IPURL_DEFAULT
    if os.environ.get(EV_IPURL):
        url = os.environ[EV_IPURL]

    change_batch = get_change_batch(
        get_ip_from_url(url),
        os.environ[EV_R53_A_RR],
        ttl=os.environ.get(EV_R53_TTL, TTL_DEFAULT))

    print(change_batch)
    update_r53(os.environ[EV_R53_ZONE_ID], change_batch)
