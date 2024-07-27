import re
import pandas as pd
from .models import Fastener, Seller
from . import db
from sqlalchemy.exc import IntegrityError


def read_name_and_df(filename):
    # The dtype and na_filter arguments were found to help due to pandas treating the
    # string 'None' as a proxy for Nan (in pandas dtype), or None (in python types).
    seller_inventory_df = pd.read_csv(filename, dtype=str, na_filter=False)

    # This regex captures the part between 'seller-' and the next '-' as a group.
    seller_name_match = re.search(r"seller-(\w+)-", filename)

    seller_name = (
        seller_name_match.group(1) if seller_name_match else "Default-sellerName"
    )

    return seller_name, seller_inventory_df


def row_to_model_A(row, seller):
    row_dict = row.to_dict()

    fastener = Fastener(
        **{
            "category": row_dict.get("category", "Default-category"),
            "thread_size": row_dict.get("thread_size", "Default-thread_size"),
            "material": row_dict.get("material", "Default-material"),
            "finish": row_dict.get("finish", "Default-finish"),
            "seller": seller,
            "external_sku": row_dict.get("product_id", "Default-external_sku"),
            "description": row_dict.get("description"),
            "quantity": row_dict.get("quantity"),
            "price": row_dict.get("price"),
        }
    )
    return fastener


def row_to_model_B(row, seller):
    row_dict = row.to_dict()

    fastener = Fastener(
        **{
            "category": row_dict.get("product_category", "Default-category"),
            "thread_size": row_dict.get("threading", "Default-thread_size"),
            "material": row_dict.get("composition", "Default-material"),
            "finish": row_dict.get("surface_treatment", "Default-finish"),
            "seller": seller,
            "external_sku": row_dict.get("item_number"),
            "description": row_dict.get("description"),
            "quantity": row_dict.get("quantity"),
            "price": row_dict.get("price"),
        }
    )
    return fastener


def df_to_model_list(df, seller):
    # Naive implementation to handle different sellers
    if seller.name == "a":
        return df.apply(row_to_model_A, axis=1, seller=seller).to_list()
    elif seller.name == "b":
        return df.apply(row_to_model_B, axis=1, seller=seller).to_list()
    else:
        return []


def ingest_file(filename):
    name, df = read_name_and_df(filename)

    db.create_all()
    if not Seller.query.filter_by(name=name).first():
        seller = Seller(name=name)
        db.session.add(seller)
        db.session.commit()
    else:
        seller = Seller.query.filter_by(name=name).first()
    fasteners = df_to_model_list(df, seller)
    for i, fastener in enumerate(fasteners):
        print(i)
        try:
            db.session.add(fastener)
            db.session.commit()
        except IntegrityError:
            db.session.rollback()
            existing_fastener = Fastener.query.filter_by(
                seller=seller, external_sku=fastener.external_sku
            ).first()
            existing_fastener.update_fields(fastener)
            db.session.add(existing_fastener)
            db.session.commit()
