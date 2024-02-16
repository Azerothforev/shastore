from typing import Annotated, TYPE_CHECKING

from sqlalchemy import ForeignKey, String
from sqlalchemy.orm import Mapped, mapped_column
from sqlalchemy.orm import relationship
from mixin import ProductRelationMixin, ProductUserFkMixin

from database import Base

if TYPE_CHECKING:
    from auth.models import User

idpk = Annotated[int, mapped_column(primary_key=True, index=True)]
stin = Annotated[int, mapped_column(default=0)]


class Color(ProductRelationMixin, Base):
    __tablename__ = "color"
    product_back_populates = 'color'
    id: Mapped[idpk]
    name: Mapped[str]


class State(ProductRelationMixin, Base):
    __tablename__ = "state"
    product_back_populates = 'state'
    id: Mapped[idpk]
    name: Mapped[str]


class Category(ProductRelationMixin, Base):
    __tablename__ = "category"
    product_back_populates = 'category'
    id: Mapped[idpk]
    name: Mapped[str]


class Brand(ProductRelationMixin, Base):
    __tablename__ = "brand"
    product_back_populates = 'brand'
    id: Mapped[idpk]
    name: Mapped[str]


class Product(Base):
    __tablename__ = "product"
    id: Mapped[idpk]
    price: Mapped[int]
    description: Mapped[str] = mapped_column(
        String(400)
    )
    interest: Mapped[stin]
    status: Mapped[stin]
    information: Mapped[str] = mapped_column(
        String(256), unique=True
    )
    seller_id: Mapped[int] = mapped_column(
        ForeignKey("user.id")
    )
    brand_id: Mapped[int] = mapped_column(
        ForeignKey("brand.id")
    )
    category_id: Mapped[int] = mapped_column(
        ForeignKey("category.id")
    )
    state_id: Mapped[int] = mapped_column(
        ForeignKey("state.id")
    )
    color_id: Mapped[int] = mapped_column(
        ForeignKey("color.id")
    )

    seller: Mapped["User"] = relationship(
        back_populates="products"
    )
    brand: Mapped["Brand"] = relationship(
        back_populates="products"
    )
    state: Mapped["State"] = relationship(
        back_populates="products"
    )
    color: Mapped["Color"] = relationship(
        back_populates="products"
    )
    category: Mapped["Category"] = relationship(
        back_populates="products"
    )


class Cart(ProductUserFkMixin, Base):
    __tablename__ = "cart"
    id: Mapped[idpk]


class Favorite(ProductUserFkMixin, Base):
    __tablename__ = "favorite"
    id: Mapped[idpk]
