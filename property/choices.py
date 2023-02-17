from django.db.models import TextChoices
from property.constant import *


class MealPreferenceChoices(TextChoices):
    VEGETARIAN = MEAL_TYPE['VEGETARIAN'], 'Vegetarian'
    NON_VEGETARIAN = MEAL_TYPE['NON-VEGETARIAN'], 'Non-Vegetarian'
    


class DrinkPreferenceChoices(TextChoices):
    ALCOHOLIC = DRINK_TYPE['ALCOHOLIC'], 'Alcoholic'
    non_ALCOHOLIC = DRINK_TYPE['NON-ALCOHOLIC'], 'Non-Alcoholic'
   

class MusicPreferenceChoices(TextChoices):
    LIVE_DJ = MUSIC_TYPE['LIVE-DJ'], 'Live-DJ'
    LIVE_MUSIC = MUSIC_TYPE['LIVE-MUSIC'], 'Live-Music'


