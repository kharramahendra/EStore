from django.core.checks import messages
from django.db import models
from multiselectfield import MultiSelectField
from django.contrib.auth.models import User

from django.utils.timezone import now

# Create your models here.
# Create your models here.
sizes = ((1,'XS'),
              (2,'S'),
              (3,'M'),
              (4,'L'),
              (5,'XL'),
              (6,'XXL'))

colors = ((1, 'red'),
               (2, 'blue'),
               (3, 'yellow'),
               (4, 'pink'),
               (5, 'black'),
               (6,'white'),
               (7,'green'))
class Product(models.Model):
    product_id = models.AutoField(primary_key=True)
    product_name = models.CharField(max_length=50)
    category = models.CharField(max_length=50, default="")
    price = models.IntegerField(default=0)
    desc = models.CharField(max_length=300, default="")
    pub_date = models.DateField()
    image = models.ImageField(upload_to='shop/images', default="")
    image2 = models.ImageField(upload_to='shop/images', default="")
    image3 = models.ImageField(upload_to='shop/images', default="")
    Sizes = MultiSelectField(choices=sizes)
    colors = MultiSelectField(choices=colors)
    
    def __str__(self):
        return self.product_name

class ProductComment(models.Model):
    sno= models.AutoField(primary_key=True)
    comment=models.TextField()
    user=models.ForeignKey(User, on_delete=models.CASCADE)
    product=models.ForeignKey(Product, on_delete=models.CASCADE)
    timestamp= models.DateTimeField(default=now)

    def __str__(self):
        return self.comment[0:13] + "..." + "by" + " " + self.user.username
    


class Orders(models.Model):
    order_id = models.AutoField(primary_key=True)
    user = models.ForeignKey(User,on_delete=models.CASCADE)
    items_json = models.CharField(max_length=10000)
    amount = models.IntegerField( default=0)
    name = models.CharField(max_length=90)
    address = models.CharField(max_length=111)
    city = models.CharField(max_length=111)
    zip_code = models.CharField(max_length=111)
    phone = models.CharField(max_length=111, default="")

    def __str__(self):
      return self.name


class OrderUpdate(models.Model):
    update_id  = models.AutoField(primary_key=True)
    order_id = models.IntegerField(default="")
    update_desc = models.CharField(max_length=5000)
    timestamp = models.DateField(auto_now_add=True)

    def __str__(self):
        return self.update_desc[0:7] + "..."


class Contact(models.Model):
    co_id  = models.AutoField(primary_key=True)
    email = models.CharField(max_length=500)
    message = models.CharField(max_length=5000)
    timestamp = models.DateField(auto_now_add=True)

    def __str__(self):
        return self.name