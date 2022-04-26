from seleniumwire import webdriver
from selenium.webdriver import ActionChains
from selenium.webdriver.common.keys import Keys
import random
import math
import threading
import time
from MatrixHandler.MainMatrixHandler import MainHandlerClass
import request_api
from SettingReader import SettingReader, PathReader


class Tracker:
    PROBABILITY_THRESHOLD = 1000
    matrix = []
    matrix_available_1D = []
    videos = []
    durations = []
    proxies = []
    my_threads = []
    matrix_handler = None
    agent_busy = []

    current_agent = 0
    amount_of_agent = 0

    matrix_busy = False

    proxy_number = 0
    url_number = 0

    path_read = False

    driver_path = ""
    video_path = ""
    matrix_path = ""
    video_m_path = ""
    proxy_m_path = ""
    proxies_path = ""

    def e(self, my_proxy, url_link, duration):
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
        driver = webdriver.Firefox(seleniumwire_options=options, executable_path=self.driver_path)
        try:
            driver.set_page_load_timeout(150)
            driver.set_window_position(random.randint(0, 200), random.randint(0, 200))
            driver.set_window_size(400 + random.randint(0, 100), 400 + random.randint(0, 100))
            driver.get(str(url_link))
        except:
            print("Proxy Connection Error")
            driver.close()
            return
        else:
            time.sleep(5)
            print("Button Clicking Initiating - Clean IP: " + str(my_proxy))

            actions = ActionChains(driver)
            actions.send_keys(Keys.SPACE).perform()
            duration = int(duration)
            delta = int((random.randint(5, int(duration*3/10))))
            duration = int(duration)-delta
            time.sleep(duration)
            driver.close()

    def __init__(self):
        self.setting_read, self.driver_path, self.video_path, self.matrix_path, self.proxy_m_path, self.video_m_path, self.proxies_path = SettingReader.setting_read()

        if self.setting_read:
            print("\n------ Enter your choice ------")
            print("[1] Load Matrix From File")
            print("[2] Create New Matrix")

            g = input("Choose Option:")
            if g == "1":
                print("Load")
                self.load_from_matrix()
            elif g == "2":
                print("New")
                self.create_new_matrix()
            else:
                print("Please only enter 1 or 2!")

    def load_from_matrix(self):
        print("Loading components from save")
        # ----------------- Matrix Handling Section -----------------
        self.matrix_handler = MainHandlerClass(self.matrix_path, self.video_m_path, self.proxy_m_path, len(self.proxies), len(self.videos))
        self.matrix, self.matrix_available_1D = self.matrix_handler.get_matrix()
        print(len(self.matrix))
        print("Amount of Unused Cells: " + str(len(self.matrix_available_1D)))
        self.videos, self.durations = PathReader.url_receiver(self.video_m_path)
        # ----------------- Proxy Requesting Section -----------------
        with open(self.proxy_m_path, "r") as setting_f:
            i = 0
            print("\n-------------- Proxy List Extracting --------------")
            for line in setting_f.readlines():
                line = line.strip()
                if not line:
                    continue
                print("Proxy Item " + str(i + 1) + " -> Url: " + str(line))
                self.proxies.append(line)
                i = i + 1

        # ----------------- Initiating Main Handler -----------------
        self.main_function()

    def create_new_matrix(self):
        # ----------------- URL Retrieve Section -----------------
        print("Creating new components and saving")
        self.videos, self.durations = PathReader.url_receiver(self.video_path)
        print("Please wait..")

        # ----------------- Proxy Requesting Section -----------------
        with open(self.proxies_path, "r") as setting_f:
            i = 0
            print("\n-------------- Proxy List Extracting --------------")
            for line in setting_f.readlines():
                line = line.strip()
                if not line:
                    continue
                print("Proxy Item "+str(i+1)+" -> Url: "+str(line))
                self.proxies.append(line)
                i = i + 1

        # ----------------- Matrix Handling Section -----------------
        self.matrix_handler = MainHandlerClass(self.matrix_path, self.video_m_path, self.proxy_m_path, len(self.proxies), len(self.videos))
        self.matrix_handler.empty_matrix_creator()

        # Taking Backup of Proxy and Videos
        self.matrix_handler.write_videos_matrix(self.videos, self.durations)
        self.matrix_handler.write_proxy_matrix(self.proxies)

        # Writing and Refreshing Matrix with Only ZEROS
        self.matrix, self.matrix_available_1D = self.matrix_handler.get_matrix()

        # ----------------- Initiating Main Handler -----------------
        self.main_function()

    def threading_agent(self, agent_name, agent_id):
        while len(self.matrix_available_1D) > 0:
            if self.matrix_busy is False:
                probability = random.randint(0, 100)
                print("\nProbability: " + str(probability) + "%")
                if probability < self.PROBABILITY_THRESHOLD:
                    self.matrix_busy = True
                    print("Agent-" + str(agent_name) + " enabled.")
                    random_selected_cell = random.randint(0, len(self.matrix_available_1D))
                    i = int(self.matrix_available_1D[random_selected_cell].split("-")[0])
                    j = int(self.matrix_available_1D[random_selected_cell].split("-")[1])
                    # print(str(i) + "-" + str(j))
                    selected_proxy = self.proxies[i]
                    selected_url = self.videos[j]
                    selected_duration = self.durations[j]

                    print("Selected Proxy -> "+selected_proxy + " - Selected URL ->" + selected_url+" - Duration -> " + selected_duration)

                    self.matrix[i][j] = 1
                    # Writing and Refreshing Matrix with Only ZEROS
                    self.matrix_handler.write_matrix(self.matrix)
                    self.matrix, self.matrix_available_1D = self.matrix_handler.read_matrix()

                    print("Amount of Unused Cells: " + str(len(self.matrix_available_1D)))

                    self.matrix_busy = False
                    self.current_agent = self.current_agent+1
                    self.current_agent = self.current_agent % self.amount_of_agent

                    self.e(selected_proxy, selected_url, selected_duration)
                    time.sleep(1+4*random.random())
                else:
                    rand_time = random.randint(30, 90)
                    print("Agent-" + str(agent_id) + " disabled. Sleeping (" + str(rand_time) + " Sec)")
                    time.sleep(rand_time)
            else:
                time.sleep(1)

    def main_function(self):
        while self.amount_of_agent <= 0 or self.amount_of_agent > 50:
            g = input("\nPlease Enter Agent Number as Integer (1-[Max = 50]):")
            if g.isnumeric():
                self.amount_of_agent = int(g)
                print("You Entered: " + str(math.floor(self.amount_of_agent)))
                if 1 <= math.floor(self.amount_of_agent) <= 50:
                    print("\n-------------------------------------- Initiating --------------------------------------")
                else:
                    print("Please put integer value between (1-" + str(len(self.proxies)) + ")!!!")
            else:
                print("Please put integer value between (1-" + str(len(self.proxies)) + ")!!!")

        print("Amount of Unused Cells: " + str(len(self.matrix_available_1D)))
        if 0 < self.amount_of_agent <= 50:
            for i in range(self.amount_of_agent):
                t = threading.Thread(target=self.threading_agent, args=(str(i+1), i))
                t.start()
                self.my_threads.append(t)
        else:
            print("Amount of thread is out of range.")
            time.sleep(3)


Tracker()
