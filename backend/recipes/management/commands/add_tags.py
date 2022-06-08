"""Модуль загрузки ингредиентов в базу данных"""
import csv
import os

from django.conf import settings
from django.core.management.base import BaseCommand

from recipes.models import Tag

CSV_FILE = os.path.join(settings.BASE_DIR, 'data/tags.csv')


class Command(BaseCommand):
    help = f'Loads sample data from "{CSV_FILE}"'

    def handle(self, *args, **options):
        with open(
            CSV_FILE,
            'r', encoding='utf-8'
        ) as file:
            reader = csv.reader(file, delimiter=',')
            for row in reader:
                name, color, slug = row
                Tag.objects.get_or_create(
                    name=name,
                    color=color,
                    slug=slug
                )
        print('Successfully uploaded!')
