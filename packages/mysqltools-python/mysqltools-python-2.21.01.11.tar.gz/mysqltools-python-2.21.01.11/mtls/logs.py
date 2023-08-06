import logging

logger = logging.getLogger("mysqltools-python")
logger.setLevel(logging.DEBUG)
handler = logging.StreamHandler()
formatter = logging.Formatter(
        '%(asctime)s - %(name)s - %(threadName)s - %(levelname)s - %(message)s')
handler.setFormatter(formatter)
logger.addHandler(handler)

sql_file_logger = logger.getChild('sqlfile')
sqlpy_http_logger = logger.getChild('sqlpy-http')
le_investor_logger = logger.getChild('le-investor')

sql_file_logger.setLevel(logging.WARNING)

# 自动向表中填充数据
auto_fill_logger = logger.getChild('auto-fill')





def set_logger_level(logger:logging.Logger,log_level:str):
    """
    logger:
        logging.Logger

    log_level:
        str
    """

    level_mapping = [('info',logging.info),('debug',logging.debug),('error',logging.error)]

    for level_name,level_value in level_mapping:
            if log_level == level_name:
                    logger.setLevel(level_name,level_value)
