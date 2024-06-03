import threading
import time
import feedparser
import json
import requests
from bs4 import BeautifulSoup

def save_feed_dict(feed_dict , category):
    with open(f"{category}.json" , "w" , encoding="utf-8") as f:
        json.dump(feed_dict , f , indent=4)

def get_news_text(url):
    response = requests.get(url)
    if response.status_code == 200:
        with open("temp.html" , "wb") as f:
            f.write(response.content)
        soup = BeautifulSoup(response.content, "html.parser")
        text_div = soup.find("div" , class_="row baznashr-body")
        if text_div:
            paragraphs = text_div.find_all("p")
            raw_text = ""
            for paragraph in paragraphs:
                raw_text += paragraph.text + "\n"
            return raw_text
        return "-"
    else:
        print(f"Failed to get Raw Text of news: {url} , status_code: {response.status_code}")
        return False
    
def parse_feed(rss_url , category):
    feed = feedparser.parse(rss_url)    
    if feed.status == 200:
            results = []
            for entry in feed.entries:
                raw_text = get_news_text(entry.link)
                if raw_text == False:
                    continue                    
                results.append({

                    "title": entry.title,
                    "category": category,
                    "pubDate": entry.published_parsed,
                    "link": entry.link,
                    "id": str(entry.link).split("/")[-2],
                    "text": raw_text
                })
            return results
    else:
        print("Failed to get RSS feed. Status code:", feed.status)
        return False
        
def start_crawing():
    feeds = [
        {"category": "all_news_mostvisited" , "url": "https://www.yjc.ir/fa/rss/all/mostvisited"},
        {"category":"all_news_latest" , "url":"https://www.yjc.ir/fa/rss/allnews"}
         ]
    
    for feed in feeds:
        try:
            feed_dict = parse_feed(feed["url"] , feed["category"])
            if feed_dict != False:
                save_feed_dict(feed_dict , feed["category"])
            else:
                print(f"error in getting feed:{feed} reason: Connection Error")
                
            print(f"got feed:{feed} successfully")
            
        except Exception as e:
            print(f"error in getting feed:{feed} with error of {e}")

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