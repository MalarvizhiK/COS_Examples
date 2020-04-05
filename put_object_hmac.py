import os
import datetime
import hashlib
import hmac
import requests

# please don't store credentials directly in code
# access_key = os.environ.get('COS_HMAC_ACCESS_KEY_ID')
# secret_key = os.environ.get('COS_HMAC_SECRET_ACCESS_KEY')

access_key = '133a8a292c024941858a56e6fd3ea7a6'
secret_key = '0e1098cf470630f0eb4b7000188d7d912b6433f958c0a5fe'

# request elements
http_method = 'PUT'
host = 's3.us-south.cloud-object-storage.appdomain.cloud'
region = 'us-south'
endpoint = 'https://s3.us-south.cloud-object-storage.appdomain.cloud'
bucket = 'nfvconfigvault' # add a '/' before the bucket name to list buckets
object_key = 'BIGIP-15.0.1-0.0.11.qcow2.md5.new'
request_parameters = ''


# hashing and signing methods
def hash(key, msg):
    return hmac.new(key, msg.encode('utf-8'), hashlib.sha256).digest()

# region is a wildcard value that takes the place of the AWS region value
# as COS doen't use the same conventions for regions, this parameter can accept any string
def createSignatureKey(key, datestamp, region, service):

    keyDate = hash(('AWS4' + key).encode('utf-8'), datestamp)
    keyString = hash(keyDate, region)
    keyService = hash(keyString, service)
    keySigning = hash(keyService, 'aws4_request')
    return keySigning


# assemble the standardized request
time = datetime.datetime.utcnow()
timestamp = time.strftime('%Y%m%dT%H%M%SZ')
datestamp = time.strftime('%Y%m%d')
copy_source = '/vnfimages/BIGIP-15.0.1-0.0.11.qcow2'
standardized_resource = '/' + bucket + '/' + object_key
standardized_querystring = request_parameters
standardized_headers = 'host:' + host + '\n' + 'x-amz-date:' + timestamp + '\n' + 'x-amz-copy-source:' + copy_source + '\n' 
signed_headers = 'host;x-amz-date;x-amz-copy-source'
payload_hash = hashlib.sha256(''.encode('utf-8')).hexdigest()

standardized_request = (http_method + '\n' +
                        standardized_resource + '\n' +
                        standardized_querystring + '\n' +
                        standardized_headers + '\n' +
                        signed_headers + '\n' +
                        payload_hash).encode('utf-8')


# assemble string-to-sign
hashing_algorithm = 'AWS4-HMAC-SHA256'
credential_scope = datestamp + '/' + region + '/' + 's3' + '/' + 'aws4_request'
sts = (hashing_algorithm + '\n' +
       timestamp + '\n' +
       credential_scope + '\n' +
       hashlib.sha256(standardized_request).hexdigest())


# generate the signature
signature_key = createSignatureKey(secret_key, datestamp, region, 's3')
signature = hmac.new(signature_key,
                     (sts).encode('utf-8'),
                     hashlib.sha256).hexdigest()
print(signature)

# assemble all elements into the 'authorization' header
v4auth_header = (hashing_algorithm + ' ' +
                 'Credential=' + access_key + '/' + credential_scope + ', ' +
                 'SignedHeaders=' + signed_headers + ', ' +
                 'Signature=' + signature)

print(v4auth_header)
print(timestamp)
'''
# create and send the request
headers = {'x-amz-date': timestamp, 'Authorization': v4auth_header}
# the 'requests' package autmatically adds the required 'host' header
request_url = endpoint + standardized_resource + standardized_querystring

print(request_url)
print(headers)

print('\nSending `%s` request to IBM COS -----------------------' % http_method)
print('Request URL = ' + request_url)
request = requests.get(request_url, headers=headers)

print('\nResponse from IBM COS ----------------------------------')
print('Response code: %d\n' % request.status_code)
print(request.text)
'''

# Put a file in COS
copy_source = '/vnfimages/BIGIP-15.0.1-0.0.11.qcow2.md5'
headers = {'x-amz-date': timestamp, 'Authorization': v4auth_header, 'x-amz-copy-source': copy_source, 'host': host}
request_url = endpoint + '/nfvconfigvault/BIGIP-15.0.1-0.0.11.qcow2.md5.new'
request = requests.put(request_url, headers=headers)

print('\nResponse from IBM COS ----------------------------------')
print('Response code: %d\n' % request.status_code)
print(request.text)

