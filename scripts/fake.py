import random

from faker import Faker
from pydantic import Field, BaseModel

from example.dataset import Supplies, Accessory

faker = Faker()


class Accessory(BaseModel):
    view_widgets: dict = {}
    sort_fields: list = ["name", "rating", "category"]
    id: int = Field(None, description="ID")
    color: str | None = Field(None, description="Color")
    name: str | None = Field(None, description="Name")


def generate_accessory():
    return {
        "id": faker.unique.random_int(min=1, max=1000),
        "color": faker.color_name(),
        "name": faker.word(),
    }


def generate_supply_data():
    accessories_count = random.randint(0, 10)
    accessories = [generate_accessory() for _ in range(accessories_count)]
    accessories = [Accessory(**a).model_dump() for a in accessories]

    return {
        "id": faker.unique.random_int(min=1, max=100000),
        "rating": round(random.uniform(1.0, 5.0), 2),
        "category": random.choice(["books", "other"]),
        "name": faker.catch_phrase(),
        "image": faker.image_url(),
        "slug": faker.slug(),
        "subtitle": faker.sentence(),
        "accessories": accessories,
    }


if __name__ == '__main__':
    data = [generate_supply_data() for i in range(50)]
    supply = Supplies()
    supply.put_raws(data)
    # supply.dump()
