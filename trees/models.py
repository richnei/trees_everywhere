from django.db import models
from django.contrib.auth.models import User
from decimal import Decimal

class Account(models.Model):
    name = models.CharField(max_length=100)
    created = models.DateTimeField(auto_now_add=True)
    active = models.BooleanField(default=True)
    users = models.ManyToManyField(User, related_name='accounts')

    def __str__(self):
        return self.name


class Tree(models.Model):
    name = models.CharField(max_length=100)
    scientific_name = models.CharField(max_length=150)

    def __str__(self):
        return self.name


class PlantedTree(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='planted_trees')
    tree = models.ForeignKey(Tree, on_delete=models.CASCADE)
    account = models.ForeignKey(Account, on_delete=models.CASCADE)
    age = models.IntegerField()
    planted_at = models.DateTimeField(auto_now_add=True)
    location_lat = models.DecimalField(max_digits=9, decimal_places=6)
    location_lon = models.DecimalField(max_digits=9, decimal_places=6)

    def __str__(self):
        return f"{self.tree.name} by {self.user.username}"


class Profile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE, related_name='profile')
    about = models.TextField()
    joined = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.user.username

def plant_tree(self, tree, location, account, age=0):
    return PlantedTree.objects.create(
        user=self,
        tree=tree,
        account=account,
        age=age,
        location_lat=location[0],
        location_lon=location[1]
    )

def plant_trees(self, plants):
    planted = []
    for tree, lat, lon, account, age in plants:
        planted.append(
            self.plant_tree(tree, (lat, lon), account, age)
        )
    return planted

User.add_to_class("plant_tree", plant_tree)
User.add_to_class("plant_trees", plant_trees)
