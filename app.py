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
app.debug = True

dotenv_path = join(dirname(__file__), '.env')
load_dotenv(dotenv_path)

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


@app.route('/caasSender', methods=["GET", "POST"])
def caas_request():
    res = {
        "chargeableBalance": "10",
        "password": str(IDEA_PASSWD),  # This should be replaced with your ideamart app password
        "applicationId": str(IDEA_APP_ID),  # Replace this with your APP ID
        "paymentInstrumentName": "MobileAccount",
        "subscriberId": "94777123456",  # Use the MSISDN in the format you received
        "currency": "LKR"
    }
    with open("CAASRequest.txt", "w") as text_file:
        print("CAAS request: {}".format(res), file=text_file)
    url = str(SMS_GW_HOST) + "/caas/balance/query"  # Use production API end point in the live system

    res = json.dumps(res).encode('utf8')
    req = urllib.request.Request(url, res, headers={"Content-Type": "application/json", "Accept": "application/json"})
    response = urlopen(req)
    ideamart_respones = response.read()
    with open("CAASResponse.txt", "w") as text_file:
        print("CAAS response: {}".format(ideamart_respones), file=text_file)
    return jsonify({"data": json_serialize(ideamart_respones)})


@app.route('/lbsSender', methods=["GET", "POST"])
def lbs_request():
    res = {
        "password": str(IDEA_PASSWD),  # This should be replaced with your ideamart app password
        "applicationId": str(IDEA_APP_ID),  # Replace this with your APP ID
        "subscriberId": "tel:94771234567",  # Use the MSISDN in the format you received
        "serviceType": "IMMEDIATE",
        "responseTime": "NO_DELAY",
        "freshness": "HIGH",
        "horizontalAccuracy": "1500",
        "vesrion": "2.0"
    }

    with open("LBSRequest.txt", "w") as text_file:
        print("LBS request: {}".format(res), file=text_file)
    url = str(SMS_GW_HOST) + "/lbs/locate"  # Use production URL in the live system

    res = json.dumps(res).encode('utf8')
    req = urllib.request.Request(url, res, headers={"Content-Type": "application/json", "Accept": "application/json"})
    response = urlopen(req)
    ideamart_respones = response.read()
    with open("LBSResponse.txt", "w") as text_file:
        print("LBS response: {}".format(ideamart_respones), file=text_file)
    return jsonify({"data": json_serialize(ideamart_respones)})


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
    req = urllib.request.Request(url, res, headers={"Content-Type": "application/json", "Accept": "application/json"})
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


# @app.route('/ussdReceiver', methods=["GET", "POST"])
# def ussd_receiver():
#     if request.method == "GET":
#         response = make_response("Yes, you are alive")
#         response.headers['Content-Type'] = 'application/json'
#         response.headers['Accept'] = 'application/json'
#         return response
#     else:
#         message_content = json.loads(request.data)
#         with open("USSDMO.txt", "w") as text_file:
#             print("Message Received: {}".format(message_content), file=text_file)


@app.route('/ussdSender', methods=["GET", "POST"])
def ussd_sender():
    res = {
        "message": "1. Press One 2. Press two 3. Press three, 4. Exit",
        "destinationAddress": "tel:94777123456",  # Use the MSISDN in the same format you received
        "password": str(IDEA_PASSWD),  # This should be replaced with your ideamart app password
        "applicationId": str(IDEA_APP_ID),  # Replace this with your APP ID
        "ussdOperation": "mt-cont",
        "sessionId": "1330929317043"
    }
    with open("USSDMT.txt", "w") as text_file:
        print("Message sent: {}".format(res), file=text_file)
    url = str(SMS_GW_HOST) + "/ussd/send"  # Change the end point to the production when using in the live environment

    res = json.dumps(res).encode('utf8')
    req = urllib.request.Request(url, res, headers={"Content-Type": "application/json", "Accept": "application/json"})
    response = urlopen(req)
    return jsonify({"msg": "ussd sent", "data": json_serialize(response.read())})


if __name__ == '__main__':
    app.logger.info(str("SMS GATEWAY IN .env file-->> {}").format(str(os.environ["SMS_GW_HOST"])))
    app.run(host="0.0.0.0", port=int(os.environ["PORT"]))
