from typing import TYPE_CHECKING
from sqlalchemy import ForeignKey
from sqlalchemy.orm import declared_attr, Mapped, mapped_column, relationship

if TYPE_CHECKING:
    from product.models import Product


class ProductRelationMixin:
    product_back_populates: str

    @declared_attr
    def products(cls) -> Mapped[list['Product']]:
        return relationship(
            "Product",
            back_populates=cls.product_back_populates
        )


class ProductUserFkMixin:

    @declared_attr
    def product_id(cls) -> Mapped[int]:
        return mapped_column(
            ForeignKey(
                "product.id",
                ondelete='CASCADE'
            )
        )

    @declared_attr
    def user_id(cls) -> Mapped[int]:
        return mapped_column(
            ForeignKey(
                "user.id",
                ondelete='CASCADE'
            )
        )


class AccountOrdersMixin:

    @declared_attr
    def product_id(cls) -> Mapped[int]:
        return mapped_column(
            ForeignKey(
                "product.id",
                ondelete='CASCADE'
            )
        )

    @declared_attr
    def seller_id(cls) -> Mapped[int]:
        return mapped_column(
            ForeignKey(
                "user.id",
                ondelete='CASCADE'
            )
        )

    @declared_attr
    def buyer_id(cls) -> Mapped[int]:
        return mapped_column(
            ForeignKey(
                "user.id",
                ondelete='CASCADE'
            )
        )
