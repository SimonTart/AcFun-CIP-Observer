import logging

for log_name in ['proxy_info_logging', 'proxy_error_logging', 'observer_info_logging', 'observer_error_logging']:
    logging_format = logging.Formatter('%(asctime)s:%(levelname)s:%(message)s')
    logger = logging.getLogger(log_name)
    logger.setLevel(logging.INFO)
    logger.addHandler(logging.FileHandler('./logs/%s.txt' % log_name))
