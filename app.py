# weather
#Documentation
#flash error messages

#fix traffic map 

# Necessary Packages to import

stringofpath = '/home/gregory.swedeen/htdocs/AdvWebDev/env/lib/python3.6/site-packages'
import sys
sys.path.append(stringofpath)
import twitterAPITest
import googlemaps
from datetime import datetime
from flask import Flask, redirect, url_for, flash, request
from flask import render_template, jsonify
import pymysql
from flask_bootstrap import Bootstrap
from flask_pymongo import PyMongo
from pymongo import MongoClient
from flask_wtf import FlaskForm, csrf
from wtforms import StringField, SubmitField, validators, SelectField, PasswordField
from wtforms.validators import DataRequired, Length

# Initialize the MongoDB client
ENDPOINT = "mongodb://127.0.0.1:27017"
PORT = 27017
client = MongoClient(ENDPOINT, PORT) 
#Select the Database
db = client.testDatabase  
# Collections
tweets = db.tweets
user = db.user
locations = db.locations
Trends = db.Trends

# GOOGLE MAPS 
apiKey= 'AIzaSyAd9VpWUwhwQ9RxWSfbvlNMYAwl-McVt3k'
gmaps = googlemaps.Client(key=apiKey)

# Flask App
app = Flask(__name__)
app.config.from_mapping(SECRET_KEY='dev', DATABASE= ENDPOINT,)
Bootstrap(app)

# MySQL Connection
connection = pymysql.connect("cs2s.yorkdc.net", "gregory.swedeen", "KFDP5DAP", "gregoryswedeen")

# Form for creating an Account
class userForm(FlaskForm):
	userName = StringField('Username',validators=[DataRequired()])
	password = PasswordField('Password',validators=[DataRequired(), Length(min=2)])
	submit = SubmitField('Submit')

# default route, making the user login
@app.route('/')
def defaultRoute():
	return redirect('/login')

# Get the distance and time to destination based on input
def getDistanceStats():
	users = user.find({})
	Locations = locations.find({})
	if users.count() == 0 or Locations.count() == 0:
		CurrentUser = 'Please Log In'
		startLocation = 'Please Enter Location'
		stopLocation = 'Please Enter Destination'
		lat = 'Please Enter Location'
		lng = 'Please Enter Location'
		destLat = 'Please Enter Location'
		destLng = 'Please Enter Location'
	else:
		CurrentUser = user.find()[0]['user']
		startLocation = locations.find()[0]['start']
		stopLocation = locations.find()[0]['stop']
		geocode_result = gmaps.geocode(startLocation)
		lat = geocode_result[0]['geometry']['location']['lat']
		lng = geocode_result[0]['geometry']['location']['lng']
		destination = locations.find()[0]['stop']
		geocode_result = gmaps.geocode(destination)
		destLat = geocode_result[0]['geometry']['location']['lat']
		destLng = geocode_result[0]['geometry']['location']['lng']
		CurrentUser = user.find()[0]['user']
		startLocation = locations.find()[0]['start']
		stopLocation = locations.find()[0]['stop']
	results = gmaps.distance_matrix(startLocation,stopLocation)['rows'][0]['elements'][0]
	distance = results['distance']['text']
	duration = results['duration']['text']
	print(duration,distance)
	return (duration + ' ' + distance)

# Map to display the directions and distanceStats for the given route
@app.route('/directionMap')
def directionMap():
	users = user.find({})
	Locations = locations.find({})
	if users.count() == 0 or Locations.count() == 0:
		CurrentUser = 'Please Log In'
		startLocation = 'Please Enter Location'
		stopLocation = 'Please Enter Destination'
		lat = 'Please Enter Location'
		lng = 'Please Enter Location'
		destLat = 'Please Enter Location'
		destLng = 'Please Enter Location'
		distance = '0'
	else:
		CurrentUser = user.find()[0]['user']
		startLocation = locations.find()[0]['start']
		stopLocation = locations.find()[0]['stop']
		geocode_result = gmaps.geocode(startLocation)
		lat = geocode_result[0]['geometry']['location']['lat']
		lng = geocode_result[0]['geometry']['location']['lng']
		destination = locations.find()[0]['stop']
		geocode_result = gmaps.geocode(destination)
		destLat = geocode_result[0]['geometry']['location']['lat']
		destLng = geocode_result[0]['geometry']['location']['lng']
		CurrentUser = user.find()[0]['user']
		startLocation = locations.find()[0]['start']
		stopLocation = locations.find()[0]['stop']
		distance = getDistanceStats()
	return render_template('directionsMap.html', lat = lat, lng = lng, destLat = destLat, destLng = destLng, user = CurrentUser, start = startLocation, stop = stopLocation, distance = distance)

