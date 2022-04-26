from selenium import webdriver
import time
import math
from selenium.webdriver import ActionChains, DesiredCapabilities
from selenium.webdriver.common.keys import Keys
import tkinter as tk
from tkinter import filedialog
import os
import threading
import request_api
import random


root = tk.Tk()
root.withdraw()

driver_path = ""
video_file_path = ""
setting_file_path = ""

# url_driver = "C:/Users/Omer/Desktop/Proxy/Drivers/geckodriver.exe"
# p_file = "C:/Users/Omer/Desktop/Proxy/Proxies/proxies

urls = []
proxies = []
durations = []
time_counter = 0


def e(my_proxy, url_link, thread_index, duration):
    options = {
        'proxy': {
            'http': my_proxy,
            'https': my_proxy,
            'no_proxy': 'localhost,127.0.0.1'
        }
    }
    # profile = webdriver.FirefoxProfile()
    # profile.set_preference("browser.cache.disk.enable", False)
    # profile.set_preference("browser.cache.memory.enable", False)
    # profile.set_preference("browser.cache.offline.enable", False)
    # profile.set_preference("network.http.use-cache", False)
    #
    # driver = webdriver.Firefox(firefox_profile=profile, seleniumwire_options=options, executable_path=driver_path)
    caps = DesiredCapabilities.FIREFOX.copy()
    caps['marionette'] = False
    driver = webdriver.Firefox(executable_path=driver_path, capabilities=caps)
    try:
        driver.set_page_load_timeout(150)
        driver.set_window_position(random.randint(0,200), random.randint(0,200))
        driver.set_window_size(400+random.randint(0,100), 400+random.randint(0,100))
        driver.get(str(url_link))
    except:
        print("Proxy Connection Error")
        driver.close()
    else:
        time.sleep(5)
        print("Button Clicking Initiating - Clean IP: " + str(my_proxy))

        actions = ActionChains(driver)
        actions.send_keys(Keys.SPACE).perform()

        time.sleep(duration)
        driver.close()


def main_function():
    # total_proxy_number = 118
    total_proxy_number = len(proxies)

    print("\nProxy File Readed")
    print("Number of Proxies: " + str(total_proxy_number))

    amount_in_one_loop = 0

    while math.floor(amount_in_one_loop) < 1 or math.floor(amount_in_one_loop) > total_proxy_number:
        g = input("\nPlease Enter Window Number as Integer (1-" + str(total_proxy_number) + "):")
        if g.isnumeric():
            amount_in_one_loop = int(g)
            print("You Entered: " + str(math.floor(amount_in_one_loop)))
            if 1 <= math.floor(amount_in_one_loop) <= total_proxy_number:
                print("\n-------------------------------------- Initiating --------------------------------------")
            else:
                print("Please put integer value between (1-" + str(len(proxies)) + ")!!!")
        else:
            print("Please put integer value between (1-" + str(len(proxies)) + ")!!!")

    if 1 <= math.floor(amount_in_one_loop) <= total_proxy_number:
        number_loop_constant = math.floor(total_proxy_number / amount_in_one_loop)
        remaining = total_proxy_number % amount_in_one_loop
        total_tracker = total_proxy_number
        print("Main Thread Starts - Remaining: " + str(total_tracker))
        print("--------------------------------------\n")
        for i in range(number_loop_constant):
            current_url = 0
            total_tracker = total_tracker - amount_in_one_loop
            print("Loop " + str(i + 1) + " # Item in This Group: " + str(amount_in_one_loop) + " - Remaining: " + str(
                total_tracker) + "\n")
            for url in urls:
                print("----------------- NEW URL[" + str(current_url + 1) + "] -----------------")
                my_threads = []
                for j in range(amount_in_one_loop):
                    current_index = i * amount_in_one_loop + j
                    print("Item: " + str(current_index + 1) + " | Proxy: " + proxies[
                        current_index] + " | Duration: " + str(
                        durations[current_url]) + " Url " + str(current_url + 1) + ": " + url)
                    t = threading.Thread(target=e,
                                         args=(proxies[current_index], url, current_url, durations[current_url]))
                    t.start()
                    my_threads.append(t)
                current_url = current_url + 1
                for t in my_threads:
                    t.join()
                time.sleep(1)
            print("--------------------------------------\n")
        if remaining > 0:
            print(
                "Loop " + str(number_loop_constant + 1) + " # Item in This Group: " + str(
                    remaining) + " - Remaining: 0\n")
            current_url = 0
            for url in urls:
                print("----------------- NEW URL[" + str(current_url + 1) + "] -----------------")
                my_threads = []
                for t in range(remaining):
                    current_index = number_loop_constant * amount_in_one_loop + t
                    print(
                        "Item: " + str(current_index + 1) + " | Proxy: " + proxies[current_index] + " Duration: " + str(
                            durations[current_url]) + " Url " + str(current_url + 1) + ": " + url)
                    t = threading.Thread(target=e,
                                         args=(proxies[current_index], url, current_url, int(durations[current_url])))
                    t.start()
                    my_threads.append(t)
                current_url = current_url + 1
                for t in my_threads:
                    t.join()
                time.sleep(1)
            print("--------------------------------------\n")


def starter():
    print("Time-passed: "+str(time_counter)+" sec")


print("\nPlease Select Info File Location:")
setting_file = filedialog.askopenfilename(title="Setting File", filetypes=[('Txt File Only', '.txt')])

if setting_file != "":
    print("Selected File: "+str(setting_file))

    with open(setting_file, "r") as setting_f:
        for line in setting_f.readlines():
            line = line.strip()
            if not line:
                continue
            if line.split("=")[0] == "driver":
                print("\nDriver Path: "+line.split("=")[1])
                driver_path = line.split("=")[1]
            elif line.split("=")[0] == "videos":
                print("Videos File Path: "+line.split("=")[1])
                video_file_path = line.split("=")[1]

    if video_file_path != "" and driver_path != "":
        print("\nFiles' existence checking...")
        if os.path.exists(video_file_path) and os.path.exists(driver_path):
            print("Files exist. Proceeding url checking.\n")

            proxies = request_api.starter()
            for proxy in proxies:
                print("Proxy -> "+str(proxy))

            with open(video_file_path, "r") as fd:
                print("\nVideo list:")
                for line in fd.readlines():
                    line = line.strip()
                    if not line:
                        continue
                    print('Videos -> Url: '+str(line.split(" ")[0])+" Duration: "+str(line.split(" ")[1]))
                    urls.append(str(line.split(" ")[0]))
                    durations.append(int(line.split(" ")[1]))

            if len(proxies)>0 and len(urls)>0:
                print("-------------------------------------- Setting Completed --------------------------------------")
                main_function()

        else:
            print("Files don't exist. Please make sure that you set all files' path in setting file."
                  "(driver= , proxies= , videos= )")
    else:
        print("\nPlease make sure that you set all files' path in setting file.(driver= , proxies= , videos= )")
        time.sleep(5)
else:
    print("You haven't selected info file.")
    time.sleep(3)
