#from flask import Flask
#app = Flask(__name__)

#@app.route("/")
#def hello():
 #   return "Hello World!"

from helpers import create_app



app = create_app()

if __name__ == "__main__":
    app.run(host='0.0.0.0', port=5000) #default is 127.0.0.1



