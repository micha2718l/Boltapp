from . import create_app, db
from .models import Fastener, Seller

app = create_app()

if __name__ == "__main__":
    print("Running app")
    with app.app_context():
        db.create_all()  # Create tables
        # Sample data for testing
        if not Seller.query.first():
            sellers = [
                Seller(name="A"),
                Seller(name="B"),
            ]
            db.session.add_all(sellers)
            db.session.commit()
        else:
            sellers = Seller.query.all()
        if not Fastener.query.first():
            fasteners = [
                Fastener(
                    category="Bolt",
                    thread_size=10,
                    material="Steel",
                    finish="Zinc",
                    seller=sellers[0],
                ),
                Fastener(
                    category="Screw",
                    thread_size=10,
                    material="Steel",
                    finish="Zinc",
                    seller=sellers[0],
                ),
                Fastener(
                    category="Nut",
                    thread_size=10,
                    material="Steel",
                    finish="Zinc",
                    seller=sellers[1],
                ),
                Fastener(
                    category="Washer",
                    thread_size=10,
                    material="Steel",
                    finish="Zinc",
                    seller=sellers[1],
                ),
            ]
            db.session.add_all(fasteners)
            db.session.commit()

    app.run(debug=True)
