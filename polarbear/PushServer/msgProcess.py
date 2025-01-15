#!/usr/bin/env python
# Coding: utf-8
# Author: Samsepi0l

import time
from polarbear.Config import configServer as configer
from polarbear.BotServer.logger import logger


class MsgProcesser(object):

    def __init__(self,original_msg={}):
        self.original_msg = original_msg


    def format_originmsg_weather(self,msg_details=""):
        """
            格式化消息,确定消息类型,天气:markdown; 
        """
        try:
            if self.original_msg and isinstance(self.original_msg,dict):
                msg_info_temp = {}
                if 'tianqi' in self.original_msg:
                    msg_info_temp = {
                        "msgtype": "markdown",
                        "markdown": {
                            "content": f"""**<font color="warning">【天气预报】: 未来3日天气情况</font>**\n{msg_details}""",
                            "mentioned_list": ["@wangjinfu", "@all"],
                        },
                    }
                    return msg_info_temp 
                else:
                    logger.error(f"format_originmsg_weather error: original_msg key error")
                    return msg_info_temp                
        except Exception as e:
            logger.error(f"format_originmsg_weather error: {e}")

    def format_originmsg_news(self,msg_details=[]):
        """
            格式化消息,确定消息类型,新闻:news(图文)
        """
        try:
            if self.original_msg and isinstance(self.original_msg,dict):
                msg_info_temp = {}
                if 'xinwen' in self.original_msg:
                    msg_info_temp = {
                        "msgtype": "news",
                        "news": {
                            "articles": msg_details,
                        },
                    }
                    if msg_details:
                        return msg_info_temp
                else:
                    logger.error(f"format_originmsg_news error: original_msg key error")
                    return msg_info_temp
                
        except Exception as e:
            logger.error(f"format_origin_msg error: {e}")

    def format_originmsg_weibo(self,msg_details=""):
        """
            格式化消息,确定消息类型,微博:text
        """
        try:
            if self.original_msg and isinstance(self.original_msg,dict):
                msg_info_temp = {}
                if 'weibo' in self.original_msg:
                    msg_info_temp = {
                        "msgtype": "markdown",
                        "markdown": {
                            "content": f"""**<font color="warning">【微博热搜】: 微博热搜热点排行</font>**\n ###### 更新时间: {time.strftime("%Y-%m-%d %H:%M")}\n{msg_details}""",
                        },
                    }
                    return msg_info_temp 
                else:
                    logger.error(f"format_originmsg_weibo error: original_msg key error")
                    return msg_info_temp                
        except Exception as e:
            logger.error(f"format_originmsg_weibo error: {e}")    

    def format_originmsg_englishwords(self,msg_details=""):
        """
            格式化消息,确定消息类型,英语句子:markdown
        """
        try:
            if self.original_msg and isinstance(self.original_msg,dict):
                msg_info_temp = {}
                if 'englishwords' in self.original_msg:
                    msg_info_temp = {
                        "msgtype": "markdown",
                        "markdown": {
                            "content": f"""**<font color="warning">【每日英语】: 每日英语句子</font>**\n{msg_details}""",
                            "mentioned_list": ["@wangjinfu", "@all"],
                        },
                    }
                    return msg_info_temp 
                else:
                    logger.error(f"format_originmsg_weather error: original_msg key error")
                    return msg_info_temp                
        except Exception as e:
            logger.error(f"format_originmsg_englishwords error: {e}")

    def format_originmsg_douyinhots(self,msg_details=""):
        """
            格式化消息,确定消息类型,抖音热点:markdown
        """
        try:
            if self.original_msg and isinstance(self.original_msg,dict):
                msg_info_temp = {}
                if 'douyinhots' in self.original_msg:
                    msg_info_temp = {
                        "msgtype": "markdown",
                        "markdown": {
                            "content": f"""**<font color="warning">【抖音热搜】: 抖音热搜热点排行</font>**\n ###### 更新时间: {time.strftime("%Y-%m-%d %H:%M")}\n{msg_details}""",
                        },
                    }
                    return msg_info_temp 
                else:
                    logger.error(f"format_originmsg_douyinhots error: original_msg key error")
                    return msg_info_temp                
        except Exception as e:
            logger.error(f"format_originmsg_douyinhots error: {e}")
        
    def process_msg_content(self,origin_message={}):
        """
            处理原始消息,判断消息类型,组装content
            param:
                original_msg: 消息类型+消息内容 dict
            return:
                push_data: 消息类型+消息内容 dict
        """
        try:
            self.original_msg = origin_message
            if self.original_msg and isinstance(self.original_msg,dict):
                try:
                    if 'tianqi' in self.original_msg:
                        weather_details = ""
                        for i in self.original_msg.get('tianqi',''):
                            if i and isinstance(i,dict):
                                date = i.get('date','')
                                text_day = i.get('text_day','')
                                text_night = i.get('text_night','')
                                temp_high = i.get('high','')
                                temp_low = i.get('low','')
                                wind_speed = i.get('wind_speed','')
                                wind_scale = i.get('wind_scale','')
                                humidity = i.get('humidity','')
                                rainfall = i.get('rainfall','')
                                location = i.get('location','')
                                # 拼接每个日期的天气信息
                                weather_details += f"""
                                #### Date: <font color="info">{date}</font>                                
                                > 城市: {location}
                                > 日间: {text_day},  夜间: {text_night}
                                > 温度: {temp_low}~{temp_high}℃
                                > 风速: {wind_speed},  风力:{wind_scale}级
                                > 湿度: {humidity}
                                > 降雨量: {rainfall} mm\n"""
                        msg_info = self.format_originmsg_weather(weather_details)
                        if msg_info:
                            return msg_info

                    elif 'xinwen' in self.original_msg:
                        news_details = []
                        count = 0
                        news_list = self.original_msg.get('xinwen', '')
                        while count < 5 and news_list:
                            for i in news_list:
                                if i and isinstance(i,dict):
                                    title = i.get('title','')
                                    description = i.get('description','')
                                    url = i.get('url','')
                                    picUrl = i.get('picUrl','')
                                    # 拼接每条新闻内容
                                    new_details = {                               
                                        "title": title,
                                        "description": description,
                                        "url": url,
                                        "picurl": picUrl,
                                    }
                                    news_details.append(new_details)
                                    count += 1

                                    if count >= 6:  # 消息太多有请求限制
                                        break
                        if news_details:            
                            msg_info = self.format_originmsg_news(news_details)
                            # import pdb;pdb.set_trace()
                            if msg_info:
                                return msg_info

                    elif 'weibo' in self.original_msg:
                        weibo_details = ""
                        count = 0
                        weibohot_list = self.original_msg.get('weibo', '')
                        for i in weibohot_list:
                            if count >= 30:  # 当计数器达到30时退出循环
                                break
                            if i and isinstance(i, dict):
                                hotword = i.get('hotword', '')
                                hotwordnum = i.get('hotwordnum', '')
                                count += 1
                                weibo_details += f"""热搜词{count}: {" ".join(hotword.split())}, 热度: {" ".join(hotwordnum.split())}\n"""

                        if weibo_details:            
                            msg_info = self.format_originmsg_weibo(weibo_details)
                            # import pdb;pdb.set_trace()
                            if msg_info:
                                return msg_info
                            
                    elif 'englishwords' in self.original_msg:
                        englishwords_details = ""
                        for i in self.original_msg.get('englishwords',''):
                            if i and isinstance(i,dict):
                                content = i.get('content','')
                                note = i.get('note','')
                                date = i.get('date','')
                                englishwords_details += f"""
                                #### Date: <font color="info">{date}</font>
                                > Words: {content}
                                > Note: {note}\n"""
                        if englishwords_details:
                            msg_info = self.format_originmsg_englishwords(englishwords_details)
                            if msg_info:
                                return msg_info
                    
                    elif 'douyinhots' in self.original_msg:
                        douyinhots_details = ""
                        count = 0
                        douyinhots_list = self.original_msg.get('douyinhots', '')
                        for i in douyinhots_list:
                            if count >= 50:  # 当计数器达到50时退出循环
                                break
                            if i and isinstance(i, dict):
                                hotword = i.get('word', '')
                                hotindex = str(i.get('hotindex', ''))
                                count += 1
                                douyinhots_details += f"""热搜词{count}: {" ".join(hotword.split())}, 热度: {" ".join(hotindex.split())}\n"""
                                # import pdb;pdb.set_trace()
                        if douyinhots_details:            
                            msg_info = self.format_originmsg_douyinhots(douyinhots_details)
                            if msg_info:
                                return msg_info
                            
                    else:
                        logger.error("original_msg format key error: original_msg_keys can not recognized ")
                        return False
                except Exception as e:
                    logger.error("original_msg format error: original_msg_keys or content can not recognized: {}".format(e))
                    return False
            else:
                logger.error("original_msg value error: origin_message is not dict or is None")
                return False
        except Exception as e:
            logger.error("process_msg_content error: {}".format(e))
            return False