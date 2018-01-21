__author__ = 'Thilina_08838'
from flask import *

import logging

from urllib.request import urlopen
html = urlopen("http://www.google.com/")
print(html)

app = Flask(__name__)
app.debug = True


@app.route('/')
def hello_world():
    return render_template("index.html")


@app.route('/smsReceiver', methods=["GET", "POST"])
def sms_receiver():
    """
    This method is to retrieve request came from ideamart simulator of dialog and send sms message
    :return:
    """


    if request.method == "GET":
        response = make_response("Telco App is running")
        response.headers['Content-Type'] = 'application/json'
        response.headers['Accept'] = 'application/json'
        return response
    else:
        ideamart_message = json.loads(request.data)
        name = ideamart_message["message"].split(" ")[1]
        res = {'message': "Hi, " + name,
               "destinationAddresses": ideamart_message["sourceAddress"],
               "password": "password",  # This should be replaced with your ideamart app password
               "applicationId": ideamart_message["applicationId"]
               }

        # URL should be  changed to https://api.dialog.lk/sms/send when you host the application
        url = "http://localhost:5000/sms/send"
        req = urllib.request.Request(url, data=json.dumps(res),
                              headers={"Content-Type": "application/json", "Accept": "application/json"})
        response = urllib2.urlopen(req)
        ideamart_respones = response.read()
        logging.error("Result content: " + ideamart_respones)

        if response.getcode() == 200:
            logging.info('*** Message delivered Successfully! ****')
            response = make_response("Message delivered Successfully!")
            response.headers['Content-Type'] = 'application/json'
            response.headers['Accept'] = 'application/json'
            return response
        else:
            logging.error(
                '*** Message was not delivered Successfully!! ERROR-CODE: ' + str(response.getcode()) + ' ****')
            response = make_response("Message was not delivered Successfully!")
            response.headers['Content-Type'] = 'application/json'
            response.headers['Accept'] = 'application/json'
            return response


if __name__ == '__main__':
    app.run(host="localhost", port=5000)