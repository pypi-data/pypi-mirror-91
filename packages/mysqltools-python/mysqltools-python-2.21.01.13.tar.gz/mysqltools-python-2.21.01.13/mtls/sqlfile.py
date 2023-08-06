"""
实现一些处理 SQL 文件的小工具
"""

import os
import sys
from .logs import sql_file_logger

logger = sql_file_logger

"""
def every_n(file_path:str,sleep_time:float,batch_size:int)->[]:
    result = []
    if os.path.isfile(file_path) != True:
"""