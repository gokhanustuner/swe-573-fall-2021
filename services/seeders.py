from django_seed import Seed
from services.models import Service

seeder = Seed.seeder()
seeder.add_entity(Service, 5)

inserted_pks = seeder.execute()
