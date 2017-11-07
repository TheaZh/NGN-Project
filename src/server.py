from flask import Flask, render_template
from pymongo import MongoClient
app = Flask(__name__)

@app.route('/')
def log_in():
    return render_template('/pages/login.html')



if __name__ == '__main__':
    app.run()
