from models import Hero, Power, hero_powers
from random import choice
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker

# Define the database connection
DATABASE_URI = 'sqlite:///db/app.db'
engine = create_engine(DATABASE_URI)

# Create a session to interact with the database
Session = sessionmaker(bind=engine)
session = Session()

print("🦸‍♀️ Seeding powers...")
powers_data = [
    {"name": "super strength", "description": "gives the wielder super-human strengths"},
    {"name": "flight", "description": "gives the wielder the ability to fly through the skies at supersonic speed"},
    {"name": "super human senses", "description": "allows the wielder to use her senses at a super-human level"},
    {"name": "elasticity", "description": "can stretch the human body to extreme lengths"}
]

# Seed powers
powers = [Power(**power_data) for power_data in powers_data]
session.add_all(powers)
session.commit()
print("🦸‍♀️ Seeding powers complete!")

print("🦸‍♀️ Seeding heroes...")
heroes_data = [
    {"name": "Kamala Khan", "super_name": "Ms. Marvel"},
    {"name": "Doreen Green", "super_name": "Squirrel Girl"},
    {"name": "Gwen Stacy", "super_name": "Spider-Gwen"},
    {"name": "Janet Van Dyne", "super_name": "The Wasp"},
    {"name": "Wanda Maximoff", "super_name": "Scarlet Witch"},
    {"name": "Carol Danvers", "super_name": "Captain Marvel"},
    {"name": "Jean Grey", "super_name": "Dark Phoenix"},
    {"name": "Ororo Munroe", "super_name": "Storm"},
    {"name": "Kitty Pryde", "super_name": "Shadowcat"},
    {"name": "Elektra Natchios", "super_name": "Elektra"}
]

# Seed heroes
heroes = [Hero(**hero_data) for hero_data in heroes_data]
session.add_all(heroes)
session.commit()
print("🦸‍♀️ Seeding heroes complete!")

print("🦸‍♀️ Adding powers to heroes...")

strengths = ["Strong", "Weak", "Average"]
heroes = session.query(Hero).all()

for hero in heroes:
    for _ in range(1, 4):  # Add up to 3 random powers to each hero
        power = session.query(Power).order_by(Power.id).first()
        hero.powers.append(power)
        hero.strengths.append(choice(strengths))
        session.commit()

print("🦸‍♀️ Done seeding!")

# Close the database session
session.close()
