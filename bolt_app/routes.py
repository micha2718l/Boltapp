from flask import Blueprint, request, jsonify
from .models import Fastener, Seller

main = Blueprint("main", __name__)


@main.route("/fasteners", methods=["GET"])
def get_fasteners():
    default = {"sort_by": "category", "order": "asc"}

    sort = request.args.get("sort", f"{default['sort_by']}:{default['order']}")
    sort_parts = sort.split(":")

    sort_by = sort_parts[0] if len(sort_parts) > 0 else default["sort_by"]
    if sort_by not in ["category", "thread_size", "material", "finish"]:
        sort_by = default["sort_by"]

    order = sort_parts[1] if len(sort_parts) > 1 else default["order"]
    if order not in ["asc", "desc"]:
        order = default["order"]

    if order == "desc":
        fasteners = Fastener.query.order_by(getattr(Fastener, sort_by).desc()).all()
    else:
        fasteners = Fastener.query.order_by(getattr(Fastener, sort_by).asc()).all()

    return jsonify([fastener.to_dict() for fastener in fasteners])


@main.route("/sellers", methods=["GET"])
def get_sellers():
    # For simplicity, we will always sort by name
    sellers = Seller.query.order_by(getattr(Seller, "name").asc()).all()

    return jsonify([seller.to_dict() for seller in sellers])


@main.route("/test/", methods=["GET"])
def test():
    return "Hello, World!"
