from django.db import models
from django.contrib.auth.models import User

# Create your models here.


class UserProfile(models.Model):
    """
    User Profile model
    This model extends the user model provided by django auth
    """

    # explicitly set default manager
    objects = models.Manager()
    # one sentence description about the user
    description = models.CharField(max_length=255, null=True)
    # when the user profile was created
    created_on = models.DateTimeField(auto_now_add=True)
    # when the user profile was last updated
    updated_on = models.DateTimeField(auto_now=True)
    # one to one field to the User model in django auth
    user = models.OneToOneField(User, on_delete=models.CASCADE)


class ShoppingList(models.Model):
    """
    Shopping List model
    """
    # explicitly set default manager
    objects = models.Manager()
    # shopping list name
    name = models.CharField(max_length=255)
    # short description about the list
    description = models.CharField(max_length=255, null=True)
    # when the shopping list was created
    created_on = models.DateTimeField(auto_now_add=True)
    # when the shopping list was last updated
    updated_on = models.DateTimeField(auto_now=True)
    # owner of the list
    user = models.ForeignKey(User, on_delete=models.CASCADE)


class Item(models.Model):
    """
    Shopping List Items model
    """
    # explicitly set default manager
    objects = models.Manager()
    # shopping list item name
    name = models.CharField(max_length=255)
    # short description about the item
    description = models.CharField(max_length=255, null=True)
    # bought status - bool field to indicate if or not bought
    bought = models.BooleanField(default=False)
    # when the item was added
    created_on = models.DateTimeField(auto_now_add=True)
    # when the item was last updated
    updated_on = models.DateTimeField(auto_now=True)
    # list the item belongs to
    the_list = models.ForeignKey(ShoppingList, on_delete=models.CASCADE)
