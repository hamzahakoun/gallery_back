from django.contrib import admin
from .models import *


admin.site.register([User, Image,Tag])
# Register your models here.
