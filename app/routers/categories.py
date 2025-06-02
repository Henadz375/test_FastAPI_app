from typing import Annotated

from fastapi import APIRouter, Depends, status, HTTPException
from sqlalchemy import insert, select, delete, update
from sqlalchemy.orm import Session
from slugify import slugify
from sqlalchemy.ext.asyncio import AsyncSession

from app.backend.db_depends import get_session
from app.models.category_models import Category
from app.schemas.category_schema import CategoryIn

router = APIRouter(prefix='/categories', tags=['categories'])


@router.get('/')
async def get_all_categories(session: Annotated[AsyncSession, Depends(get_session)]):
    categories= await session.scalars(select(Category))
    return categories.unique().all()



@router.post('/', status_code=status.HTTP_201_CREATED)
async def create_category(category: CategoryIn, session: Annotated[AsyncSession, Depends(get_session)]):
    await session.execute(insert(Category).values(name=category.name,
                                            parent_id=category.parent_id,
                                            slug=slugify(category.name)))
    await session.commit()
    return {
        'status_code': status.HTTP_201_CREATED,
        'message': 'Successful'
    }


@router.put('/{slug}')
async def update_category(slug: str, category: CategoryIn, session: Annotated[AsyncSession, Depends(get_session)]):
    res = await session.execute(select(Category).where(Category.slug == slug))
    category_in_db=res.scalar()
    if not category_in_db:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail='Category not found')

    category_in_db.name=category.name
    category_in_db.slug=slugify(category.name)
    category_in_db.parent_id=category.parent_id


    await session.commit()
    return {'message': 'Update'}


@router.delete('/{slug}')
async def delete_category(slug: str, session: Annotated[AsyncSession, Depends(get_session)]):
    cat_in_db= await session.scalar(select(Category).where(Category.slug == slug))
    if not cat_in_db:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail='Category not found')

    await session.execute(delete(Category).where(Category.slug == slug))
    await session.commit()
    return {'message': 'Record has been deleted'}
