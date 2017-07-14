from flask import Flask, render_template, make_response
from flask_restful import Resource, Api
import datetime

app = Flask(__name__)
api = Api(app)

class Index(Resource):
    def get(self):
    	header = {'Content-Type': 'text/html'}
        return make_response(render_template('index.html'),200, header)

class Kraken_api(Resource):
	def get(self):
		return {'resource': 'Balance'}

class Hello(Resource):
	def get(self):
		header = {'Content-Type': 'text/html'}
		now = datetime.datetime.now()
		timeString = now.strftime("%d-%m-%Y %H:%M:%S")
		templateData = {
			'title' : 'HELLO TIME!',
			'time': timeString
			} 
		return make_response(render_template('hello_time.html', **templateData), 200, header)

api.add_resource(Index, '/')
api.add_resource(Kraken_api, '/api')
api.add_resource(Hello, '/hello_time')

if __name__ == '__main__':
    app.run(debug=True)