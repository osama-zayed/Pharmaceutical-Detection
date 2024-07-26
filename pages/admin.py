from django.contrib import admin
from .models import Rating
from .models import Medication
admin.site.register(Rating)
admin.site.register(Medication)