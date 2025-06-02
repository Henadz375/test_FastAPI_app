from typing import Annotated

from fastapi import APIRouter, Depends, status, HTTPException
from slugify import slugify
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.orm import Session
from sqlalchemy import select, insert, delete, update

from app.models import Product, Category
from app.schemas.product_schema import ProductIn, ProductInBase
from app.backend.db_depends import get_session

router = APIRouter(prefix='/products', tags=['products'])


async def get_prod(session: AsyncSession, slug: str) -> Product:
    product = await session.scalar(select(Product).where(Product.slug == slug))

    if not product:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail='There is no product found')
    return product


@router.get('/', response_model=list[ProductInBase])
async def get_all_products(session: Annotated[AsyncSession, Depends(get_session)]):
    all_products = await session.execute(select(Product).where(Product.is_active == True, Product.stock > 0))
    all_products = all_products.unique().scalars().all()

    if not all_products:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail='There are no products')
    return all_products


@router.get('/category/{category_slug}')
async def product_by_category(category_slug: str, session: Annotated[AsyncSession, Depends(get_session)]):
    category_obj = await session.scalar(select(Category).where(Category.slug == category_slug))

    if not category_obj:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND)

    under_category = await session.execute(select(Category).where(Category.parent_id == category_obj.id))

    products_id = [category_obj.id] + [el.id for el in under_category.scalars().all()]

    products_by_category = await session.execute(
        select(Product).where(Product.category_id.in_(products_id), Product.is_active == True, Product.stock > 0))

    return products_by_category.scalars().all()


@router.get('/{product_slug}')
async def product_detail(product_slug: str, session: Annotated[AsyncSession, Depends(get_session)]):
    return await get_prod(session, product_slug)


@router.post('/', status_code=status.HTTP_201_CREATED)
async def create_product(product: ProductIn, session: Annotated[AsyncSession, Depends(get_session)]):
    await session.execute(insert(Product).values(name=product.name,
                                                 description=product.description,
                                                 price=product.price,
                                                 image_url=product.image_url,
                                                 stock=product.stock,
                                                 category_id=product.category,
                                                 slug=slugify(product.name)))
    await session.commit()
    return {'status_code': status.HTTP_201_CREATED, 'transaction': 'Successful'}


@router.put('/{product_slug}')
async def update_product(product_slug: str, product: ProductIn, session: Annotated[AsyncSession, Depends(get_session)]):
    prod = await get_prod(session, product_slug)

    await session.execute(update(Product).values(name=product.name,
                                                 description=product.description,
                                                 price=product.price,
                                                 image_url=product.image_url,
                                                 stock=product.stock,
                                                 category_id=product.category,
                                                 slug=slugify(product.name)).where(Product.id == prod.id))
    await session.commit()

    return {'status_code': status.HTTP_200_OK, 'transaction': 'Product update is successful'}


@router.delete('/{product_slug}')
async def delete_product(product_slug: str, session: Annotated[AsyncSession, Depends(get_session)]):
    prod = await get_prod(session, product_slug)

    await session.execute(delete(Product).where(Product.id == prod.id))
    await session.commit()
    return {'status_code': status.HTTP_200_OK, 'transaction': 'Product delete is successful'}
