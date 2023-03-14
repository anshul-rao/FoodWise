from flask import request
from flask_restx import Namespace, Resource, fields
from models import FoodInventory
from flask_jwt_extended import jwt_required

inventoryNS = Namespace('inventory', description="A namespace for Inventory")

# Inventory Model Serializer
foodinvModel = inventoryNS.model("Food Inventory", {
    "id": fields.Integer(),
    "name": fields.String(),
    "quantity": fields.Integer(),
    "expiry_date": fields.Date()
}
)

@inventoryNS.route('/hello')
class HelloResource(Resource):
    def get(self):
        return {"message": "Hello World!"}

@inventoryNS.route('/inventory')
class FoodInventoryList(Resource):
    @inventoryNS.marshal_list_with(foodinvModel)
    def get(self):
        """Returns a list of all FoodInventory objects"""
        return FoodInventory.query.all()

    @inventoryNS.expect(foodinvModel)
    @inventoryNS.marshal_with(foodinvModel, code=201)
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


@inventoryNS.route("/inventory/<int:item_id>")
class FoodInventoryItem(Resource):
    @inventoryNS.marshal_with(foodinvModel)
    def get(self, item_id):
        """Returns a specific FoodInventory object by ID"""
        item = FoodInventory.query.get_or_404(
            item_id)  # Queries item_id and returns 404 if item isn't found
        return item

    @inventoryNS.expect(foodinvModel)
    @inventoryNS.marshal_with(foodinvModel)
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

    @inventoryNS.marshal_with(foodinvModel)
    @jwt_required()
    def delete(self, item_id):
        """Deletes a specific FoodInventory object by ID"""
        itemToDelete = FoodInventory.query.get_or_404(
            item_id)  # Queries item_id and returns 404 if item isn't found
        itemToDelete.delete()
        # HTTP status code 204 indicates deletion was successful
        return itemToDelete, 204
        # return {"message": "Item deleted successfully"}, 204