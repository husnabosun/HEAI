import os
import django

os.environ.setdefault("DJANGO_SETTINGS_MODULE", "hackhaton.settings")
django.setup()

from app.views import determine_branch

print(determine_branch("heart attack"))
