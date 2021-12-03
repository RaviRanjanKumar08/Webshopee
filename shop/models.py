from django.db import models

# Create your models here.
class Customer(models.Model):
    id = models.AutoField(primary_key=True)
    firstname=models.CharField(max_length=50,default="")
    lastname = models.CharField(max_length=50,default="")
    email=models.EmailField(max_length=50)
    phone=models.CharField(max_length=10)
    password=models.CharField(max_length=30)
    

    def __str__(self):
        return self.firstname + " " + self.lastname





class Product(models.Model):
    
    product_id=models.AutoField
    product_name=models.CharField(max_length=200)
    desc=models.CharField(max_length=300)
    pub_date=models.DateField()
    category = models.CharField(max_length=50,default="")
    subcategory = models.CharField(max_length=50, default="")
    price = models.IntegerField(default=0)
    image = models.ImageField(upload_to="shop/images", default="")

    def __str__(self):
        return self.product_name


class Contact(models.Model):
    msg_id = models.AutoField(primary_key=True)
    name = models.CharField(max_length=50)
    email = models.CharField(max_length=70, default="")
    phone = models.CharField(max_length=70, default="")
    desc = models.CharField(max_length=500, default="")


    def __str__(self):
        return self.name

class Order(models.Model):
    # cid=models.ForeignKey(Customer,on_delete=models.CASCADE,default="1")
    order_id = models.AutoField(primary_key=True)
    items_json = models.CharField(max_length=5000)
    name = models.CharField(max_length=90)
    amount = models.IntegerField(default=0)
    email = models.CharField(max_length=111)
    address = models.CharField(max_length=111)
    city = models.CharField(max_length=111)
    state = models.CharField(max_length=111)
    zip_code = models.CharField(max_length=111)
    phone = models.CharField(max_length=111, default="")
    cust_details=models.CharField(max_length=111,default="")
    
    def __str__(self):
        return self.name

class OrderUpdate(models.Model):
    update_id  = models.AutoField(primary_key=True)
    order_id = models.IntegerField(default="")
    update_desc = models.CharField(max_length=5000)
    timestamp = models.DateField(auto_now_add=True)

    def __str__(self):
        return self.update_desc[0:7] + "..."


