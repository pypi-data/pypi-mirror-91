import logging

logger = logging.getLogger("mysqltools")
logger.setLevel(logging.DEBUG)
#stream_handler = logging.StreamHandler()
handler = logging.StreamHandler()
formatter = logging.Formatter(
        '%(asctime)s - %(name)s - %(threadName)s - %(levelname)s - %(message)s')
handler.setFormatter(formatter)
logger.addHandler(handler)

sql_file_logger = logger.getChild('sqlfile')
sqlpy_http_logger = logger.getChild('sqlpy-http')
le_investor_logger = logger.getChild('le-investor')

sql_file_logger.setLevel(logging.WARNING)


