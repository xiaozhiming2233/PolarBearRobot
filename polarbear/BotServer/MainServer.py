#!/usr/bin/env python
# Coding: utf-8
# Author: Samsepi0l

import os
import json
import time
import schedule
from polarbear.Config import configServer as configer
from polarbear.ApiServer.pluginserver.dailyAffairs import DailyAffairs 
from polarbear.PushServer.msgPush import MsgPusher 
from polarbear.BotServer.logger import logger
from datetime import datetime



class BotMainServer(object):

    def __init__(self,debug=False):
        self.dailyAffairs = DailyAffairs()
        self.msgPush = MsgPusher()
        self.configData = configer.returnConfigData()
        self.morningPageTime = self.configData['pushtimeConfig']['morningPageTime']
        self.eveningPageTime = self.configData['pushtimeConfig']['eveningPageTime']
        self.noonPageTime = self.configData['pushtimeConfig']['noonPageTime']
        self.secWikiTime = self.configData['pushtimeConfig']['secWikiTime']
        self.weiboTime = self.configData['pushtimeConfig']['weiboTime']
        self.testTime = self.configData['pushtimeConfig']['testTime']
        self.state_file = "/app/src/task_state.json"  # 状态存储文件路径
        self.tasks_completed = self.load_task_state()  # 初始化时加载状态
        self.debug = debug

    def load_task_state(self):
        """从文件加载任务状态"""
        if os.path.exists(self.state_file):
            try:
                with open(self.state_file, 'r') as f:
                    content = f.read().strip()
                    if not content:  # 如果文件为空
                        logger.info("Task state file is empty, using default state")
                        return self.get_default_state()
                    return json.loads(content)
            except json.JSONDecodeError as e:
                logger.warning(f"Invalid JSON in task state file: {e}")
            except Exception as e:
                logger.warning(f"Failed to load task state: {e}")
        return self.get_default_state()

    def get_default_state(self):
        """返回默认的任务状态"""
        return {"morning": False, "noon": False, "evening": False}

    def save_task_state(self):
        """保存任务状态到文件"""
        try:
            # 使用原子写入，防止写入过程中出现问题
            temp_file = self.state_file + ".tmp"
            with open(temp_file, 'w') as f:
                json.dump(self.tasks_completed, f, indent=2)
            os.replace(temp_file, self.state_file)
        except Exception as e:
            logger.error(f"Failed to save task state: {e}")

        
    def pushMorningPage(self):
        logger.info("Get dailyweather and push msg_info...")
        dailyweather = self.dailyAffairs.getWeather()
        self.msgPush.run(dailyweather)
        logger.info("Push dailyweather msg_info SUCCESS...")
        time.sleep(30)
        logger.info("Get dailynews and push msg_info...")
        dailynews = self.dailyAffairs.getNews()
        self.msgPush.run(dailynews)
        logger.info("Push dailynews msg_info SUCCESS...")
        if self.debug:
            pass    
        else:
            self.tasks_completed["morning"] = True
            self.save_task_state()

    def pushNoonPage(self):
        logger.info("Get weibo affairs and push msg_info...")
        weibohot = self.dailyAffairs.getWeibo()
        self.msgPush.run(weibohot)
        logger.info("Push weibohot msg_info SUCCESS...")
        time.sleep(30)
        logger.info("Get douyinhots affairs and push msg_info...")
        douyinhots = self.dailyAffairs.getDouyinHots()
        # import pdb;pdb.set_trace()
        self.msgPush.run(douyinhots)
        logger.info("Push douyinhots msg_info SUCCESS...")
        if self.debug:
            pass
        else:
            self.tasks_completed["noon"] = True
            self.save_task_state()

    def pushEveningPage(self):
        logger.info("Get englishwords and push msg_info...")
        englishwords = self.dailyAffairs.getEnglishwords()
        # import pdb; pdb.set_trace()
        self.msgPush.run(englishwords)
        logger.info("Push englishwords msg_info SUCCESS...")
        if self.debug:
            pass
        else:
            self.tasks_completed["evening"] = True
            self.save_task_state()

    def reset_tasks(self):
        """重置任务状态并保存"""
        self.tasks_completed = {"morning": False, "noon": False, "evening": False}
        self.save_task_state()
        logger.info("Tasks have been reset for the new day")

    def run(self):
        logger.info("BotMainServer is RUNNING, start get daily affairs...")
        self.tasks_completed = {"morning": False, "noon": False, "evening": False}
        
        # 定义任务调度 - 仅工作日运行
        for task_time, task_func in [
            (self.morningPageTime, self.pushMorningPage),
            (self.noonPageTime, self.pushNoonPage),
            (self.eveningPageTime, self.pushEveningPage)
        ]:
            # 分别为每个工作日设置任务
            schedule.every().monday.at(task_time).do(task_func)
            schedule.every().tuesday.at(task_time).do(task_func)
            schedule.every().wednesday.at(task_time).do(task_func)
            schedule.every().thursday.at(task_time).do(task_func)
            schedule.every().friday.at(task_time).do(task_func)

        # 添加午夜重置任务（包括周末）
        schedule.every().day.at("00:00").do(self.reset_tasks)

        last_log_time = 0
        while True:
            now = time.time()
            current_weekday = datetime.now().weekday()
            current_time = time.strftime("%H:%M", time.localtime())
            
            if current_weekday < 5:  # 工作日
                schedule.run_pending()
                
                # 每10分钟打印一次等待消息
                if now - last_log_time >= 600:
                    next_tasks = []
                    
                    # 检查未完成的任务
                    if not self.tasks_completed["morning"]:
                        next_tasks.append(f"morning task at {self.morningPageTime}")
                    if not self.tasks_completed["noon"]:
                        next_tasks.append(f"noon task at {self.noonPageTime}")
                    if not self.tasks_completed["evening"]:
                        next_tasks.append(f"evening task at {self.eveningPageTime}")
                    
                    # 根据任务状态打印不同的日志
                    if next_tasks:
                        tasks_str = ", ".join(next_tasks)
                        logger.info(f"[Workday] Current time: {current_time}, waiting for next tasks: {tasks_str}")
                    else:
                        logger.info(f"[Workday] All tasks completed for today ({current_time}), waiting for midnight reset")
                    
                    last_log_time = now
            else:  # 周末
                schedule.run_pending()  # 仍然运行以处理午夜重置
                # 周末每小时只打印一次日志
                if now - last_log_time >= 3600:
                    weekend_day = "Saturday" if current_weekday == 5 else "Sunday"
                    logger.info(f"[Weekend - {weekend_day}] Current time: {current_time}, no tasks scheduled")
                    last_log_time = now
            
            time.sleep(120)  # 每2分钟检查一次调度

    def test_schedule_run(self):
        print("start test...")
        self.tasks_completed = {"morning": False, "noon": False, "evening": False}
        schedule.every().day.at(self.testTime).do(self.pushMorningPage)
        schedule.every().day.at(self.testTime).do(self.pushNoonPage)
        while True:
            schedule.run_pending()
            time.sleep(10)
            break

    def test_class_func_run(self):
        print("start test_class_func_run...")
        self.pushMorningPage()
        self.pushNoonPage()
        # self.pushEveningPage()

if __name__ == '__main__':
    DEBUG = False   #True False
    botMainServer = BotMainServer(debug=DEBUG)
    if DEBUG:
        botMainServer.test_class_func_run()
        # botMainServer.test_schedule_run()
    else:   
        botMainServer.run()
    # botMainServer.test_schedule_run()
    # botMainServer.test_class_func_run()
