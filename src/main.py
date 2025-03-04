
from flask import Flask, request, jsonify, render_template, send_file
import logging
import os
from flask_cors import CORS
import matplotlib.pyplot as plt

from dotenv import load_dotenv

from api.ApiMain import apiMain
from api.ApiLlmText import apiLlmText
from api.ApiLlmAgent import apiLlmAgent
from api.ApiControlBurn import apiControlBurn

# Initialize Flask app
app = Flask(__name__, static_folder="static", template_folder="templates")
CORS(app)  # Enables CORS for all routes

# Load environment variables
load_dotenv()

#### Logging Configuration
logging.basicConfig(
    format='%(asctime)s - %(levelname)s: %(name)s : %(message)s',
    handlers=[
        logging.StreamHandler(),  # print to console
    ],
)
#### Log Init
logger = logging.getLogger(__name__)
logger.setLevel(os.environ.get('LOGLEVEL', 'INFO').upper())

### APIs
app.register_blueprint(apiMain)
app.register_blueprint(apiLlmText)
app.register_blueprint(apiLlmAgent)
app.register_blueprint(apiControlBurn)

### Main method
def main():
    logger.info("main started .....")

    
    ### Run the app
    app.run(host ='0.0.0.0', port = 3001, debug = True)

### Invoke Main method
if __name__ == '__main__':

    # plt.figure(figsize=(20, 12))
    # plt.plot([1, 2, 3], [4, 5, 6])  # Example plot
    # plt.show()  # This must run in the main thread
    main()