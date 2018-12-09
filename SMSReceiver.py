__author__ = 'Thilina_08838'

from flask import *


def init_sms_receiver(app):
    @app.route('/smsReceiver', methods=["GET", "POST"])
    def sms_receiver():
        if request.method == "GET":
            response = jsonify({"msg": "Yes, you are alive"})
            response.headers['Content-Type'] = 'application/json'
            response.headers['Accept'] = 'application/json'
            return response
        else:
            message_content = json.loads(request.data)

        with open("SMSMO.txt", "w") as text_file:
            print("Received message: {}".format(message_content), file=text_file)  # Capture the incoming SMS
        return jsonify({"data": message_content})
