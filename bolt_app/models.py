from . import db


class Fastener(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    category = db.Column(db.String(80), nullable=False)
    thread_size = db.Column(db.String(80), nullable=False)
    material = db.Column(db.String(80), nullable=False)
    finish = db.Column(db.String(80), nullable=False)
    seller_id = db.Column(db.Integer, db.ForeignKey("seller.id"), nullable=False)

    def to_dict(self):
        return {
            "id": self.id,
            "category": self.category,
            "thread_size": self.thread_size,
            "material": self.material,
            "finish": self.finish,
            "seller": self.seller.to_dict(),
        }


class Seller(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(80), nullable=False)
    fasteners = db.relationship("Fastener", backref="seller", lazy=True)

    def to_dict(self):
        return {"id": self.id, "name": self.name}
