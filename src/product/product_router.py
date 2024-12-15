from fastapi import APIRouter, Depends, HTTPException, Request, Form
from sqlalchemy.orm import Session
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select
from fastapi.responses import HTMLResponse
from fastapi.templating import Jinja2Templates
from fastapi.staticfiles import StaticFiles

from .product_models import Products
from .product_shema import ProductCreate, ProductPydantic
from ..db import get_session


app = APIRouter(prefix="/products", tags=["Products"])

templates = Jinja2Templates(directory="src/product/templates")


# #добавление продукта
# @app.post("/")
# def create_product(product_create: ProductCreate, session: Session = Depends(get_session)):
#     product = Products(name=product_create.name, price=product_create.price, description=product_create.description)
#     session.add(product)
#     session.commit()
#     session.refresh(product)
#     return  product


@app.get("/", response_model=ProductPydantic, response_class=HTMLResponse)
async def list_products(request: Request, session: AsyncSession = Depends(get_session)):
    products = await session.scalars(select(Products))
    products = products.all()
    context = {
        "request": request,
        "title": "Товары нашей компании",
        "products": products
    }
    return templates.TemplateResponse("index.html", context=context)
    

@app.get("/product-add", response_class=HTMLResponse)
async def add_product(request: Request):
    context = {
    "request": request,
    "title": "Добавление продукта"
    }
    return templates.TemplateResponse("productadd.html", context=context)

@app.post("/product-add", response_class=HTMLResponse)
async def add_product(request: Request, session: AsyncSession = Depends(get_session)):
    form = await request.form()
    form_data = form._dict
    price = int(form_data["price"])
    product = Products(name=form_data["name"], price=price, description=form_data["description"])
    
    try:
        session.add(product)
        await session.commit()
        context = {
            "request": request,
            "title": "Продукт успешно добавлен",
            "message": "Продукт был успешно добавлен."
        }
        return templates.TemplateResponse("productadd.html", context=context)
    except Exception as e:
        print(f"Error saving product to the database: {e}")
        context = {
            "request": request,
            "title": "Ошибка при добавлении продукта",
            "error_message": "Произошла ошибка при добавлении продукта. Попробуйте снова позже."
        }
        return templates.TemplateResponse("productadd.html", context=context)
    # form = await request.form()
    # form_data = form._dict
    # product = Products(**form_data)
    # session.add(product)
    # await session.commit()
    # context = {
    #     "request": request,
    #     "title": "Добавление продукта"
    # }
    # return templates.TemplateResponse("productadd.html", context=context)

@app.get("/", response_model=ProductPydantic, response_class=HTMLResponse)
async def list_products(request: Request, session: AsyncSession = Depends(get_session)):
    products = await session.scalars(select(Products))
    products = products.all()
    context = {
        "request": request,
        "title": "Товары нашей компании",
        "products": products
    }
    return templates.TemplateResponse("index.html", context=context)
    
@app.post("/delete-product/{id}", response_class=HTMLResponse)
async def delete_product_post(id: int, request: Request, session: AsyncSession = Depends(get_session)):
    product = await session.scalar(select(Products).filter(Products.id == id))
    session.delete(product)
    await session.commit()
    context = {
        "request": request,
        "title": "Удаление продукта"
    }
    return templates.TemplateResponse("productdel.html", context=context)

@app.get("/delete-product/{id}", response_class=HTMLResponse)
async def delete_product_get(id: int, request: Request, session: AsyncSession = Depends(get_session)):
    product = await session.scalar(select(Products).filter(Products.id == id))
    name = product.name
    price = product.price
    description = product.description
    context = {
        "request": request,
        "title": "Удаление продукта",
        "name": name,
        "price": price,
        "description": description
    }
    return templates.TemplateResponse("productdel.html", context=context)

@app.get("/product-add/{id}", response_model=ProductPydantic, response_class=HTMLResponse)
async def get_balance(request: Request, id: int, session: AsyncSession = Depends(get_session)):
    product= await session.scalar(select(Products).filter(Products.id == id))
    name = product.name
    price = product.price
    description = product.description
    context = {
        "request": request,
        "title": "Каталог товаров",
        "id": id,
        "name": name,
        "price": price,
        "description": description
    }
    return templates.TemplateResponse("product_id.html", context=context)