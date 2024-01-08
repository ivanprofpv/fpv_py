import random
from .factories import UserFactory, CategoryFactory

def seed_users(num_users):
    for _ in range(num_users):
        UserFactory.create()

def seed_categories(num_categories):
    for _ in range(num_categories):
        CategoryFactory.create()

def seed_data():
    seed_users(10)
    seed_categories(5)