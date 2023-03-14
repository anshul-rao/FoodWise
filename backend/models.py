from exts import db
from datetime import datetime, timedelta


class FoodInventory(db.Model):
    id = db.Column(db.Integer(), primary_key=True)
    name = db.Column(db.String(), nullable=False)  # String preset 50
    quantity = db.Column(db.Integer(), nullable=False)
    expiry_date = db.Column(db.String(), nullable=False)
    # user_id = db.Column(db.Integer(), db.ForeignKey('user.id'), nullable=False)

    def __repr__(self):
        return f"<FoodInventory {self.id}: {self.name}>"

    # Setter Methods

    def save(self):
        """
        The save function is used to save the changes made to a model instance.
        It takes in no arguments and returns nothing.
        :param self: Refer to the current instance of the class
        :return: The object that was just saved
        """
        db.session.add(self)
        db.session.commit()
    
    def delete(self):
        """
        The delete function is used to delete a specific row in the database. It takes no parameters and returns nothing.
        :param self: Refer to the current instance of the class, and is used to access variables that belongs to the class
        :return: Nothing
        """
        db.session.delete(self)
        db.session.commit()

    def update(self, name, quantity, expiry_date):
        """
        The update function updates the title and description of a given blog post.
        It takes two parameters, title and description.
        :param self: Access variables that belongs to the class
        :param title: Update the title of the post
        :param description: Update the description of the blog post
        :return: A dictionary with the updated values of title and description
        """
        self.name = name
        self.quantity = quantity
        self.expiry_date = expiry_date

        db.session.commit()

    def addItem(self, name, quantity, expiry_date=None):
        item = FoodInventory(name=name, quantity=quantity,
                             expiryDate=expiry_date)
        db.session.add(item)
        db.session.commit()

    def removeItem(self, name):
        item = FoodInventory.query.filter_by(name=name).first()
        db.session.delete(item)
        db.session.commit()

    def updateItemQuantity(self, name, quantity):
        item = FoodInventory.query.filter_by(name=name).first()
        item.quantity = quantity
        db.session.commit()

    def updateItemExpiryDate(self, name, expiryDate):
        item = FoodInventory.query.filter_by(name=name).first()
        item.expiryDate = expiryDate
        db.session.commit()

    # Getter Methods

    def getItem(self, name):
        item = FoodInventory.query.filter_by(name=name).first()  # ?
        return item

    def getAllItems(self):
        allItems = FoodInventory.query.all()
        return allItems

    def getLowQuantityItems(self, lowThreshold):
        items = FoodInventory.query.filter(
            FoodInventory.quantity <= lowThreshold).all()
        return items

    def getExpriredItems(self):
        now = datetime.utcnow()
        items = FoodInventory.query.filter(
            FoodInventory.expiry_date < now).all()
        return items

    def getCloseExpiryItems(self, days):
        now = datetime.utcnow()
        thresholdDate = now + timedelta(days=days)
        items = FoodInventory.query.filter(FoodInventory.expiry_date >= now,
                                           FoodInventory.expiry_date <= thresholdDate).all()
        return items
