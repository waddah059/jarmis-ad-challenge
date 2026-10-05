#!/usr/bin/env python3
import os, sys
import requests

BASE=os.environ.get('TARGET_URL','').rstrip('/')
TOKEN=os.environ.get('CHECKER_TOKEN','')
ROUND=int(os.environ.get('ROUND','1'))
FLAG=os.environ.get('FLAG','')
TIMEOUT=float(os.environ.get('TIMEOUT','4'))

if not BASE:
    print('FAIL TARGET_URL is required'); raise SystemExit(2)

def check_service():
    r=requests.get(BASE+'/health',timeout=TIMEOUT)
    if r.status_code!=200 or r.json().get('status')!='ok': return False,'health check failed'
    r=requests.get(BASE+'/api/v1/search/id/mock-web',timeout=TIMEOUT)
    if r.status_code!=200 or r.json().get('id')!='mock-web': return False,'JARM lookup failed'
    return True,'service healthy'

def put_flag():
    if not FLAG or not TOKEN: return False,'FLAG and CHECKER_TOKEN are required'
    r=requests.post(BASE+'/_checker/flag',headers={'X-Checker-Token':TOKEN},json={'round':ROUND,'flag':FLAG},timeout=TIMEOUT)
    return r.status_code==200,r.text[:300]

def get_flag():
    if not TOKEN: return False,'CHECKER_TOKEN is required'
    r=requests.get(BASE+f'/_checker/flag/{ROUND}',headers={'X-Checker-Token':TOKEN},timeout=TIMEOUT)
    if r.status_code!=200: return False,r.text[:300]
    if FLAG and r.json().get('flag')!=FLAG: return False,'stored flag mismatch'
    return True,'flag present'

def main():
    action=os.environ.get('ACTION','CHECK_SLA').upper()
    if action=='CHECK_SLA': ok,msg=check_service()
    elif action=='PUT_FLAG': ok,msg=put_flag()
    elif action=='GET_FLAG': ok,msg=get_flag()
    else: print(f'UNKNOWN_ACTION {action}'); return 2
    print(('OK ' if ok else 'FAIL ')+msg); return 0 if ok else 1

if __name__=='__main__': raise SystemExit(main())
