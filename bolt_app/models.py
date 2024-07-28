from . import db


class Fastener(db.Model):
    __table_args__ = (
        db.UniqueConstraint("seller_id", "external_sku", name="unique_seller_sku"),
    )

    # Primary, neccessary fields
    id = db.Column(db.Integer, primary_key=True)
    category = db.Column(db.String(80), nullable=False)
    thread_size = db.Column(db.String(80), nullable=False)
    material = db.Column(db.String(80), nullable=False)
    finish = db.Column(db.String(80), nullable=False)

    # These two will be used together as a composite key for uniqueness
    seller_id = db.Column(db.Integer, db.ForeignKey("seller.id"), nullable=False)
    external_sku = db.Column(db.String(80), nullable=True)

    # Extra fields
    description = db.Column(db.String(80), nullable=True)
    quantity = db.Column(db.Integer, nullable=True)
    price = db.Column(db.Float, nullable=True)

    date_added = db.Column(db.DateTime, nullable=False, default=db.func.now())

    def update_fields(self, new_fastener):
        for key, value in new_fastener.__dict__.items():
            if key != "_sa_instance_state":
                setattr(self, key, value)

    def to_dict(self):
        return {
            "id": self.id,
            "category": self.category,
            "thread_size": self.thread_size,
            "material": self.material,
            "finish": self.finish,
            "seller": self.seller.to_dict(),
            "external_sku": self.external_sku,
            "description": self.description,
            "quantity": self.quantity,
            "price": self.price,
        }


class Seller(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(80), nullable=False)
    fasteners = db.relationship("Fastener", backref="seller", lazy=True)

    def to_dict(self):
        return {"id": self.id, "name": self.name}
