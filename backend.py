import time
import requests
import threading

url = 'https://www.virustotal.com/vtapi/v2/'
api = 'c0cdfc9faae9ba0e5929d03b9f14e5707f87719f4ea7c68f046e1005060c2209'


def upload(file):
    params = {'apikey': api}
    u = url + "file/scan"
    file = {'file': open(file, 'rb')}
    response = requests.post(u, files=file, params=params)
    return response.json()


def get_results(data):
    scan_id = data["scan_id"]
    u = url + "file/report"
    params = {'apikey': api, 'resource': scan_id}
    response = requests.get(u, params=params)

    if response.status_code == 200:
        results = response.json()
        if results['response_code'] == 1:
            return results


def execute(file):
    uploaded_data = upload(file)
    for each in range(0, 15):
        results = get_results(uploaded_data)
        print('pending....')

        if results is not None:
            return results
            break
        time.sleep(10)


if __name__ == "__main__":
    execute()
