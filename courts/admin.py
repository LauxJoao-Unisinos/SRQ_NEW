from django.contrib import admin
from .models import Court, OpeningHour, Block
admin.site.register(Court)
admin.site.register(OpeningHour)
admin.site.register(Block)
