__author__ = 'Thilina_08838'

import urllib.request
from urllib.request import urlopen

from flask import *

from helper import json_serialize


def init_lbs_sender(app, IDEA_PASSWD, SMS_GW_HOST, IDEA_APP_ID,SUBSCRIBER_ID):
    @app.route('/lbsSender', methods=["GET", "POST"])
    def lbs_request():
        res = {
            "password": str(IDEA_PASSWD),  # This should be replaced with your ideamart app password
            "applicationId": str(IDEA_APP_ID),  # Replace this with your APP ID
            "subscriberId": "tel:"+str(SUBSCRIBER_ID),  # Use the MSISDN in the format you received
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
        req = urllib.request.Request(url, res,
                                     headers={"Content-Type": "application/json", "Accept": "application/json"})
        response = urlopen(req)
        ideamart_respones = response.read()
        with open("LBSResponse.txt", "w") as text_file:
            print("LBS response: {}".format(ideamart_respones), file=text_file)
        return jsonify({"data": json_serialize(ideamart_respones)})
