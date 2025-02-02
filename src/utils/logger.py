import logging
import yaml
import os
from datetime import datetime

def setup_logger():
    # 日志系统配置
    # 设置日志格式、级别和输出
    with open("config/config.yaml", "r", encoding="utf-8") as f:
        config = yaml.safe_load(f)
    
    log_config = config["logging"]
    
    if not os.path.exists("logs"):
        os.makedirs("logs")
        
    logging.basicConfig(
        level=getattr(logging, log_config["level"]),
        format=log_config["format"],
        handlers=[
            logging.FileHandler(log_config["file"]),
            logging.StreamHandler()
        ]
    )
    
    return logging.getLogger("ScooterController") 