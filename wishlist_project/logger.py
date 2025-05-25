import logging
import sys

# 1) Define a formatter
formatter = logging.Formatter(
    fmt="%(asctime)s %(levelname)-8s [%(name)s]: %(message)s",
    datefmt="%Y-%m-%d %H:%M:%S",
)

# 2) Create a console handler
console_handler = logging.StreamHandler(sys.stdout)
console_handler.setLevel(logging.INFO)
console_handler.setFormatter(formatter)

# 3) Get the root logger and attach the handler
logging.root.setLevel(logging.INFO)
logging.root.addHandler(console_handler)

# 4) Optionally: create convenience wrappers
def get_logger(name: str):
    return logging.getLogger(name)