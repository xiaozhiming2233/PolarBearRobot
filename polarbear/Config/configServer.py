import yaml
import os


def returnConfigPath():
    """
    返回配置文件夹路径
    """
    current_path = os.path.dirname(os.path.abspath(__file__))  # 获取当前文件的绝对路径
    config_path = os.path.join(current_path, 'config.yaml')  # 拼接路径
    return config_path


def returnConfigData():
    """
    返回配置文件数据（YAML格式）
    """
    config_path = returnConfigPath()
    if not os.path.exists(config_path):  # 检查文件是否存在
        raise FileNotFoundError(f"配置文件 {config_path} 不存在，请检查路径!")
    with open(config_path, mode='r', encoding='UTF-8') as f:
        config_data = yaml.load(f, Loader=yaml.Loader)
    return config_data


def returnFingerConfigData():
    """
    返回指纹配置文件数据
    :return:
    """
    current_path = returnConfigPath()
    configData = yaml.load(open(current_path + '/finger.yaml', mode='r', encoding='UTF-8'), yaml.Loader)
    return configData


def returnFeishuConfigData():
    """
    返回飞书配置文件数据
    :return:
    """
    current_path = returnConfigPath()
    configData = yaml.load(open(current_path + '/feishu.yaml', mode='r', encoding='UTF-8'), yaml.Loader)
    return configData


def saveFeishuConfigData(configData):
    """
    保存飞书配置
    :param configData:
    :return:
    """
    current_path = returnConfigPath()
    with open(current_path + '/feishu.yaml', mode='w') as file:
        yaml.dump(configData, file)


def returnUserDbPath():
    return returnConfigPath() + 'User.db'


def returnRoomDbPath():
    return returnConfigPath() + 'Room.db'


def returnGhDbPath():
    return returnConfigPath() + 'Gh.db'


def returnPointDbPath():
    return returnConfigPath() + 'Point.db' 