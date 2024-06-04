import threading
import atexit
import time
import os

lock_file = 'periodic_task.lock'

def my_periodic_task():
    print("Running periodic task...")
    print(time.strftime("%Y-%m-%d %H:%M:%S"))

def start_periodic_task():
    if not os.path.exists(lock_file):
        with open(lock_file, 'w') as f:
            f.write('Task started\n')
        print("Starting periodic task...")
        def run_periodic():
            while True:
                my_periodic_task()
                time.sleep(5)
        periodic_thread = threading.Thread(target=run_periodic)
        periodic_thread.daemon = True
        periodic_thread.start()

def remove_lock_file():
    try:
        os.remove(lock_file)
    except FileNotFoundError:
        pass

atexit.register(remove_lock_file)
