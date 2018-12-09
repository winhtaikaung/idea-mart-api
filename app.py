#! usr/bin/python
# -*- coding: utf-8 -*-
import os
import urllib.request
from os.path import join, dirname
from urllib.request import urlopen

from dotenv import load_dotenv
from flask import *

from helper import json_serialize

app = Flask(__name__)

dotenv_path = join(dirname(__file__), '.env')
load_dotenv(dotenv_path, verbose=True)

if os.environ["ENV"] != "production":
    app.debug = True
else:
    app.debug = False

SMS_GW_HOST = os.environ["SMS_GW_HOST"]
IDEA_APP_ID = os.environ["IDEA_APP_ID"]
IDEA_PASSWD = os.environ["IDEA_PASSWD"]


@app.route('/', methods=["GET"])
def index():
    return jsonify({
        "msg": "this is un official version of idea-mart api please be considerate before you use and api will change time to time.Please keep an eye on the postman and your neighbourings ;)",
        "api_endpoint": 'https://idea-mart.herokuapp.com',
        "repo_url": "https://github.com/winhtaikaung/idea-mart-api",
        "postman_collection": "https://www.getpostman.com/collections/722bc31cf3fb4d522be0",
        "contact": "http://t.me/waung"})


@app.route('/smsOperation', methods=["GET", "POST"])
def sms_ops():
    if request.method == "GET":

        response = jsonify({"msg": "Yes, you are alive"})
        response.headers['Content-Type'] = 'application/json'
        response.headers['Accept'] = 'application/json'
        return response
    else:
        message_content = json.loads(request.data)

        with open("SMSMO.txt", "w") as text_file:
            print("Received message: {}".format(message_content), file=text_file)  # Capture the incoming SMS

        message = message_content["message"].split(" ")[1]
        res = {'message': " " + message,
               "destinationAddresses": message_content["sourceAddress"].split(" ")[0],
               "password": str(IDEA_PASSWD),  # This should be replaced with your ideamart app password
               "applicationId": message_content["applicationId"]
               }
        with open("SMSMT.txt", "w") as text_file:
            print("send message: {}".format(res), file=text_file)
        url = str(SMS_GW_HOST) + "/sms/send"  # Don't use localhost in the live API

        res = json.dumps(res).encode('utf8')  # Send the encoded value to the API call
        req = urllib.request.Request(url, res,
                                     headers={"Content-Type": "application/json", "Accept": "application/json"})
        response = urlopen(req)

        if response.getcode() == 200:
            app.logger.info('Message delivered Successfully!')
            response = jsonify({"msg": "Message delivered Successfully!", "data": json_serialize(response.read())})
            response.headers['Content-Type'] = 'application/json'
            response.headers['Accept'] = 'application/json'
            with open("DeliveryNotif.txt", "w") as text_file:
                print("send message: {}".format(response), file=text_file)
            return response
        else:
            app.logger.error(
                '*** Message not delivered Successfully ERROR-CODE: ' + str(response.getcode()) + ' ****')
            response = jsonify({"msg": "Message delivered Successfully!", "data": json_serialize(response.read())})
            response.headers['Content-Type'] = 'application/json'
            response.headers['Accept'] = 'application/json'
            with open("DeliveryNotif.txt", "w") as text_file:
                print("send message: {}".format(response), file=text_file)
            return response


if __name__ == '__main__':
    app.logger.info(str("SMS GATEWAY IN .env file-->> {}").format(str(os.environ["SMS_GW_HOST"])))
    from USSDReceiver import init_ussd_receiver
    from SMSSender import init_sms_sender
    from SMSReceiver import init_sms_receiver
    from ussdSender import init_ussd_sender
    from LBS import init_lbs_sender
    from CAAS import init_caas_request

    init_ussd_receiver(app, IDEA_PASSWD, SMS_GW_HOST)
    init_ussd_sender(app, IDEA_PASSWD, SMS_GW_HOST, IDEA_APP_ID)
    init_sms_sender(app, IDEA_PASSWD, SMS_GW_HOST, IDEA_APP_ID)
    init_sms_receiver(app)
    init_lbs_sender(app, IDEA_PASSWD, SMS_GW_HOST, IDEA_APP_ID)
    init_caas_request(app, IDEA_PASSWD, SMS_GW_HOST, IDEA_APP_ID)
    app.run(host="0.0.0.0", port=int(os.environ["PORT"]))
