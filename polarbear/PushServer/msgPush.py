#!/usr/bin/env python
# Coding: utf-8
# Author: Samsepi0l

import time
import json
import requests
from polarbear.Config import configServer as configer
from polarbear.PushServer.msgProcess import MsgProcesser 
from polarbear.BotServer.logger import logger

requests.packages.urllib3.disable_warnings()

class MsgPusher(object):

    def __init__(self,original_msg={}):
        # 读取配置文件
        self.configData = configer.returnConfigData()
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
            'Content-Type': 'application/json',
        }
        self.session = requests.Session()
        self.original_msg = original_msg
        self.msgProcesser = MsgProcesser(original_msg)

    def run(self,original_message):
        try:
            self.original_msg = original_message
            msg_type = list(self.original_msg.keys())[0]
            webhookkey_url = self.webhookkey  
            push_data = self.msgProcesser.process_msg_content(self.original_msg)
            # import pdb;pdb.set_trace()
            if webhookkey_url:
                request_url = webhookkey_url
                resp = self.session.post(request_url, headers=self.headers, data=json.dumps(push_data), verify=False, allow_redirects=True, timeout=15, proxies=self.proxies)
                resp_json = json.loads(resp.text)
                if resp.status_code == 200 and resp_json['errcode'] == 0:
                    logger.info("Send [{}] Message and Mentioned @all SUCCESS...".format(msg_type))
                else:
                    logger.error("Send [{}] Message and Mentioned FAILED, response: {}".format(msg_type, resp_json))
            else:
                logger.error("Send [{}] Message and Mentioned FAILED, webhookkey_url is None".format(msg_type))


        except Exception as e:
            logger.info("Send Message request error: {}".format(e))


if __name__ == '__main__':

    msg_info = {
      "msgtype": "text",
    	"text": {
        	"content": "PolarBear-Bot v1.0.1 Class-test...",
            "mentioned_list":["@wangjinfu","@all"],
		    # "mentioned_mobile_list":["13800001111","@all"]
    	},
    }
    # msg_push = MsgPusher(msg_info)
    # msg_push.run()
 