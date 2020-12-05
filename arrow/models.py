from django.db import models


class User(models.Model):
    First_Name = models.CharField(max_length=100)
    Last_Name = models.CharField(max_length=100)
    Email = models.EmailField()
    Contact = models.CharField(max_length=10)

    class Meta:
        db_table = "User"

    def __str__(self):
        return self.First_Name + ' ' + self.Last_Name


class Product(models.Model):
    User = models.ForeignKey(User, on_delete=models.CASCADE, related_name="products", null=True, blank=True)
    Product_Category = models.CharField(max_length=50)
    Product_Name = models.CharField(max_length=50)

    class Meta:
        db_table = "product"
