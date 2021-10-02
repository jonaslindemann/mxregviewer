#!/bin/env python3

from flask import Flask
from flask import render_template
from flask import request
from datetime import datetime


from tabulate import tabulate

import mxreg

app = Flask(__name__)

time_sheet = mxreg.TimeSheet()
#time_sheet.connect()
#time_sheet.update()

@app.route('/', methods=['POST', 'GET'])
@app.route('/index', methods=['POST', 'GET'])
def index():

    if request.method == 'POST':
        time_sheet.date_str = request.form.get("current_date_str")
    else:
        current_date = datetime.now()
        time_sheet.date_str = current_date.strftime("%Y-%m-%d")
     
    registration_table = time_sheet.query_date(time_sheet.date_str)

    if len(registration_table)>0:

        columns = registration_table[0]
        data = registration_table[1:]

        columns = ["Datum/Tid", "Namn", "Personnummer", "Licens", "Mobil", "Klubb", "Klass", "Bana", "TA", "Email"]
        field_size = ["15%", "25%", "10%", "10%", "10%", "15%", "20%", "20%", "5%", "20%"]

        column_fields = []

        i = 1
        for column in columns:
            col_templ = "{ field: 'fld%d', text: '%s', size: '%s', sortable: true }" % (i, column, field_size[i-1])
            if i<len(columns):
                column_fields.append(str(col_templ)+",")
            else:
                column_fields.append(str(col_templ))
            i+=1

        record_fields = []

        i = 1
        for record in data:
            rec_templ = "{ recid: %d, " % i

            j = 1
            for value in record:
                rec_templ += "fld%d: '%s' " % (j, value)
                if j<len(record):
                    rec_templ += ", "
                j+=1

            if i<len(data):
                rec_templ += "},"
            else:
                rec_templ += "}"
            
            record_fields.append(rec_templ)

            i+=1

        return render_template('index.html', title='Dagens tränande', columns=column_fields, records=record_fields, current_date_str=time_sheet.query_date)
    else:
        return render_template('index.html', title='Dagens tränande', columns=[], records=[], current_date_str=time_sheet.date_str)
