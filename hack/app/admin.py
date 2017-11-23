from django.contrib import admin
from models import Farmer, LendTractor, BorrowTractor, Location, Crop
admin.site.register(Farmer)
admin.site.register(LendTractor)
admin.site.register(BorrowTractor)
admin.site.register(Location)
admin.site.register(Crop)

# Register your models here.
