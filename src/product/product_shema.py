from pydantic import BaseModel, ConfigDict

# схема для создания продукта
class ProductCreate(BaseModel):
    name: str
    price: int
    description: str

class ProductPydantic(BaseModel):
    id: int
    name: str
    price: int
    description: str

    model_config = ConfigDict(from_attributes=True, use_enum_values=True)

    