import requests
import hashlib
import urllib
import urllib3
import json

url = 'https://www.virustotal.com/vtapi/v2/'
api = 'c0cdfc9faae9ba0e5929d03b9f14e5707f87719f4ea7c68f046e1005060c2209'


def upload(md5):
    params = {'resource': md5, 'apikey': api}
    u = url + "file/scan/upload_url"
    file = {'file': open('1 Cyber Crime - final.pptx', 'rb')}
    response = requests.post(u, files=file, params=params)
    print(response.status_code)


upload()
