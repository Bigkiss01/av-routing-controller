import json
import sys

def extract_mxsta(file_path):
    with open(file_path, 'r', encoding='utf-8') as f:
        har_data = json.load(f)
        
    for entry in har_data['log']['entries']:
        url = entry['request']['url']
        if 'getjson.cgi?json=mxsta' in url:
            res = entry['response']['content'].get('text', '')
            if res:
                with open('mxsta_response.json', 'w', encoding='utf-8') as out:
                    out.write(res)
                print("Successfully extracted mxsta to mxsta_response.json")
                return
    print("mxsta not found or empty")

if __name__ == '__main__':
    extract_mxsta('192.168.2.10.har')
