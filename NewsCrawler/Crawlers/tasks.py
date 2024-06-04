import xml.etree.ElementTree as ET
import threading
import requests
import atexit
import json
import time
import os

def parse_xml_response(xml_content):
    items = {}
    root = ET.fromstring(xml_content)
    for item in root.findall('.//item'):
        x = {}
        x['title'] = item.find('title').text
        x['pubDate'] = item.find('pubDate').text
        x['link'] = item.find('link').text
        x['id'] = str(x['link']).split("/")[-2]
        description_element = item.find('description')
        if description_element is not None and description_element.text is not None:
            x['description'] = description_element.text.strip()
        else:
            x['description'] = ""
        items[x['id']] = x
    return items

def save_response_to_file(url, filename):
    try:
        response = requests.get(url)
        if response.status_code == 200:
            with open(filename, 'wb') as file:
                file.write(response.content)
            print(time.strftime("%Y-%m-%d %H:%M:%S"), "Response saved successfully to", filename)
            return response.content
        else:
            print("Error:", response.status_code)
            return None
    except requests.exceptions.RequestException as e:
        print("Error:", e)
        return None

################################################################################

def load_dict_from_file(filename):
    if os.path.exists(filename):
        with open(filename, 'r', encoding='utf-8') as file:
            return json.load(file)
    else:
        return {}

def save_dict_to_file(data, filename):
    with open(filename, 'w', encoding='utf-8') as file:
        json.dump(data, file, ensure_ascii=False, indent=4)

def update_old_dict_with_new_objects(old_dict, new_dict):
    new_objects = {}
    for key, value in new_dict.items():
        if key not in old_dict:
            old_dict[key] = value
            new_objects[key] = value
    return old_dict, new_objects

################################################################################

def start_crawling():
    print(time.strftime("%Y-%m-%d %H:%M:%S"), "start crawling ............... ✔✔✔✔✔✔✔✔✔✔✔✔")
    urls = {
        'all_news': 'https://yjc.ir/fa/rss/allnews',
        'most_all_news': 'https://yjc.ir/fa/rss/all/mostvisited',
        'first_page': 'https://yjc.ir/fa/rss/1',
        'most_first_page': 'https://yjc.ir/fa/rss/1/mostvisited',
        'election': 'https://yjc.ir/fa/rss/16',
        'most_election': 'https://yjc.ir/fa/rss/16/mostvisited',
        'international': 'https://yjc.ir/fa/rss/9',
        'most_international': 'https://yjc.ir/fa/rss/9/mostvisited',
        'sports': 'https://yjc.ir/fa/rss/8',
        'most_sports': 'https://yjc.ir/fa/rss/8/mostvisited',
        'social': 'https://yjc.ir/fa/rss/5',
        'most_social': 'https://yjc.ir/fa/rss/5/mostvisited',
        'economics': 'https://yjc.ir/fa/rss/6',
        'most_economics': 'https://yjc.ir/fa/rss/6/mostvisited',
        'arts': 'https://yjc.ir/fa/rss/4',
        'most_arts': 'https://yjc.ir/fa/rss/4/mostvisited',
        'medical': 'https://yjc.ir/fa/rss/7',
        'most_medical': 'https://yjc.ir/fa/rss/7/mostvisited'
    }

    all_items = {}

    for k, v in urls.items():
        filename = os.path.join(data_directory, f"{k}_response.xml")
        xml_content = save_response_to_file(v, filename)
        if xml_content:
            items = parse_xml_response(xml_content)
            all_items.update(items)

    all_the_news_file = os.path.join(data_directory, 'all_the_news.json')
    new_objects_file = os.path.join(data_directory, 'new_objects.json')

    old_dict = load_dict_from_file(all_the_news_file)
    new_dict = load_dict_from_file(new_objects_file)

    updated_old_dict, new_objects = update_old_dict_with_new_objects(old_dict, all_items)
    updated_new_dict, nn = update_old_dict_with_new_objects(new_dict, new_objects)

    save_dict_to_file(updated_old_dict, all_the_news_file)
    save_dict_to_file(updated_new_dict, new_objects_file)

    print(time.strftime("%Y-%m-%d %H:%M:%S"), "crawling finished ............... ✔✔✔✔✔✔✔✔✔✔✔✔")


################################################################################

lock_file = 'periodic_task.lock'
data_directory = 'Crawlers/Data'
if not os.path.exists(data_directory):
    os.makedirs(data_directory)

def start_periodic_task():
    if not os.path.exists(lock_file):
        with open(lock_file, 'w') as f:
            f.write('Task started\n')
        def run_periodic():
            while True:
                start_crawling()
                time.sleep(120)
        periodic_thread = threading.Thread(target=run_periodic)
        periodic_thread.daemon = True
        periodic_thread.start()

def remove_lock_file():
    try:
        os.remove(lock_file)
    except FileNotFoundError:
        pass

atexit.register(remove_lock_file)
