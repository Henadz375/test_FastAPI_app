import uvicorn
from fastapi import FastAPI
from app.routers import categories, products

app = FastAPI()

app.include_router(categories.router)
app.include_router(products.router)


@app.get('/')
async def welcome():
    return {'message': 'welcome'}


# if __name__ == '__main__':
#     uvicorn.run('main:app', reload=True)
