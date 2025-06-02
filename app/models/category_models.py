from sqlalchemy import Integer, String, Boolean, ForeignKey
from sqlalchemy.orm import Mapped, relationship, mapped_column

from app.backend.db import Base



class Category(Base):
    __tablename__ = 'categories'

    id: Mapped[int] = mapped_column(Integer(), primary_key=True, index=True)
    name: Mapped[str] = mapped_column(String())
    slug: Mapped[str] = mapped_column(String(), unique=True, index=True)
    is_active: Mapped[bool] = mapped_column(Boolean(), default=True)
    parent_id: Mapped[int] = mapped_column(ForeignKey('categories.id'), nullable=True)

    products = relationship('Product', back_populates='category', lazy='joined')
