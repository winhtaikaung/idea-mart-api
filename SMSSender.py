__author__ = 'Thilina_08838'
import urllib.request
from urllib.request import urlopen

from flask import *

from helper import json_serialize


def init_sms_sender(app, IDEA_PASSWD, SMS_GW_HOST, IDEA_APP_ID):
    @app.route('/smsSender', methods=["GET", "POST"])
    def sms_sender():
        res = {
            "message": "Hello World",
            "destinationAddresses": "tel:94771122336",  # Use the number, in format received from ideamart
            "password": str(IDEA_PASSWD),  # This should be replaced with your ideamart app password
            "applicationId": str(IDEA_APP_ID)  # Replace this with your APP ID
        }
        with open("SMSMT.txt", "w") as text_file:
            print("send message: {}".format(res), file=text_file)
        url = str(SMS_GW_HOST) + "/sms/send"  # Use production API in the live environment

        res = json.dumps(res).encode('utf8')  # Send the encoded value to the API call
        req = urllib.request.Request(url, res,
                                     headers={"Content-Type": "application/json", "Accept": "application/json"})
        response = urlopen(req)

        if response.getcode() == 200:
            app.logger.info('Message delivered Successfully!')
            response = jsonify({"msg": "Message delivered Successfully!", "data": json_serialize(response.read())})
            response.headers['Content-Type'] = 'application/json'
            response.headers['Accept'] = 'application/json'
            with open("DeliveryNotify.txt", "w") as text_file:
                print("send message: {}".format(response), file=text_file)
            return response
        else:
            app.logger.error('Message not delivered Successfully ERROR-CODE: ' + str(response.getcode()) + '')
            response = jsonify({"msg": 'Message not delivered Successfully ERROR-CODE: ' + str(response.getcode()) + '',
                                "data": json_serialize(response.read())})
            response.headers['Content-Type'] = 'application/json'
            response.headers['Accept'] = 'application/json'
            with open("DeliveryNotify.txt", "w") as text_file:
                print("send message: {}".format(response), file=text_file)
            return response
