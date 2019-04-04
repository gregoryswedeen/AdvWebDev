from flask import Flask,jsonify,request,Response
from flaskext.mysql import MySQL

restServer = Flask(__name__)

mysql = MySQL()

restServer.config['MYSQL_DATABASE_USER'] = 'm.odea'
restServer.config['MYSQL_DATABASE_PASSWORD'] = 'xxxxxxxxxx'
restServer.config['MYSQL_DATABASE_DB'] = 'modea'
restServer.config['MYSQL_DATABASE_HOST'] = 'cs2s.yorkdc.net'
restServer.config['MYSQL_DATABASE_PORT'] = 3306
restServer.config['MYSQL_DATABASE_CHARSET'] = 'utf8'
mysql.init_app(restServer)
conn = mysql.connect()
cursor = conn.cursor()


@restServer.after_request
def after_request(response):
	response.headers.add('Access-Control-Allow-Origin', '*')
	response.headers.add('Access-Control-Allow-Headers', 'Content-Type,Authorization')
	response.headers.add('Access-Control-Allow-Methods', 'GET,PUT,POST,DELETE,OPTIONS')
	return response

@restServer.route("/")
def test():
        return "Hello"

@restServer.route("/dbsend", methods=['POST'])
def sendData():
	data = request.form
#	return "Received"
        return jsonify(data)

@restServer.route("/dbget", methods=['GET'])
def getData():
	resultList = []
	cursor.execute("SELECT rider_id FROM riders")
	result = cursor.fetchall()
	for k in result:
		riderslist = {'rider_id' : k[0]}
		resultList.append(riderslist)
	return jsonify(resultList)


if __name__ == '__main__':
        print("== Running in debug mode ==")
        restServer.run(host='cs2s.yorkdc.net', port=5001, debug=True)
