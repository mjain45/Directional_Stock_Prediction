#!/usr/bin/env python
# encoding: utf-8
import json
from flask import Flask, request
from get_stock_direction import get_direc
from datetime import datetime


app = Flask(__name__)
@app.route('/getDirection')

def index():
    ticker_gms = [('AMZN',2), ('AAPL', 1)]
    str_time = request.args.get("time")####
    # time = request.args.get("time")
    # print("date is ", date)
    # print("time is ", time)
    # dt_time = datetime.combine(datetime.date(2011, 1, 1), 
                          #datetime.time(10, 23))
    
    str_time = str_time[:-5]
    
    orig_dt = datetime.strptime(str_time, '%Y-%m-%dT%H:%M:%S') #Input date time
    print("time is ...", orig_dt)
    res = get_direc(ticker_gms, orig_dt)
    print("result is : ", res)
    return json.dumps(res)

app.run()