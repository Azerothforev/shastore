from sqlalchemy.orm import Mapped
from mixin import AccountOrdersMixin

from database import Base
from product.models import idpk, stin


class Order(AccountOrdersMixin, Base):
    __tablename__ = 'order'
    id: Mapped[idpk]
    status: Mapped[stin]
