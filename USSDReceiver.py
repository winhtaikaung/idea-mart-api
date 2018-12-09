__author__ = 'Thilina_08838'
import urllib.request
from urllib.request import urlopen

from flask import *

from helper import json_serialize


def init_ussd_receiver(app, IDEA_PASSWD, SMS_GW_HOST):
    @app.route('/ussdReceiver', methods=["GET", "POST"])
    def ussd_receiver():
        if request.method == "GET":
            response = jsonify({"msg": "Yes, you are alive"})
            response.headers['Content-Type'] = 'application/json'
            response.headers['Accept'] = 'application/json'
            return response
        else:
            message_content = json.loads(request.data)
            with open("USSDMO.txt", "w") as text_file:
                print("Message Received: {}".format(message_content), file=text_file)
            name = message_content["message"].split(" ")[1]
            res = {'message': "Hi, " + name,
                   "destinationAddress": message_content["sourceAddress"].split(" ")[0],
                   "password": str(IDEA_PASSWD),  # This should be replaced with your ideamart app password
                   "applicationId": message_content["applicationId"],
                   "ussdOperation": message_content["ussdOperation"],
                   "sessionId": message_content["sessionId"]
                   }
            with open("USSDMT.txt", "w") as text_file:
                print("Message sent: {}".format(res), file=text_file)
            url = str(
                SMS_GW_HOST) + "/ussd/send"  # Change the end point to the production when using in the live environment

            res = json.dumps(res).encode('utf8')
            req = urllib.request.Request(url, res,
                                         headers={"Content-Type": "application/json", "Accept": "application/json"})
            response = urlopen(req)
            return jsonify({"data": json_serialize(response.read())})
