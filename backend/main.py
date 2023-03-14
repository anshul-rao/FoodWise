from flask import Flask, jsonify, request
from flask_restx import Api, Resource, fields
from config import DevConfig
from models import FoodInventory, User
from exts import db
from flask_migrate import Migrate
from werkzeug.security import generate_password_hash, check_password_hash
from flask_jwt_extended import JWTManager, create_access_token, create_refresh_token, jwt_required

# Decorator Meanings
# marshal_with(): Takes data obj and applies field filtering.
    # Takes in a data obj and displays it in an simpler format such as JSON
# expect(): Defines an expected input format for the request

app = Flask(__name__)
app.config.from_object(DevConfig)

db.init_app(app)

migrate = Migrate(app, db)
JWTManager(app)

api = Api(app, doc='/docs')

# Inventory Model Serializer
foodinvModel = api.model("Food Inventory", {
    "id": fields.Integer(),
    "name": fields.String(),
    "quantity": fields.Integer(),
    "expiry_date": fields.Date()
}
)

registerModel = api.model("Register", {
    "username": fields.String(),
    "email": fields.String(),
    "password": fields.String()
})

loginModel = api.model("Login", {
    "username": fields.String(),
    "password": fields.String()
})


@api.route('/hello')
class HelloResource(Resource):
    def get(self):
        return {"message": "Hello World!"}
    
@api.route('/register')
class Register(Resource):
    @api.expect(registerModel)
    def post(self):
        data = request.get_json()

        username = data.get('username')

        dbUser = User.query.filter_by(username=username).first()
        if dbUser is not None:
            return jsonify({"message":f"User with username {username} already exists."})
        
        newUser = User(
            username = data.get('username'),
            email = data.get('email'),
            password = generate_password_hash(data.get('password'))
        )

        newUser.save()

        return jsonify({"message": "User created successfully!"})

@api.route('/login')
class Login(Resource):
    @api.expect(loginModel)
    def post(self):
        data = request.get_json()

        username = data.get('username')
        password = data.get('password')

        dbUser = User.query.filter_by(username=username).first()

        if dbUser and check_password_hash(dbUser.password, password):
            accessToken = create_access_token(identity=dbUser.username)
            refreshToken = create_refresh_token(identity=dbUser.username)

            return jsonify({
                "accessToken": accessToken, "refreshToken": refreshToken
                })
        pass


@api.route('/inventory')
class FoodInventoryList(Resource):
    @api.marshal_list_with(foodinvModel)
    def get(self):
        """Returns a list of all FoodInventory objects"""
        return FoodInventory.query.all()

    @api.expect(foodinvModel)
    @api.marshal_with(foodinvModel, code=201)
    @jwt_required()
    def post(self):
        """Add a new FoodInventory object to database"""
        data = request.get_json()

        newItem = FoodInventory(
            id=data.get('id'),
            name=data.get('name'),
            quantity=data.get('quantity'),
            expiry_date=data.get('expiry_date')
        )

        newItem.save()

        return newItem, 201
    
        # item = request.json["id"]
        # name = request.json["name"]
        # quantity = request.json["quantity"]
        # expiry_date = request.json["expiry_date"]
        # item = FoodInventory(name=name, quantity=quantity, expiry_date=expiry_date)
        # db.session.add(item)
        # db.session.commit()
        # return item, 201 # HTTP status code 201 indicates item creation was successful


@api.route("/inventory/<int:item_id>")
class FoodInventoryItem(Resource):
    @api.marshal_with(foodinvModel)
    def get(self, item_id):
        """Returns a specific FoodInventory object by ID"""
        item = FoodInventory.query.get_or_404(
            item_id)  # Queries item_id and returns 404 if item isn't found
        return item

    @api.expect(foodinvModel)
    @api.marshal_with(foodinvModel)
    @jwt_required()
    def put(self, item_id):
        """Updates a specific FoodInventory object by ID"""
        itemToUpdate = FoodInventory.query.get_or_404(
            item_id)  # Queries item_id and returns 404 if item isn't found
        
        data=request.get_json()
        itemToUpdate.update(data.get('name'), data.get('quantity'), data.get('expiry_date'))

        # item.name = request.json.get("name", item.name)
        # item.quantity = request.json.get("quantity", item.quantity)
        # item.expiry_date = request.json.get("expiry_date", item.expiry_date)
        # db.session.commit()
        return itemToUpdate

    @api.marshal_with(foodinvModel)
    @jwt_required()
    def delete(self, item_id):
        """Deletes a specific FoodInventory object by ID"""
        itemToDelete = FoodInventory.query.get_or_404(
            item_id)  # Queries item_id and returns 404 if item isn't found
        itemToDelete.delete()
        # HTTP status code 204 indicates deletion was successful
        return itemToDelete, 204
        # return {"message": "Item deleted successfully"}, 204


@app.shell_context_processor
def makeShellContext():
    return {
        "db": db,
        "Food Inventory": FoodInventory
    }


if __name__ == '__main__':
    app.run()