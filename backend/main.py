from flask import Flask
from flask_restx import Api, Resource
from config import DevConfig
from models import FoodInventory
from exts import db

app = Flask(__name__)
app.config.from_object(DevConfig)

db.init_app(app)

api = Api(app, doc='/docs')

# foodinvModel = api.model()

@api.route('/hello')
class HelloResource(Resource):
    def get(self):
        return {"message": "Hello World!"}


@app.shell_context_processor
def makeShellContext():
    return {
        "db": db,
        "Food Inventory": FoodInventory
    }


if __name__ == '__main__':
    app.run()
