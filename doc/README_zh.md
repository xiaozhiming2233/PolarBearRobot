## 企业微信群机器人消息推送-PolarBearRobot


- [English](./doc/README_en.md)
- [中文](./doc/README_zh.md)
---
### 0x0 说在前面
- 本项目基于python3.12开发，使用docker部署
- 本项目获取公开API接口信息，使用企业微信群机器人消息推送，实现消息通知功能
- 目前每日推送内容为天气、新闻、weibo热搜、douyin热搜，后续增加功能
- 本项目是一个开源项目，旨在帮助开发者学习和研究相关技术

### 0x1 免责声明
**本项目仅供学习、交流和研究之用，严禁用于任何非法用途。使用者应对其行为负责，作者不对因使用本项目而产生的任何直接或间接后果承担责任。**

- **合法使用**：请确保在使用本项目时遵守所在国家或地区的法律法规。
- **禁止滥用**：严禁将本项目用于任何非法活动，包括但不限于网络攻击、数据窃取、恶意软件传播等。
- **责任自负**：使用者需对自身行为负责，作者不对任何滥用行为承担责任。
---

### 0x2 使用方法
#### 技术栈
- python3.12
- docker

```
企业微信群建机器人:
记录webhookrul

构建docker镜像: 
docker build -t polarbear:1.0.1 .

配置文件填写apikey、webhookurl等信息:
PolarBear/polarbear/Config/config.yaml

启动容器，使用脚本启动docker-compose文件:
./bear_start.sh

```
---

### 0x3 项目结构
```
├── bear_start.sh
├── bear_stop.sh
├── build.py
├── doc
├── docker-compose.yml
├── Dockerfile
├── LICENSE
├── main.py
├── polarbear
│   ├── ApiServer
│   ├── BotServer
│   ├── Config
│   ├── DBServer
│   ├── __init__.py
│   ├── Log
│   ├── PushServer
│   └── __pycache__
├── README.md
├── requirements.txt
├── site-packages
│   ├── anyio...
├── task_state.json
└── test
    ├── test.py...

```
### 0x4 项目截图
- 天气：
![天气截图](./img/weather_pic.jpg)
- 新闻：
![新闻截图](./img/news_pic.jpg)
- weibo热搜：
![weibo热搜截图](./img/weibo_.pic.jpg)
- douyin热搜：
![douyin热搜截图](./img/douyin_.pic.jpg)


### 0x5 备份
```
导出项目requirements.txt:
cd polarbear && pipreqs ./ ----encoding=utf8


```
### 交流与反馈

- 如果你有任何问题或建议，欢迎通过 [Issues](https://github.com/Samsepik9/PolarBearRobot/issues) 与我联系，不定期查看消息并回复，本项目鼓励健康的交流和学习氛围。

- 如果你喜欢这个项目，请给我一颗star，谢谢你的支持！如果你特别喜欢这个项目，也可以请我喝杯咖啡👽，谢谢老板的支持！
![coffee](./img/coffee_.pic.jpg)
