from django.contrib import admin
from .models import *
# Register your models here.
class ListingAdmin(admin.ModelAdmin):
    list_display = ('id', 'title', 'owner', 'price')
    
admin.site.register(User)
admin.site.register(Listing, ListingAdmin)
admin.site.register(Category)
admin.site.register(Bid)
admin.site.register(Comment)
