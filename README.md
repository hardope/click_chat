# web-based-messenger
## Design and development of a web based messenger application
### Steps on installation
* Download file
* Unzip file
* Save file to directory
* Open command-line
* make sure python is installed
* install flask to pip

### LogIn Details For 2 users
   Username: Password
1. Karen: karenpassword
2. Jarvis: jarvispassword
## Video Demo:  <https://youtu.be/Uu9KiFMZaAU>
#### Description:

My Project takes it name after a popular social media platform from META "Messenger", Though its more of a mini version. My project is a basic messaging
platform with two users both having a username and password. On loading the page the website will display a login page, for a username and password, if
the username and password are correct you will be logged in to the messages route, but if not an error page will be rendered with the error detail.

### app.py:

This is my web application, It handles all the back end operations and renders the necessary htnl pages, also it is responsible for accessing and
entering data into the database. Also it checks for the methods employed by the page requests and reacts to them, respectively and redirects to new pages
necessary.

#### @app.route("/messages")

In this route a connection is set to the sqlite database and then data s read for messages to be displayed, also there is a text field for new messages,
after a new message is submitted to the new route, the new route then handles the database command of inserting the new message into database.

#### @app.route("/", methods=["GET", "POST"])

At this route is the login page, it supports two methods and if the request method is 'GET' it simply renders the login page. Whereas if the request
method is 'POST' it means the form is submitted and then the data from the form is collected and checked for validating and if any error occurs during this
process the user will be redirected to the error page where the detail of the error will be displayed. On the other hand if the username and password are
correct the user will be redirected to the message route where the message is displayed and new messages can be sent.

@app.route("/new" , methods=["POST"])

At this route new messages from the messages route are submitted, then the database is connected and new messages are entered to the database.

### messenger.db:
This is the database used to store the database and the users using two tables namely: "users" and "messages" with needed columns, this table
timestamps the messages as they arrive.

#### TABLE user

In this table the username for the two users and their passwords are stored, in order to allow the python application to access and crossheck them with
submitted data.

#### TABLE messages

In this table the message is stored along with a time stamp created along side them, this enables other users to access the message.

### error.html:
This is the error page that tells the user about the cause of an error after ane has occured.

### index.html:
This is the messages page, it is where message can be read and new messages can be sent, it refreshes within a time interval to enable instant
messaging. In this page the result of the sql command to selected by the python app is passed as input and several Jinja syntax and for loops are used to
breakdown the data and display it effectively.

### login.html:
This is the page that contains a form with two inputs to enable the user to login, this page will be rredirected to the error page if there is
an error and to the messages page if login was successful.
