from flask import Blueprint, request, render_template
import logging, os

from agb.AgbMain import AgbMain

apiMain = Blueprint('api_main', __name__)

logger = logging.getLogger(__name__)
logger.setLevel(os.environ.get('LOGLEVEL', 'INFO').upper())

@apiMain.route('/')
def index():
    logger.info("main index page")
    return render_template('index.html')

@apiMain.route('/hello')
def hello():
    return "hello", 200

@apiMain.route('/welcome')
def welcome():
    return "Welcome to watxonx-ai Util application", 200

@apiMain.route('/about')
def about():
    return render_template('about.html')

# Route for the contact page
@apiMain.route('/contact')
def contact():
    return render_template('contact.html')

# Route for the contact page
@apiMain.route('/agb')
def agb():
    return render_template('agb.html')

@apiMain.route('/api/agb/invoke', methods=['POST'])
def invoke_text():
    logger.debug("/api/agb/invoke ...")

    payload = request.get_json()

    ### Call the main function to get the response
    agbMain = AgbMain()
    resp = agbMain.invoke(payload)

    return resp, 200

