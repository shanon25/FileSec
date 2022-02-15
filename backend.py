import time

import requests

url = 'https://www.virustotal.com/vtapi/v2/'
api = 'c0cdfc9faae9ba0e5929d03b9f14e5707f87719f4ea7c68f046e1005060c2209'


def upload():
    params = {'apikey': api}
    u = url + "file/scan"
    file = {'file': open('Shanon fernando - CCEH final assignment.pdf', 'rb')}
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


def execute():
    uploaded_data = upload()
    for each in range(0, 10):
        results = get_results(uploaded_data)
        print('pending....')

        if results is not None:
            print("result found", results)
            return results
            break

        time.sleep(20)


if __name__ == "__main__":
    execute()
