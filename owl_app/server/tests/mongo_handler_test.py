import unittest
import sys
import os
import logging

# SET CWD
root_path = os.path.abspath(os.path.join(os.path.dirname(__file__), ".."))
sys.path.append(root_path)

# LOGGING
log_dir = os.path.join(os.getcwd() + '\owl_app\logs')
log_name = os.path.join(log_dir, 'python_tests_logs.log')
logging.basicConfig(level=logging.INFO,
                    filename=log_name,
                    filemode='w',
                    format="%(asctime)s %(levelname)s %(message)s")
logger = logging.getLogger(__name__)

from handlers.mongo_handler import FlaskMongoHandler

class TestFlaskMongoHandler(unittest.TestCase):

    def setUp(self):
        self.test_client = FlaskMongoHandler('Players')
        logger.info("Set up for TestFlaskMongoHandler successful, beginning tests...")


    def test_flask_mongo_init(self):
        expected = 'Flask Mongo Handler; DB: Players'
        client_name = self.test_client.__str__()
        try:
            expected == client_name
            logger.info(f"Test passed: {client_name} == {expected}")
        except:
            logger.error(f"Test FAILED: {client_name} != {expected}")
        self.assertEqual(expected, client_name)


if __name__ == "__main__":
    unittest.main()


