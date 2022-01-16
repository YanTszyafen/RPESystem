from django.contrib import admin
from home.models import AdsCategory, Ad, Comment, RPESModel
# Register your models here.
admin.site.register(AdsCategory)
admin.site.register(Ad)
admin.site.register(Comment)
admin.site.register(RPESModel)
