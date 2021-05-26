from oauth2client.service_account import ServiceAccountCredentials
import gspread
import os
import datetime
from pytz import timezone
from flask import Flask, render_template, request, redirect

# setting timezone to EST
tz = timezone('US/Eastern')

import menuitems

# creating a list of foods
foods = menuitems.return_s().split("\n")

# stripping garbage out of the foods and reversing the list
foods = [x.strip() for x in foods]
del foods[-1]
print(foods)
# removing the first index because for some reason it's blank

# getting the date for future use
date = datetime.datetime.now(tz)

# setting all date variables for future use
year = date.year
month = date.month
day = date.day

del foods[0]

# setting up the google drive api
scope = ['https://spreadsheets.google.com/feeds', 'https://www.googleapis.com/auth/drive']
credentials = ServiceAccountCredentials.from_json_keyfile_name("client_secret.json", scope)
client = gspread.authorize(credentials)
sheet = client.open("database").sheet1


# method to get the next available row in the spreadsheet
def next_available_row():
	str_list = list(filter(None, sheet.col_values(1)))
	return str(len(str_list)+1)

# method to get the next available column in the spreadsheet
def next_available_column(row):
	values_list = sheet.row_values(row)
	return (len(values_list)+1)

# Armaan what does this do
def find_between( s, first, last ):
    try:
        start = s.index( first ) + len( first )
        end = s.index( last, start )
        return s[start:end]
    except ValueError:
        return ""

# creating an instance of the flask object
app = Flask(__name__)

# main page
@app.route('/')
def index():
	global foods, year, month, day
	return render_template("index.html", foods=foods, year=year, month=month, day=day)

# thank you page for when they submit something
@app.route('/thanks')
def thanks():
    return render_template("thanks.html")

# review page that takes the date 
@app.route('/review/<date>')
def hello(date):
	global foods
	# foods = foods[1:]
	return render_template("rating.html", foods=foods, date=day)

# 
@app.route('/review/<date>', methods=['POST'])
def hello_post(date):
	comment = request.form['text']
	rating = request.form['dropdown']
	r = next_available_row()
	# Updating date column 
	sheet.update_cell(r, 1, date)
	
	# Updating comment column
	sheet.update_cell(r, 2, comment)

	# Updating rating column
	sheet.update_cell(r, 3, rating)

	return redirect('/thanks')

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=8080)
	