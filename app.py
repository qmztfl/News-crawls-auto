import json
import time

from flask import Flask, render_template, current_app
from scrapy import cmdline

from config import getdata

data = getdata.data()

app = Flask(__name__)


@app.route('/')
def drink():  # put application's code here
    context = data.index()
    return render_template('index.html', context=context)


@app.route('/cs')
def cs():  # put application's code here
    context = data.hangkong()
    return render_template('hangkong.html', context=context)


@app.route('/family')
def family():  # put application's code here
    context = data.guoji()
    return render_template('guoji.html', context=context)


@app.route('/activity')
def activity():  # put application's code here
    context = data.guonei()
    return render_template('guonei.html', context=context)


@app.route('/other')
def other():
    context = data.war()
    return render_template('war.html', context=context)


def flask_main():
    app.run(host='127.0.0.1:5000')


if __name__ == '__main__':
    # app.run(host='0.0.0.0')
    flask_main()