# Default page once logged in
@app.route('/page',methods=['GET','POST'])
def page():
	users = user.find({})
	Locations = locations.find({})
	if users.count() == 0 or Locations.count() == 0:
		CurrentUser = 'Please Log In'
		startLocation = 'Please Enter Location'
		stopLocation = 'Please Enter Destination'
		print('worked')
	else:
		CurrentUser = user.find()[0]['user']
		startLocation = locations.find()[0]['start']
		stopLocation = locations.find()[0]['stop']
	return render_template('index.html', user = CurrentUser, start = startLocation, stop = stopLocation)

# Map to display current traffic conditions focused on the users start location
@app.route('/renderMap',methods=['GET','POST'])
def renderMap():
	if request.method == 'GET':
		users = user.find({})
		Locations = locations.find({})
		if users.count() == 0 or Locations.count() == 0:
			CurrentUser = 'Please Log In'
			startLocation = 'Please Enter Location'
			stopLocation = 'Please Enter Destination'
			lat = 'Please Enter Location'
			lng = 'Please Enter Location'
			destLat = 'Please Enter Location'
			destLng = 'Please Enter Location'
		else:
			CurrentUser = user.find()[0]['user']
			startLocation = locations.find()[0]['start']
			stopLocation = locations.find()[0]['stop']
			geocode_result = gmaps.geocode(startLocation)
			lat = geocode_result[0]['geometry']['location']['lat']
			lng = geocode_result[0]['geometry']['location']['lng']
			destination = locations.find()[0]['stop']
			geocode_result = gmaps.geocode(destination)
			destLat = geocode_result[0]['geometry']['location']['lat']
			destLng = geocode_result[0]['geometry']['location']['lng']
			CurrentUser = user.find()[0]['user']
			startLocation = locations.find()[0]['start']
			stopLocation = locations.find()[0]['stop']
		return render_template('map.html', lat = lat, lng = lng, destLat = destLat, destLng = destLng,user = CurrentUser, start = startLocation, stop = stopLocation)

# Set the users start location
@app.route('/startLocation',methods=['GET','POST'])
def startLocation():
	if request.method == 'GET':
		users = user.find({})
		Locations = locations.find({})
		if users.count() == 0 or Locations.count() == 0:
			CurrentUser = 'Please Log In'
			startLocation = 'Please Enter Location'
			stopLocation = 'Please Enter Destination'
		else:
			CurrentUser = user.find()[0]['user']
			startLocation = locations.find()[0]['start']
			stopLocation = locations.find()[0]['stop']
		return render_template('locationForm.html',user = CurrentUser, start = startLocation, stop = stopLocation)
	elif request.method == 'POST':
		response = request.form['txtPlaces']
		locations.remove({})
		location = {
			'start': response,
			'stop': 'placeholder',
		}
		locations.insert_one(location)
		return redirect('/page')

# Set the users destination
@app.route('/destination',methods=['GET','POST'])
def destination():
	if request.method == 'GET':
		users = user.find({})
		Locations = locations.find({})
		if users.count() == 0 or Locations.count() == 0:
			CurrentUser = 'Please Log In'
			startLocation = 'Please Enter Location'
			stopLocation = 'Please Enter Destination'
		else:
			CurrentUser = user.find()[0]['user']
			startLocation = locations.find()[0]['start']
			stopLocation = locations.find()[0]['stop']
		return render_template('destinationForm.html',user = CurrentUser, start = startLocation, stop = stopLocation)
	elif request.method == 'POST':
		destination = request.form['txtPlaces']
		locations.update({'stop': 'placeholder'}, {'$set': { "stop" : destination}})
		return redirect('/page')

