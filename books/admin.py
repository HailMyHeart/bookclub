from django.contrib import admin
from models import *
# Register your models here.
@admin.register(Author,Book,Tag,Remark,Favorite,AddBook,Group,Join,Article)
class PersonAdmin(admin.ModelAdmin):
    pass