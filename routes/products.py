from fastapi import APIRouter
from fastapi import HTTPException
from schemas.schemas import Product
from schemas.schemas import Category
from database.database import products_db

products_router = APIRouter()


# FastAPI handles JSON serialization and deserialization for us.
# We can simply use built-in python and Pydantic types, in this case dict[int, Item].
@products_router.get("/products")
def index() -> list[Product]:
    return products_db


@products_router.get("/products/{product_id}")
def query_item_by_id(product_id: int) -> Product:
    if product_id not in products_db:
        raise HTTPException(
            status_code=404,
            detail=f"Product with {product_id=} does not exist.")
    return products_db[product_id]


Selection = dict[str, str | int | float | Category | None]


@products_router.get("/products/")
def query_item_by_parameters(
    name: str | None = None,
    min_price: float | None = None,
    max_price: float | None = None,
    category: Category | None = None
) -> dict[str, Selection | list[Product]]:
    def check_item(item: Product) -> bool:
        """  """
        return all(
            (
                name is None or name.lower() in item.name.lower(),
                min_price is None or item.price > min_price,
                max_price is None or item.price < max_price,
                category is None or item.category is category,
            )
        )

    selection = [product for product in products_db if check_item(product)]
    return {
        "query": {"name": name,
                  "min_price": min_price,
                  "max_price": max_price,
                  "category": category},
        "products": selection
    }