# Creating an account
@app.route('/inputUser/',methods=['GET','POST'])
def inputUser():
	if request.method == 'GET':
		return render_template('userCreation.html', form = userForm())
	elif request.method == 'POST':
		try:
			form = userForm()
			if form.validate_on_submit():
				userName = form.userName.data
				password = form.password.data
				sql = "INSERT INTO `User` (`username`, `password`) VALUES (%s, %s)"
				cursor = connection.cursor()
				cursor.execute(sql, (userName, password))
				connection.commit()
				return redirect('/login')
			else: 
				flash('incorrect credentials')
				return redirect('/inputUser')
		except:
			flash('incorrect credentials')
			return redirect('/inputUser')

#Log out of current account
@app.route('/logout', methods=['GET','POST'])
def logout():
	if request.method == 'GET':
		user.remove({})
		locations.remove({})
		tweets.remove({})
		return redirect('/login')

#login to the site
@app.route('/login/', methods=['GET','POST'])
def login():
	if request.method == 'GET':
		return render_template('login.html', form = userForm(), user = 'Please Log In')
	if request.method == 'POST':
		try:
			form = userForm()
			if form.validate_on_submit():
				userName = form.userName.data
				password = form.password.data
				cursor = connection.cursor()
				sql = "SELECT * FROM User WHERE username=%s"
				cursor.execute(sql, userName)
				print(cursor)
				data = cursor.fetchone()
				if 'greg' == userName and 'greg' == password:
					user.remove({})
					tweets.remove({})
					locations.remove({})
					Trends.remove({})
					currentUser = {
						'user': userName
					}
					user.insert_one(currentUser)
					return redirect('/page')
				else:
					flash('incorrect credentials')
					return redirect('/login')
			else:
				flash('incorrect credentials')
				return redirect('/login')
		except:
			flash('incorrect credentials')
			return redirect('/login')

# Get Trends on Twitter based on users start location
def getTrends():
	users = user.find({})
	Locations = locations.find({})
	if users.count() == 0 or Locations.count() == 0:
			CurrentUser = 'Please Log In'
			startLocation = 'Please Enter Location'
			stopLocation = 'Please Enter Destination'
			lat = '0'
			lang = '0'
	else:
		CurrentUser = user.find()[0]['user']
		startLocation = locations.find()[0]['start']
		stopLocation = locations.find()[0]['stop']
		geocode_result = gmaps.geocode(startLocation)
		lat = geocode_result[0]['geometry']['location']['lat']
		lang = geocode_result[0]['geometry']['location']['lng']
	twitterAPITest.trendsByPlace(lat,lang)

# Get Popular Tweets based on the users start location
def getTweets():
	users = user.find({})
	Locations = locations.find({})
	if users.count() == 0 or Locations.count() == 0:
			CurrentUser = 'Please Log In'
			startLocation = 'Please Enter Location'
			stopLocation = 'Please Enter Destination'
			lat = '0'
			lang = '0'
	else:
		CurrentUser = user.find()[0]['user']
		startLocation = locations.find()[0]['start']
		stopLocation = locations.find()[0]['stop']
		geocode_result = gmaps.geocode(startLocation)
		lat = geocode_result[0]['geometry']['location']['lat']
		lang = geocode_result[0]['geometry']['location']['lng']
	twitterAPITest.getTweets(lat,lang)

# Display all collected Tweets to the site
@app.route('/tweets/', methods=['GET','POST'])
def displayTweets():
	getTweets()
	getTrends()
	if request.method == 'GET':
		tweet = tweets.find()
		trend = Trends.find()
		if tweet.count() == 0 or trend.count() == 0:
			TWEETS = '0'
			TRENDS = '0'
		else:
			TWEETS = tweet
			TRENDS = trend
		return render_template('viewTweets.html', tweets = TWEETS, trends = TRENDS)


if __name__ == '__main__':
	app.run(host='cs2s.yorkdc.net', port=5018,debug=True)
	# host='cs2s.yorkdc.net', port=5018
