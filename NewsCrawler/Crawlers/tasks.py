import xml.etree.ElementTree as ET
import threading
import requests
import atexit
import json
import time
import os
from datetime import datetime, timezone
import pytz
from khayyam import JalaliDatetime
from CustomNews.models import CustomNew

def parse_xml_response(xml_content, key):
    items = {}
    root = ET.fromstring(xml_content)
    for item in root.findall('.//item'):
        k = key
        status = 'latest'
        if key.startswith('most_'):
            status = 'most_visited'
            k = key.replace('most_', '', 1)
        x = {}
        x['category'] = k
        x['status'] = status
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
            items = parse_xml_response(xml_content, k)
            all_items.update(items)

    old_dict = load_dict_from_file(all_the_news_file)
    new_dict = load_dict_from_file(new_objects_file)

    updated_old_dict, new_objects = update_old_dict_with_new_objects(old_dict, all_items)
    updated_new_dict, nn = update_old_dict_with_new_objects(new_dict, new_objects)

    save_dict_to_file(updated_old_dict, all_the_news_file)
    save_dict_to_file(updated_new_dict, new_objects_file)

    print(time.strftime("%Y-%m-%d %H:%M:%S"), "crawling finished ............... ✔✔✔✔✔✔✔✔✔✔✔✔")

    save_to_database()


################################################################################

def clear_and_write_empty_json(file_path):
    with open(file_path, 'w') as file:
        file.write('{}')
    print(time.strftime("%Y-%m-%d %H:%M:%S"), "new objects are set to be reset ............... ✔✔✔✔✔✔✔✔✔✔✔✔")
    
        
def convert_iso_to_shamsi(iso_date_string):
    dt = datetime.strptime(iso_date_string, "%Y-%m-%dT%H:%M:%SZ")
    dt_utc = dt.replace(tzinfo=pytz.utc)
    shamsi_date = JalaliDatetime(dt_utc).strftime('%Y-%m-%d %H:%M:%S')
    return shamsi_date

def convert_to_iso8601(date_string):
    input_format = "%d %b %Y %H:%M:%S %z"
    dt = datetime.strptime(date_string, input_format)
    dt_utc = dt.astimezone(timezone.utc)
    iso8601_format = dt_utc.strftime("%Y-%m-%dT%H:%M:%SZ")
    return iso8601_format

def save_to_database():
    created_num = 0
    updated_num = 0
    new_objects_file = os.path.join(data_directory, 'new_objects.json')
    has_to_add_objects = load_dict_from_file(new_objects_file)
    for key, value in has_to_add_objects.items():
        adDate = convert_to_iso8601(value['pubDate'])
        shamsi_date = convert_iso_to_shamsi(adDate)
        user_profile, created = CustomNew.objects.update_or_create(
            yjc_id = value['id'],
            defaults={'category': value['category'], 'status': value['status'], 'title': value['title'], 'link': value['link'], 'pubDate_ad': adDate, 'pubDate_solar': shamsi_date, 'description': value['description']}
        )
        if created:
            created_num += 1
        else:
            updated_num += 1
    print(f'{created_num} objects are created')
    print(f'{updated_num} objects are updated')
    print(time.strftime("%Y-%m-%d %H:%M:%S"), "adding to database is finished ............... ✔✔✔✔✔✔✔✔✔✔✔✔")
    clear_and_write_empty_json(new_objects_file)
    

################################################################################

lock_file = 'periodic_task.lock'
data_directory = 'Crawlers/Data'
all_the_news_file = os.path.join(data_directory, 'all_the_news.json')
new_objects_file = os.path.join(data_directory, 'new_objects.json')

if not os.path.exists(data_directory):
    os.makedirs(data_directory)

def start_periodic_task():
    if not os.path.exists(lock_file):
        with open(lock_file, 'w') as f:
            f.write('Task started\n')
        def run_periodic():
            time.sleep(6000) #delay to start in the first place
            while True:
                start_crawling()
                time.sleep(300)
        
        periodic_thread = threading.Thread(target=run_periodic)
        periodic_thread.daemon = True
        periodic_thread.start()

def remove_lock_file():
    try:
        os.remove(lock_file)
    except FileNotFoundError:
        pass

atexit.register(remove_lock_file)
