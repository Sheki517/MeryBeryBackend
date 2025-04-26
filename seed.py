from faker import Faker
from app import create_app
from models import db, User, Farm, Variety, Inventory
import random

app = create_app()
fake = Faker()

# How many of each to create
NUM_USERS = 20
NUM_FARMS = 5
NUM_VARIETIES = 15
NUM_INVENTORY_ITEMS = 30

FLOWERS = [
        "Rose", "Tulip", "Daisy", "Sunflower", "Lily",
        "Orchid", "Marigold", "Lavender", "Peony", "Chrysanthemum",
        "Begonia", "Camellia", "Carnation", "Gardenia", "Hibiscus"
]

USER_LOCATIONS = [
    "Paris", "London", "Berlin", "Rome", "Madrid",
    "New York", "Los Angeles", "Chicago", "Boston", "San Francisco"
]

FARM_LOCATIONS = [
    "Nairobi", "Mombasa", "Kisumu", "Nakuru", "Eldoret",
    "Thika", "Naivasha", "Malindi", "Machakos", "Kericho"
]


with app.app_context():
    # Create fake users
    for _ in range(NUM_USERS):
        user = User(
            firebase_id=fake.uuid4(),
            email=fake.unique.email(),
            name=fake.name(),
            location=random.choice(USER_LOCATIONS),
            phone_number=fake.numerify(text="###-###-####")
        )
        db.session.add(user)

    # Create fake farms
    farms = []
    for _ in range(NUM_FARMS):
        farm = Farm(
            name=fake.company() + " " + "Farms",
            email=fake.unique.company_email(),
            phone_number=fake.numerify(text="###-###-####"),
            location=random.choice(FARM_LOCATIONS)
        )
        farms.append(farm)
        db.session.add(farm)

    # Create fake varieties    
    varieties = []
    for flower_name in random.sample(FLOWERS, NUM_VARIETIES):
        variety = Variety(name=flower_name)
        varieties.append(variety)
        db.session.add(variety)


    db.session.commit()

    # Add some inventory
    for _ in range(NUM_INVENTORY_ITEMS):
        farm = random.choice(farms)
        variety = random.choice(varieties)
        # Make sure no duplicates (you already have a UniqueConstraint on farm_id + variety_id)
        if not Inventory.get_by_farm_and_variety(farm.id, variety.id):
            item = Inventory(
                farm_id=farm.id,
                variety_id=variety.id,
                price=round(random.uniform(1, 10), 2),
                count=random.randint(1, 100)
            )
            db.session.add(item)

    db.session.commit()

print('✅ Database seeded successfully!')