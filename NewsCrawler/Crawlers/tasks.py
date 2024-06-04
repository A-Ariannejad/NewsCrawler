import threading
import time
import requests
import json
import requests
import xml.etree.ElementTree as ET

def parse_xml_response(xml_content):
    items = {}
    root = ET.fromstring(xml_content)
    for item in root.findall('.//item'):
        x = {}
        x['title'] = item.find('title').text
        x['pubDate'] = item.find('pubDate').text
        x['link'] = item.find('link').text
        x['id'] = str(x['link']).split("/")[-2],
        description_element = item.find('description')
        x['description'] = description_element.text if description_element is not None else ""
        items[x['id']] = x
    return items

def save_response_to_file(url, filename):
    try:
        response = requests.get(url)
        if response.status_code == 200:
            with open(filename, 'wb') as file:
                file.write(response.content)
            print("Response saved successfully to", filename)
            return response.content
        else:
            print("Error:", response.status_code)
            return None
    except requests.exceptions.RequestException as e:
        print("Error:", e)
        return None

def my_periodic_task():
    print("Running periodic task...")
    print(time.strftime("%Y-%m-%d %H:%M:%S"))

def start_periodic_task():
    print("Starting periodic task...")
    def run_periodic():
        while True:
            my_periodic_task()
            time.sleep(5)

    # Create a new thread to run the periodic task
    periodic_thread = threading.Thread(target=run_periodic)
    # Set the thread as daemon so it will exit when the main thread exits
    periodic_thread.daemon = True
    # Start the thread
    periodic_thread.start()