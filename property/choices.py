from django.db.models import TextChoices
from property.constant import *


class MealPreferenceChoices(TextChoices):
    VEGETARIAN = MEAL_TYPE['VEGETARIAN'], 'Vegetarian'
    NON_VEGETARIAN = MEAL_TYPE['NON-VEGETARIAN'], 'Non-Vegetarian'
    BOTH = MEAL_TYPE['BOTH'], 'Both'
    


class DrinkPreferenceChoices(TextChoices):
    ALCOHOLIC = DRINK_TYPE['ALCOHOLIC'], 'Alcoholic'
    non_ALCOHOLIC = DRINK_TYPE['NON-ALCOHOLIC'], 'Non-Alcoholic'
    BOTH = DRINK_TYPE['BOTH'], 'Both'
   

class MusicPreferenceChoices(TextChoices):
    LIVE_DJ = MUSIC_TYPE['LIVE DJ'], 'Live DJ'
    LIVE_MUSIC = MUSIC_TYPE['LIVE MUSIC'], 'Live Music'


class ActionChoices(TextChoices):
    APPROVED = STATUS['APPROVED'],'Approved'
    REJECTED = STATUS['REJECTED'],'Rejected'
    INITIAL = STATUS['INITIAL'],'Initial'
    CANCEL = STATUS['CANCEL'],'Cancel'

