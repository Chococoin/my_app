from flask import Flask
from flask_restful import Resource, Api

app = Flask(__name__)
api = Api(app)

class Index(Resource):
    def get(self):
        return {'resource': 'index', 'status': 'Work in Progress'}

class Kraken_api(Resource):
	def get(self):
		return {'resource': 'Balance'}

api.add_resource(Index, '/')
api.add_resource(Kraken_api, '/api')

if __name__ == '__main__':
    app.run(debug=True)