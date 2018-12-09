__author__ = 'Thilina_08838'
import urllib.request
from urllib.request import urlopen

from flask import *

from helper import json_serialize


def init_ussd_sender(app, IDEA_PASSWD, SMS_GW_HOST, IDEA_APP_ID,DEST_TEL_NUM):
    @app.route('/ussdSender', methods=["GET", "POST"])
    def ussd_sender():
        res = {
            "message": "1. Press One 2. Press two 3. Press three, 4. Exit",
            "destinationAddress": "tel:"+str(DEST_TEL_NUM),  # Use the MSISDN in the same format you received
            "password": str(IDEA_PASSWD),  # This should be replaced with your ideamart app password
            "applicationId": str(IDEA_APP_ID),  # Replace this with your APP ID
            "ussdOperation": "mt-cont",
            "sessionId": "1330929317043"
        }
        with open("USSDMT.txt", "w") as text_file:
            print("Message sent: {}".format(res), file=text_file)
        url = str(
            SMS_GW_HOST) + "/ussd/send"  # Change the end point to the production when using in the live environment

        res = json.dumps(res).encode('utf8')
        req = urllib.request.Request(url, res,
                                     headers={"Content-Type": "application/json", "Accept": "application/json"})
        response = urlopen(req)
        return jsonify({"msg": "ussd sent", "data": json_serialize(response.read())})
