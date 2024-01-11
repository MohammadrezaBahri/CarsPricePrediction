import logging


# Create a logger for info messages
posts_info_logger = logging.getLogger("posts_info_logger")
posts_info_logger.setLevel(logging.INFO)

# Configure the formatter
formatter = logging.Formatter('%(asctime)s - %(levelname)s - %(message)s')

# Create a handler to write info logs to 'logs/crawl_posts_info_log.txt'
posts_info_file_handler = logging.FileHandler('logs/posts_crawler_info_log.txt')
posts_info_file_handler.setFormatter(formatter)
posts_info_logger.addHandler(posts_info_file_handler)

# Create a logger for error messages
posts_error_logger = logging.getLogger("posts_error_logger")
posts_error_logger.setLevel(logging.ERROR)

# Create a handler to write error logs to 'logs/crawl_posts_error_log.txt'
posts_error_file_handler = logging.FileHandler('logs/posts_crawler_error_log.txt')
posts_error_file_handler.setFormatter(formatter)
posts_error_logger.addHandler(posts_error_file_handler)


# tokens logger
tokens_info_logger = logging.getLogger("tokens_info_logger")
tokens_info_logger.setLevel(logging.INFO)

tokens_info_file_handler = logging.FileHandler('logs/tokens_crawler_info_log.txt')
tokens_info_file_handler.setFormatter(formatter)
tokens_info_logger.addHandler(tokens_info_file_handler)

tokens_error_logger = logging.getLogger("tokens_error_logger")
tokens_error_logger.setLevel(logging.ERROR)

tokens_error_file_handler = logging.FileHandler('logs/tokens_crawler_error_log.txt')
tokens_error_file_handler.setFormatter(formatter)
tokens_error_logger.addHandler(tokens_error_file_handler)