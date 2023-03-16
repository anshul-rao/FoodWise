from flask import Flask
from flask_restx import Api
from flask_migrate import Migrate
from flask_jwt_extended import JWTManager
from flask_cors import CORS
from models import FoodInventory, User
from inventory import inventoryNS
from auth import authNS
from exts import db

# Decorator Meanings
# marshal_with(): Takes data obj and applies field filtering.
    # Takes in a data obj and displays it in an simpler format such as JSON
# expect(): Defines an expected input format for the request


def createApp(config):
    app = Flask(__name__)
    app.config.from_object(config)

    CORS(app) # Communicates between localhost:3000 and localhost:5000

    db.init_app(app)

    migrate = Migrate(app, db)
    JWTManager(app)

    api = Api(app, doc='/docs')

    api.add_namespace(inventoryNS)
    api.add_namespace(authNS)

    @app.shell_context_processor
    def makeShellContext():
        return {
            "db": db,
            "Food Inventory": FoodInventory,
            "user": User
        }
    
    return app