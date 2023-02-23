import json
import hashlib
import struct
import requests

# login
username = 'Service'
password = 'servicelevel'

def __getAuthPostHeader(url, varname, value):
    # get challenge from sensor
    url = url + 'getChallenge'
    requestPayload = '{ "data": { "user": "'+ username + '" } }'
    r = requests.post(url, data=requestPayload)
    chal = r.json()
    
    # parse challenge response
    realm = chal['challenge']['realm']
    nonce = chal['challenge']['nonce']
    opaque = chal['challenge']['opaque']
    hstr1 = username + ":" + realm + ":" + password
    ha1 = hashlib.sha256(hstr1.encode()).hexdigest()

    # build strings and hashes for header
    methodType = 'POST'
    hstr2 = methodType + ":" + varname
    ha2 = hashlib.sha256(hstr2.encode()).hexdigest()
    hstr3 = ha1 + ":" + nonce + ":" + ha2
    response = hashlib.sha256(hstr3.encode()).hexdigest()
    
    # build payload
    payload = {}
    payload['header'] = {}
    payload['data'] = {}

    # fill payload
    payload['header']['user'] = username
    payload['header']['realm'] = realm
    payload['header']['nonce'] = nonce
    payload['header']['response'] = response
    payload['header']['opaque'] = opaque
    payload['data'][varname] = value

    return json.dumps(payload)

    #Example
    # {
    #     "header": {
    #         "user": "Service",
    #         "realm": "SICK Sensor",
    #         "nonce": "284ba8fbb07d440a9532f751459490e6d8a35a4e9d93695e4d446d0f713451cc",
    #         "response": "c38218aa7601ad13dfb9a9ef556c7102c8a7a84ef7dc54d059e7df6a73ba509a",
    #         "opaque": "9b65dcbba17f5ad588b1220b55e3f31b2c469d5e986d3674ed2d0df2ce54a867"
    #     },
    #     "data": {
    #         "ScanDataEnable": true
    #     }
    # }

def getVariable(url, varname):
    r = requests.get(url + varname)
    return(r.json())

def postVariableAuth(url, varname, value):
    payload = __getAuthPostHeader(url, varname, value)
    b = requests.post(url + varname, data=payload)
    return(b.text)


# MAIN ------------------------
url = 'http://192.168.0.1/api/' # must end with '/'

# GET
res = getVariable(url, 'ScanDataEnable')
print(res)

# POST with Authentication
res = postVariableAuth(url, "ScanDataEnable", True)
print(res)

# GET
res = getVariable(url, "ScanDataEnable")
print(res)
# -----------------------------