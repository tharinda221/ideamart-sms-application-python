# Copyright 2016 Tharinda Ehelepola
#
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
# http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# https://github.com/tharinda221/simple-flask-web-application.git
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.

import logging
import urllib2

from flask import *

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
        url = "http://localhost:7000/sms/send"
        req = urllib2.Request(url, data=json.dumps(res),
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
