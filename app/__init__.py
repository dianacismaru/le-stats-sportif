import logging
from logging.handlers import RotatingFileHandler
import time
import os

from flask import Flask
from app.data_ingestor import DataIngestor
from app.task_runner import ThreadPool

if not os.path.exists('results'):
    os.mkdir('results')

webserver = Flask(__name__)

webserver.logger = logging.getLogger('webserver')
webserver.logger.setLevel(logging.INFO)

formatter = logging.Formatter('%(asctime)s - %(levelname)s - %(message)s')

handler = RotatingFileHandler('webserver.log', maxBytes=100000, backupCount=5)
handler.setLevel(logging.INFO)
handler.setFormatter(formatter)
handler.converter = time.gmtime

webserver.logger.addHandler(handler)

webserver.data_ingestor = DataIngestor("./nutrition_activity_obesity_usa_subset.csv",
                                        webserver.logger)
webserver.data_ingestor.process_csv()

webserver.tasks_runner = ThreadPool(webserver.data_ingestor, webserver.logger)

webserver.logger.info("Starting to get requests...\n")

from app import routes
