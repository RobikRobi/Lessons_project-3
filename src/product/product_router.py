from fastapi import APIRouter, Depends, HTTPException, Request
from sqlalchemy.orm import Session
from sqlalchemy import select
from fastapi.responses import HTMLResponse
from fastapi.templating import Jinja2Templates

from .product_models import Products
from .product_shema import ProductCreate, ProductPydantic
from ..db import get_session


app = APIRouter(prefix="/products", tags=["Products"])

templates = Jinja2Templates(directory="src/product/templates")

# #добавление продукта
@app.post("/")
def create_product(product_create: ProductCreate, session: Session = Depends(get_session)):
    product = Products(name=product_create.name, price=product_create.price, description=product_create.description)
    session.add(product)
    session.commit()
    session.refresh(product)
    return  product


@app.get("/", response_model=ProductPydantic, response_class=HTMLResponse)
def list_products(request: Request, session: Session = Depends(get_session)):
    products = session.scalars(select(Products))
    products = products.all()
    product_id = products.id
    context = {
        "request": request,
        "titel": "Продукты",
        "products": products,
        "id": product_id
    }
    return templates.TemplateResponse("index.html", context=context)
    


@app.get("/{id}", response_model=ProductPydantic, response_class=HTMLResponse)
def get_balance(request: Request, id: int, session: Session = Depends(get_session)):
    product= session.scalar(select(Products).filter(Products.id == id))
    name = product.name
    price = product.price
    description = product.description
    context = {
        "request": request,
        "titel": "Продукты",
        "name": name,
        "price": price,
        "description": description
    }
    return templates.TemplateResponse("product_id.html", context=context)