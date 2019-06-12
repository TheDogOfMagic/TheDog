import time
from multiprocessing import Process
from api import app
from getter import Getter
from tester import Tester
from db import RedisClient
from setting import *
import requests
import os
import sys
dir = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
sys.path.insert(0, dir)

class Scheduler():
    def schedule_tester(self, cycle=TESTER_CYCLE):
        """
        定时测试代理
        """
        tester = Tester()
        while TESTER_ENABLED:
            print('测试器开始运行')
            tester.run()
            time.sleep(cycle)
    
    def schedule_getter(self, cycle=GETTER_CYCLE):
        """
        定时获取代理
        """
        getter = Getter()
        while GETTER_ENABLED:
            print('抓取器开始运行')
            getter.run()
            time.sleep(cycle)
    
    def schedule_api(self):
        """
        开启API
        """
        app.run(host = API_HOST, port = API_PORT)
    
    

    def run(self):
        print('代理池开始运行')
        
        if TESTER_ENABLED:
            tester_process = Process(target=self.schedule_tester)
            tester_process.start()
        
        if GETTER_ENABLED:
            getter_process = Process(target=self.schedule_getter)
            getter_process.start()
        
        if API_ENABLED:
            api_process = Process(target=self.schedule_api)
            api_process.start()

        url = 'http://localhost:'+str(API_PORT)+'/getexit'
        time.sleep(10)
        while True:
            response = requests.get(url = url)
            if 'False' in response.text:
                print('关闭代理池！')
                if TESTER_ENABLED:
                    tester_process.terminate()
                if GETTER_ENABLED:
                    getter_process.terminate()
                if API_ENABLED:
                    api_process.terminate()
                break
            time.sleep(2)
            
            


if __name__ == "__main__":
    scheduler = Scheduler()
    scheduler.run()