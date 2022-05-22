#!/usr/bin/env python3
# -*- encoding: utf-8 -*-
'''
Created on   :2022/04/16 18:55:58
@author      :Caihao (Chris) Cui
@file        :webapp.py
@content     :xxx xxx xxx
@version     :0.1.0 in DevOpt
@License :   (C)Copyright 2021 MIT
'''

# here put the import lib
'''
export FLASK_APP=./src/webapp.py
flask run
'''

from ast import Global
from flask import Flask
from flask import render_template

from flask import Flask, render_template, request, redirect, url_for
from joblib import load

from .data.sample_format import convert_sample
from joblib import load
import pandas as pd
import random

from autogluon.tabular import TabularPredictor

app = Flask(__name__)


@app.route("/")
def hello_world():
    # return "<p>Hello, World!</p>"
    return render_template('index.html')


# def prediction(xin):
#     model = load('./src/model_DT.joblib')
#     df_xin = pd.DataFrame(xin, index=[0])
#     df_xin.set_index('client_id', inplace=True)
#     x = df_xin.values
#     y_pred = model.predict(x)
#     y_proba = model.predict_proba(x)
#     return y_pred, y_proba


# when the post method detect, then redirect to success function
@app.route('/result', methods=['POST'])
def result():
    if request.method == 'POST':
        sample = request.form.to_dict()

        print(sample)
        # print('*'*50)
        # xin = convert_sample(sample)
        # print(xin)
        # print('*'*50)

        # df_xin = pd.DataFrame(xin, index=[0])

        df_xin = pd.DataFrame([sample])
        df_xin.set_index('client_id', inplace=True)
        print(df_xin)

        # model = load('./src/model_DT.joblib')
        # x = df_xin.values
        # print('model input: {x}'.format(x=x))

        print('*' * 50)

        # model = TabularPredictor.load('./models/agModels-predictClass')
        model = TabularPredictor.load('./models/agModels-CleanRawF1')
        y_pred = model.predict(df_xin)
        y_proba = model.predict_proba(df_xin)
        print(y_pred, y_proba)
        result = y_pred.values[0]
        proba = y_proba.values[0, 1]
    else:
        result = 'yes' if random.random() > 0.5 else 0

    # if int(result)== 1:
    if result == 'yes':
        action = 'Call this Client!'
    else:
        action = "Go Next and Come Back Later!"
    return render_template("result.html",
                           client_details=sample,
                           action=action,
                           probability=proba)
