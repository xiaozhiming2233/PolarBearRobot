import os
import sys
from loguru import logger

# 尝试导入配置
try:
    import config
except ImportError:
    # 使用备用配置
    config = type('config', (object,), {
        # 日志配置
        'LOGGING_FORMAT': '{time:YYYY-MM-DD HH:mm:ss.SSS}|{level} [{file}:{function}:{line}] {message}',
        'LOGGING_ASYNC': False,
        'LOGGING_BACKTRACE': True,
        'LOGGING_DIAGNOSE': False,
        'LOGGING_STDOUT': True,
        'LOGGING_STDOUT_LEVEL': 'DEBUG',
        'LOGGING_FILE': True,
        'LOGGING_FILE_LEVEL': 'INFO',
        'LOGGING_FILE_NAME': 'log_{time:YYYY-MM-DD}.log',
        'LOGGING_FILE_ROTATION': '100 MB',
        'LOGGING_FILE_RETENTION': '180 days',
        'LOGGING_FILE_COMPRESSION': 'zip',
    })

# 打印调试信息
# print(vars(config))

_logger_config = {"handlers": []}
current_script_name = os.path.splitext(os.path.basename(sys.argv[0]))[0]
# 获取当前脚本所在目录的父目录
parent_dir = os.path.abspath(os.path.join(os.path.dirname(__file__), '..'))
log_dir = os.path.join(parent_dir, 'Log')
os.makedirs(log_dir, exist_ok=True)  # 如果 log 目录不存在，则创建它

# 设置日志文件路径
LOGGING_FILE_NAME = os.path.join(log_dir, f'{current_script_name}_log_{{time:YYYY-MM-DD}}.log')

if getattr(config, 'LOGGING_STDOUT', False):
    stdout_config = {
        "sink": sys.stdout,
        "format": config.LOGGING_FORMAT,
        "enqueue": config.LOGGING_ASYNC,
        "level": config.LOGGING_STDOUT_LEVEL,
        "backtrace": config.LOGGING_BACKTRACE,
        "diagnose": config.LOGGING_DIAGNOSE,
    }
    _logger_config['handlers'].append(stdout_config)

if getattr(config, 'LOGGING_FILE', False):
    file_config = {
        "sink":  LOGGING_FILE_NAME,
        "format": config.LOGGING_FORMAT,
        "rotation": config.LOGGING_FILE_ROTATION,
        "retention": config.LOGGING_FILE_RETENTION,
        "compression": config.LOGGING_FILE_COMPRESSION,
        "enqueue": config.LOGGING_ASYNC,
        "level": config.LOGGING_FILE_LEVEL,
        "backtrace": config.LOGGING_BACKTRACE,
        "diagnose": config.LOGGING_DIAGNOSE,
    }
    _logger_config['handlers'].append(file_config)

logger.configure(**_logger_config)