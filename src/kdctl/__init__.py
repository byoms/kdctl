import logging

app_logger = logging.getLogger('kdctl')
app_logger.setLevel(logging.DEBUG)

console_handler = logging.StreamHandler()

log_format = logging.Formatter(
    fmt = "{asctime} - {levelname} - {filename}:{lineno} - {message}",
    style = "{",
    datefmt = "%Y-%m-%d %H:%M"
)

console_handler.setFormatter(log_format)

if not app_logger.handlers:
    app_logger.addHandler(console_handler)
