from flask import Blueprint, request, render_template
import logging, os

from control_burn.ControlBurnMain import ControlBurnMain

apiControlBurn = Blueprint('api_control_burn', __name__)

logger = logging.getLogger(__name__)
logger.setLevel(os.environ.get('LOGLEVEL', 'INFO').upper())

@apiControlBurn.route('/api/control_burn/invoke', methods=['POST'])
def invoke_control_burn():
    logger.debug("/api/control_burn/invoke ...")

    payload = request.get_json()

    ### Call the main function to get the response
    controlBurnMain = ControlBurnMain()
    resp = controlBurnMain.invoke(payload)

    return resp, 200

# Route for the contact page
@apiControlBurn.route('/control_burn')
def control_burn():
    return render_template('control_burn/control_burn.html')

