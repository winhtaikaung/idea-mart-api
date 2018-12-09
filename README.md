

# Welcome to Ideamart

[![N|Solid](http://www.ideamart.lk/web/wp-content/uploads/2017/02/logo-dark.png)](https://nodesource.com/products/nsolid)

What do you get when you couple your programming knowledge with the Ideamart platform? An IdeaPro application with endless possibilities!
Imagine you need to send an SMS and get the delivery notification, invoke a USSD menu in a registered user’s phone, or even make an in in-app purchase through the carrier billing! IdeaPro is where you can bring your ideas to life!

  #### Ideamart by Platform

  - ###### Java  - [API Reference](http://breakdance.io)
  - ###### PHP -  [API Reference](http://breakdance.io)
  - ###### Python -  [API Reference](http://breakdance.io)
  - ###### Go -  [API Reference](http://breakdance.io)


#### Ideamart by Product

  - ###### SMS API(Short Message Service)
  - ###### USSD API(Unstructured Supplementary Service Data)
  - ###### CaaS API(Charging as a Service)
  - ###### LBS API (Location Based Service)
  - ###### Subscription API
  - ###### IVR API

# New Features!

  - offline simulator which you can test your apps


# Getting Started

Getting started with the ideamart API's couldn't be easier

### Server Requirments
ideamart officially support PHP, Java, Python, Go, Nodejs programming languages

##### Python requirments
Python 3.4.3 is supported

### Installation  with Docker
If you have docker installed in your machine,

```sh
$ git clone < https://github.com/ideamartio/ideamart-python.git >
```
if you have docker installed
```sh
$ cd ideamart-python && docker-compose build && docker-compose up
```

### Installation  with virtualenv
  ```sh
  mkvirtualenv your_desired_name -p python3
  ```
  then type
  ```
  workon your_desired_name
  ```
and install dependencies
```
pip install -r requirements.txt
```
change .env file as follow
```
ENV=develop

SMS_GW_HOST=https://api.dialog.lk

PORT=5000

IDEA_APP_ID=your_idea_app_id

IDEA_PASSWD=your_idea_password
```
```
then run

```
python app.py
```


or download the developer bundle with   [sample codes](http://www.ideamart.lk/web/idea-pro/downloads/download-list/) here

 # Feedback
Report any feedback or problems with this Release Candidate to the Github Issues for ideamart API.


License
----

MIT
## License
This project is licensed under the MIT License - see the LICENSE.md file for details