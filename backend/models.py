from exts import db
from datetime import datetime, timedelta


class FoodInventory(db.Model):
    id = db.Column(db.Integer(), primary_key=True)
    name = db.Column(db.String(), nullable=False)  # String preset 50
    quantity = db.Column(db.Integer(), nullable=False)
    expiry_date = db.Column(db.Date(), nullable=False)
    # user_id = db.Column(db.Integer(), db.ForeignKey('user.id'), nullable=False)

    def __repr__(self):
        return f"<FoodInventory {self.id}: {self.name}>"

    # Setter Methods

    def addItem(self, name, quantity, expiry_date=None):
        if expiry_date:
            expiry_date = datetime.strptime(expiry_date, '%Y-%m-%d')
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
