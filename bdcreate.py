import pandas as pd
import os
import django
 
os.environ.setdefault("DJANGO_SETTINGS_MODULE", "gameshop.settings")
django.setup()
from shop.models import Game, Genre, Developer  
df = pd.read_csv('C:\\Users\\Nikota\\Desktop\\Prog\\diplom\\steam.csv')
os.environ["DJANGO_ALLOW_ASYNC_UNSAFE"] = "true"

for i,row in df.iterrows():
    if not Developer.objects.filter(name=row['developer']).exists():
        Developer.objects.create(name=row['developer'])

    for gen in row['genres'].split(';'):
        if not Genre.objects.filter(name=gen).exists():
            Genre.objects.create(name=gen)
    dev = Developer.objects.filter(name=row['developer']).first()
    genre = []
    for gen in row['genres'].split(';'):
        genre.append(Genre.objects.filter(name=gen).first())
    if not Game.objects.filter(name=row['name']).exists():
        game = Game.objects.create(name=row['name'], developer=dev, release_date=row['release_date'], price=row['price'])
        for gen in genre:
            game.genre.add(gen)

