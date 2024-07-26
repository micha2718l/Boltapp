from flask import Blueprint, request, jsonify
from .models import Fastener, Seller

main = Blueprint("main", __name__)


@main.route("/fasteners", methods=["GET"])
def get_fasteners():
    sort_by = request.args.get("sort_by", "id")
    order = request.args.get("order", "asc")

    if order == "desc":
        fasteners = Fastener.query.order_by(getattr(Fastener, sort_by).desc()).all()
    else:
        fasteners = Fastener.query.order_by(getattr(Fastener, sort_by).asc()).all()

    return jsonify([fastener.to_dict() for fastener in fasteners])


@main.route("/sellers", methods=["GET"])
def get_sellers():
    sort_by = request.args.get("sort_by", "id")
    order = request.args.get("order", "asc")

    if order == "desc":
        sellers = Seller.query.order_by(getattr(Seller, sort_by).desc()).all()
    else:
        sellers = Seller.query.order_by(getattr(Seller, sort_by).asc()).all()

    return jsonify([seller.to_dict() for seller in sellers])


@main.route("/test/", methods=["GET"])
def test():
    return "Hello, World!"
