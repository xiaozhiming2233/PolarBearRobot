#!/usr/bin/env python
# Coding: utf-8
# Author: Samsepi0l

import time
import json
import requests
from polarbear.Config import configServer as configer
from polarbear.BotServer.logger import logger

class DailyAffairs(object):
    """
    每日新闻、天气、心灵鸡汤、微博热点、抖音热点推送
    """
    def __init__(self,configData={}):
        # 读取配置文件
        self.configData = configer.returnConfigData()
        self.apiwhyta = self.configData['dailyAffairsConfig']['apiwhyta']['url']
        self.apiweather = self.configData['dailyAffairsConfig']['apiweather']['url']
        self.apitianxing = self.configData['dailyAffairsConfig']['apitianxing']['url']
        # 动态生成代理
        proxy_config = self.configData['pushServerConfig']['proxy']
        self.webhookkey = self.configData['pushServerConfig']['webhookkey']
        # 动态生成代理
        self.proxies = {
            'http': f"http://{proxy_config['host']}:{proxy_config['port']}",
            'https': f"http://{proxy_config['host']}:{proxy_config['port']}"
        } if proxy_config['type'] in ['http','https'] else {
            'http': f"socks5://{proxy_config['host']}:{proxy_config['port']}",
            'https': f"socks5://{proxy_config['host']}:{proxy_config['port']}"
        } 
        self.headers = {
            'User-Agent': 'Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/537.21 (KHTML, like Gecko) Chrome/41.0.2228.0 Safari/537.21',
            'Accept': '*/*',
            'Connection': 'keep-alive',
        }
        requests.packages.urllib3.disable_warnings()
        self.session = requests.Session()        

    def getNews(self):
        """
        获取每日新闻
        param:
        return: news_dict
        """
        try:
            news_lists = []
            news_dict = {'xinwen': news_lists}
            newsurl = self.apiwhyta + '/guonei' + '?key=' + self.configData['dailyAffairsConfig']['apiwhyta']['skey'] + '&num=' + self.configData['dailyAffairsConfig']['apiwhyta']['news']['num']
            resp = self.session.get(url=newsurl, headers=self.headers, proxies=self.proxies, verify=False, allow_redirects=True, timeout=15)
            resp_json = json.loads(resp.text)
            if resp.status_code == 200 and resp_json['msg'] == 'success':
                if resp_json['result']['newslist']:
                    for i in resp_json.get('result','').get('newslist',''):
                        news_lists.append(i)
                    if news_dict:
                        return news_dict
                else:
                    logger.error("getNews api failed, News result is empty...")
                    return news_dict
            
            else:
                logger.error("getNews api failed, status_code: {} and response: {}".format(resp.status_code, resp.text))

        except Exception as e:
            logger.error("getNews api failed, error: {}".format(e))

    def getWeather(self):
        """
        获取近3日天气
        param:
        return: weathers_dict
        """
        try:
            weather_lists = []
            weathers_dict = {'tianqi': weather_lists}
            weatherurl = self.apiweather + '?key=' + self.configData['dailyAffairsConfig']['apiweather']['skey'] + '&location=' + self.configData['dailyAffairsConfig']['apiweather']['location'] + '&language=zh-Hans&unit=c'
            resp = self.session.get(url=weatherurl, headers=self.headers, proxies=self.proxies, verify=False, allow_redirects=True, timeout=15)
            resp_json = json.loads(resp.text)
            if resp.status_code == 200 and resp_json.get('results','') :
                for i in resp_json.get('results',''):
                    if i.get('location','') and i.get('daily'):
                        location = i.get('location','').get('name','')
                        weather_tmp = i.get('daily','')
                        # import pdb;pdb.set_trace()
                        for j in weather_tmp:
                            j['location'] = location
                        if weather_tmp:
                            for i in weather_tmp:
                                weather_lists.append(i)
                            if weathers_dict:
                                return weathers_dict
                        else:
                            logger.error("getWeather api failed, weather_tmp is empty...")
                            return weathers_dict
                else:
                    logger.error("getWeather api failed, weathers result is empty...")
                    return weathers_dict
            else:
                logger.error("getWeather api failed, status_code: {} and response: {}".format(resp.status_code, resp.text))

        except Exception as e:
            logger.error("getWeather api failed, error: {}".format(e))

    def getWeibo(self):
        """
        获取微博热搜
        param:
        return: newslist[{},{}]
        """
        try:
            weibos_lists = []
            weibos_dict = {'weibo': weibos_lists}
            weibourl = self.apiwhyta + '/weibohot' + '?key=' + self.configData['dailyAffairsConfig']['apiwhyta']['skey']
            resp = self.session.get(url=weibourl, headers=self.headers, proxies=self.proxies, verify=False, allow_redirects=True, timeout=15)
            resp_json = json.loads(resp.text)
            if resp.status_code == 200 and resp_json['msg'] == 'success':
                if resp_json['result']['list']:
                    for i in resp_json.get('result','').get('list',''):
                        weibos_lists.append(i)
                    if weibos_dict:
                        return weibos_dict
                else:
                    logger.error("getWeibo api failed, WeiboHot result is empty...")
                    return weibos_dict
            
            else:
                logger.error("getWeibo api failed, status_code: {} and response: {}".format(resp.status_code, resp.text))

        except Exception as e:
            logger.error("getWeibo api failed, error: {}".format(e))
        
    def getEnglishwords(self):
        """
        获取英语句子
        """
        try:
            englishwords_lists = []
            englishwords_dict = {'englishwords': englishwords_lists}
            englishwordsurl = self.apiwhyta + '/everyday' + '?key=' + self.configData['dailyAffairsConfig']['apiwhyta']['skey']
            resp = self.session.get(url=englishwordsurl, headers=self.headers, proxies=self.proxies, verify=False, allow_redirects=True, timeout=15)
            resp_json = json.loads(resp.text)
            if resp.status_code == 200 and resp_json['msg'] == 'success':
                if resp_json['result']['content'] and resp_json['result']['note']:
                    englishword_tmp = {
                        'content': resp_json['result']['content'],
                        'note': resp_json['result']['note'],
                        'date': resp_json['result']['date']
                    }
                    englishwords_lists.append(englishword_tmp)
                    if englishwords_dict:
                        return englishwords_dict
                else:
                    logger.error("getEnglishwords api failed, Englishwords result is empty...")
                    return englishwords_dict
            else:
                logger.error("getEnglishwords api failed, status_code: {} and response: {}".format(resp.status_code, resp.text))
        except Exception as e:
            logger.error("getEnglishwords api failed, error: {}".format(e))

    def getDouyinHots(self):
        """
        获取抖音热点
        """
        try:
            douyinhots_lists = []
            douyinhots_dict = {'douyinhots': douyinhots_lists}
            douyinhotsurl = self.apitianxing + '/douyinhot/index' + '?key=' + self.configData['dailyAffairsConfig']['apitianxing']['skey']
            resp = self.session.get(url=douyinhotsurl, headers=self.headers, proxies=self.proxies, verify=False, allow_redirects=True, timeout=15)
            resp_json = json.loads(resp.text)
            # import pdb;pdb.set_trace()
            if resp.status_code == 200 and resp_json['msg'] == 'success':
                if resp_json['result']['list']:
                    # print("douyinhots_len: {}".format(len(resp_json.get('result','').get('list',''))))
                    for i in resp_json.get('result','').get('list',''):
                        douyinhots_lists.append(i)
                    if douyinhots_dict:
                        return douyinhots_dict
                else:
                    logger.error("getDouyinHots api failed, DouyinHots result is empty...")
                    return douyinhots_dict
            else:
                logger.error("getDouyinHots api failed, status_code: {} and response: {}".format(resp.status_code, resp.text))
        except Exception as e:
            logger.error("getDouyinHots api failed, error: {}".format(e))


    def run(self):
        pass

if __name__ == '__main__':
    dailyAffairs = DailyAffairs()
    print(dailyAffairs.getNews())
    print(dailyAffairs.getWeather()) 
    # print(dailyAffairs.getWeibo())
    # print(dailyAffairs.getEnglishwords()) 
    # print(dailyAffairs.getDouyinHots())