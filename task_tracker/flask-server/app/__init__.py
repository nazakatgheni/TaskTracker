from flask import Flask
# this line of code will make flask available for app


#without this code it doesn't run
app = Flask(__name__)

app.secret_key = "my_secret_key"