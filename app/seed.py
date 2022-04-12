''' Скрипт добавляет рыбу в БД.'''
import os
from django.core.wsgi import get_wsgi_application
from django_seed import Seed
from qa.models import Question, Answer
from django.contrib.auth.models import User


os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'ask.settings')

application = get_wsgi_application()


seeder = Seed.seeder()

seeder.add_entity(User, 10)
seeder.add_entity(Question, 100)
seeder.add_entity(Answer, 300)
