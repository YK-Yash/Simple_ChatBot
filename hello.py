# -*- coding: utf-8 -*-
"""
Created on Sat Mar 17 21:54:36 2018

@author: Dell
"""

from flask import Flask

app = Flask(__name__)

@app.route("/")
def hello():
    return "Hello World!"


if __name__ == '__main__':
    app.run(debug=True)