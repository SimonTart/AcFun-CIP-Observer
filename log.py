import logging

for log_name in ['proxy_info_logging', 'proxy_error_logging', 'observer_info_logging', 'observer_error_logging']:
    logging_handler = logging.FileHandler('./logs/%s.txt' % log_name)
    logging_format = logging.Formatter('%(asctime)s:%(levelname)s:%(message)s')
    logging_handler.setFormatter(logging_format)

    logger = logging.getLogger(log_name)
    logger.setLevel(logging.DEBUG)
    logger.addHandler(logging_handler)
