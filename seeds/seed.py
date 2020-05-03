from app import Assistants, job_titles
from flask_seeder import FlaskSeeder, Seeder, Faker, generator
from random import randint

class DemoSeeder(Seeder):
  # run() will be called by Flask-Seeder
  def run(self):
    # Create a new Faker and tell it how to create User objects
    faker = Faker(
      cls=Assistants,
      init={
        "first_name": generator.Name(),
        "last_name": generator.Name(),
        "username": generator.Name(),
        "profession": job_titles[randint(0, len(job_titles) - 1)],
        "picture": "avatar_temporary.jpg"
      }
    )

    # Create 5 users
    for assist in faker.create(5):
      print(f"Adding user: {assist}")
      self.db.session.add(assist)