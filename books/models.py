from __future__ import unicode_literals
from django.db.models.fields.related import ManyToManyField, ForeignKey
from django.db import models
from django.contrib.auth.models import User


# Create your models here.
class Author(models.Model):
    AID = models.AutoField(primary_key=True)
    AName = models.CharField(max_length = 50, db_index = True)
    ABirthdate = models.DateField(null = True)
    ANationality = models.CharField(max_length = 30)
    ABrief = models.TextField(max_length = 300, null = True, blank = True)
    class Meta:
        db_table = 'author'

class Book(models.Model):
    BISBN = models.CharField(primary_key=True, max_length = 30)
    BTitle = models.CharField(max_length= 40, db_index = True)
    AID = models.ForeignKey(Author)
    BPublisher = models.CharField(max_length = 20)
    BPrice = models.DecimalField(max_digits=6, decimal_places=2)
    BBrief = models.TextField(max_length = 300, null = True, blank = True)
    class Meta:
        db_table = 'book'
# Create your models here.
class Tag(models.Model):
    TID = models.AutoField(primary_key = True)
    Ttype = models.CharField(max_length = 10, unique = True)
    Books = models.ManyToManyField(Book)
    class Meta:
        db_table = 'tag'
class Remark(models.Model):
    RID = models.AutoField(primary_key = True)
    RTitle = models.CharField(max_length = 40)
    RContent = models.TextField(max_length = 2000)
    RDate = models.DateField()
    BID = models.ForeignKey(Book)
    UID = models.ForeignKey(User)
    class Meta:
        db_table = 'remark'

class Favorite(models.Model):
    FID = models.AutoField(primary_key = True)
    UID = models.ForeignKey(User, unique = True)
    class Meta:
        db_table = 'favorite'
class AddBook(models.Model):
    FID = models.ForeignKey(Favorite)
    BID = models.ForeignKey(Book)
    class Meta:
        db_table = 'add_book'
        unique_together = ("FID", "BID")
class Group(models.Model):
    GID = models.AutoField(primary_key = True)
    GBuilder = models.ForeignKey(User)
    GBuildDate = models.DateField()
    GName = models.CharField(max_length = 20, db_index = True)
    class Meta:
        db_table = 'group'
class Join(models.Model):
    GID = models.ForeignKey(Group)
    UID = models.ForeignKey(User)
    class Meta:
        db_table = 'join'
        unique_together = ("GID", "UID")
class Article(models.Model):
    ATID = models.AutoField(primary_key = True)
    ATTitle = models.CharField(max_length = 40)
    ATContent = models.TextField(max_length = 2000)
    ATDate = models.DateField()
    UID = models.ForeignKey(User)
    GID = models.ForeignKey(Group)
    class Meta:
        db_table = 'article'