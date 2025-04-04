import logging
# logging.basicConfig(level=logging.INFO)
# logging.basicConfig(
#     level=logging.DEBUG,
#     format='%(asctime)s - %(levelname)s - %(name)s - %(message)s'
# )

logging.basicConfig(
    filename='app.log',
    filemode='w',  # 'w' = overwrite, 'a' = append
    level=logging.INFO,
    format='%(asctime)s - %(levelname)s - %(message)s'
)
logging.debug("debug")
logging.info("info")
logging.warning("warning")
logging.error("error")
logging.critical("critical")
