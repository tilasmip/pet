from django.db import models
from django.contrib.auth.models import(BaseUserManager,
                                       AbstractBaseUser)

class UserManager(BaseUserManager):
    def create_user(self, email, name, password=None, password2 = None):
        """
        Creates and saves a User with the given email, name and password.
        """
        if not email:
            raise ValueError('Users must have an email address')

        user = self.model(
            email=self.normalize_email(email),
            name=name,
        )

        user.set_password(password)
        user.save(using=self._db)
        return user

    def create_superuser(self, email, name, password=None):
        """
        Creates and saves a superuser with the given email, name and password.
        """
        user = self.create_user(
            email,
            password=password,
            name=name,
        )
        user.is_admin = True
        user.save(using=self._db)
        return user

class User(AbstractBaseUser):
    email = models.EmailField(
        verbose_name='Email',
        max_length=255,
        unique=True,
    )
    name = models.CharField(max_length=50)
    profile_image = models.ImageField(upload_to="documents/images/profiles",blank=True)
    is_active = models.BooleanField(default=True)
    is_admin = models.BooleanField(default=False)
    created_at = models.DateTimeField(auto_now_add= True)
    updated_at = models.DateTimeField(auto_now=True)

    objects = UserManager()

    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = ['name']

    def __str__(self):
        return self.email

    def has_perm(self, perm, obj=None):
        "Does the user have a specific permission?"
        # Simplest possible answer: Yes, always
        return True

    def has_module_perms(self, app_label):
        "Does the user have permissions to view the app `app_label`?"
        # Simplest possible answer: Yes, always
        return True

    @property
    def is_staff(self):
        "Is the user a member of staff?"
        # Simplest possible answer: All admins are staff
        return self.is_admin
    
class Category(models.Model):
    name = models.CharField(max_length = 50, unique=True,error_messages="Category name is unique and required.")
    created_at = models.DateTimeField(auto_now_add= True)
    updated_at = models.DateTimeField(auto_now =True)
    
    def __str__(self):
        return f'{self.name}'

class Breed(models.Model):
    name = models.CharField(max_length= 50, unique= True,error_messages="Breed name is unique and required.")
    category = models.ForeignKey(Category,on_delete = models.RESTRICT)
    created_at = models.DateTimeField(auto_now_add= True)
    updated_at = models.DateTimeField(auto_now =True)

    def __str__(self):
        return f'{self.name}'

class Animal(models.Model):
    description = models.CharField(default = "Dog", max_length = 255)
    category = models.ForeignKey(Category, on_delete=models.RESTRICT)
    breed = models.ForeignKey(Breed, on_delete = models.RESTRICT)
    image = models.ImageField(upload_to="documents/images/animals",blank=True)
    views = models.IntegerField(blank = True)
    created_at = models.DateTimeField(auto_now_add= True)
    updated_at = models.DateTimeField(auto_now =True)

    def __str__(self):
        return f'{self.breed.name}:{self.description[:35]}'

class Product(models.Model):
    name = models.CharField(max_length = 150)
    description = models.CharField(max_length = 255, blank = True)
    image = models.ImageField(upload_to="documents/images/products",blank=True)
    category = models.ForeignKey(Category, on_delete=models.RESTRICT)
    price = models.DecimalField(decimal_places=2, max_digits=10)
    stock = models.DecimalField(decimal_places=2, max_digits=10)
    created_at = models.DateTimeField(auto_now_add= True)
    updated_at = models.DateTimeField(auto_now =True)

    def __str__(self):
        return f'{self.name} at Rs. {self.price}'

class ProductWhislist(models.Model):
    user = models.ForeignKey(User,on_delete = models.RESTRICT)
    product = models.ForeignKey(Product,on_delete=models.RESTRICT)
    created_at = models.DateTimeField(auto_now_add= True)
    updated_at = models.DateTimeField(auto_now =True)

    def __str__(self):
        return f'{self.product.name} for {self.user.name}'

class AnimalWhislist(models.Model):
    user = models.ForeignKey(User,on_delete = models.RESTRICT)
    animal = models.ForeignKey(Animal,on_delete=models.RESTRICT)
    created_at = models.DateTimeField(auto_now_add= True)
    updated_at = models.DateTimeField(auto_now =True)

    def __str__(self):
        return f'{self.animal.breed.name}'

class ProductCart(models.Model):
    user = models.ForeignKey(User,on_delete = models.RESTRICT)
    product = models.ForeignKey(Product, on_delete= models.RESTRICT)
    quantity = models.DecimalField(decimal_places=2, max_digits=10)
    created_at = models.DateTimeField(auto_now_add= True)
    updated_at = models.DateTimeField(auto_now =True)

    def __str__(self):
        return f'{self.product.name} x {self.quantity}'

class ProductSales(models.Model):
    user = models.ForeignKey(User,on_delete = models.RESTRICT)
    product = models.ForeignKey(Product, on_delete= models.RESTRICT)
    quantity = models.DecimalField(decimal_places=2, max_digits=10)
    cupon_id = models.CharField(max_length= 20)
    amount = models.DecimalField(decimal_places=2, max_digits=10)
    referenceId = models.CharField(max_length = 50)
    created_at = models.DateTimeField(auto_now_add= True)
    updated_at = models.DateTimeField(auto_now =True)

    def __str__(self):
        return f'{self.product.name} at Rs.{self.amount}'


