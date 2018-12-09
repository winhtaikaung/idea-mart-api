from helper import json_serialize

__author__ = 'Thilina_08838'

import urllib.request
from urllib.request import urlopen

from flask import *


def init_caas_request(app, IDEA_PASSWD, SMS_GW_HOST, IDEA_APP_ID, ):
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
        req = urllib.request.Request(url, res,
                                     headers={"Content-Type": "application/json", "Accept": "application/json"})
        response = urlopen(req)
        ideamart_respones = response.read()
        with open("CAASResponse.txt", "w") as text_file:
            print("CAAS response: {}".format(ideamart_respones), file=text_file)
        return jsonify({"data": json_serialize(ideamart_respones)})
