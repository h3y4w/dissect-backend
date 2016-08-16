from flask import Flask
from flask_restful import Resource, Api, reqparse



























if __name__== "__main__":
    app = Flask(__name__)
    api = Api(app)

    api.run(debug=True)
