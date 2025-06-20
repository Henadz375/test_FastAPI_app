from sqlalchemy.orm import Mapped, relationship, mapped_column
from sqlalchemy import Integer, String, ForeignKey, Float, Boolean
from app.backend.db import Base
from app.models import Category


class Product(Base):
    __tablename__ = 'products'
    id: Mapped[int] = mapped_column(Integer(), primary_key=True, index=True)
    name: Mapped[str] = mapped_column(String())
    slug: Mapped[str] = mapped_column(String(), unique=True, index=True)
    description: Mapped[str] = mapped_column(String())
    price: Mapped[int] = mapped_column(Integer())
    image_url: Mapped[str] = mapped_column(String())
    stock: Mapped[int] = mapped_column(Integer())
    category_id: Mapped[int] = mapped_column(ForeignKey('categories.id'))
    rating: Mapped[float] = mapped_column(Float(), default=0.0)
    is_active: Mapped[bool] = mapped_column(Boolean(), default=True)


    category: Mapped['Category'] = relationship(
        'Category',
        back_populates='products',
        uselist=False,
        lazy='joined'
    )
