from django.db import models
from django.contrib.auth.models import (BaseUserManager,
                                        AbstractBaseUser)
from .enums import AdoptionStatus, Gender


class UserManager(BaseUserManager):
    def create_user(self, email, name, mobile=None, password=None, password2=None, gender=None, profile_image=None, address=None):
        """
        Creates and saves a User with the given email, name and password.
        """
        if not email:
            raise ValueError('Users must have an email address')

        user = self.model(
            email=self.normalize_email(email), mobile=mobile,
            name=name,
            gender=gender,
            profile_image=profile_image,
            address=address
        )

        user.set_password(password)
        user.save(using=self._db)
        return user

    def create_superuser(self, email, name, mobile=None, password=None):
        """
        Creates and saves a superuser with the given email, name and password.
        """
        user = self.create_user(
            email,
            password=password,
            mobile=mobile,
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
    gender = models.CharField(max_length=10, null=True,
                              blank=True, choices=Gender.choices())
    address = models.CharField(max_length=100, null=True,
                               blank=True, default="Nepal")
    mobile = models.CharField(max_length=15)
    name = models.CharField(max_length=50)
    profile_image = models.ImageField(
        upload_to="documents/images/profiles", blank=True)
    is_active = models.BooleanField(default=True)
    is_admin = models.BooleanField(default=False)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    objects = UserManager()

    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = ['name', 'mobile']

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
    name = models.CharField(max_length=50, unique=True,
                            error_messages="Category name is unique and required.")
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return f'{self.name}'


class Breed(models.Model):
    name = models.CharField(max_length=50, unique=True,
                            error_messages="Breed name is unique and required.")
    category = models.ForeignKey(Category, on_delete=models.RESTRICT)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return f'{self.name}'


class Animal(models.Model):
    name = models.CharField(max_length=100, default="Ramro Dog")
    posted_by = models.ForeignKey(
        User, on_delete=models.RESTRICT, related_name="posted_by")
    description = models.CharField(default="Dog", max_length=255)
    personality = models.CharField(max_length=100, default="Jumps a lot.")
    likes = models.CharField(max_length=100, default="Tear down the chairs.")
    category = models.ForeignKey(Category, on_delete=models.RESTRICT)
    breed = models.ForeignKey(Breed, on_delete=models.RESTRICT)
    age = models.DecimalField(default=1, decimal_places=3, max_digits=10)
    gender = models.CharField(
        max_length=10, choices=Gender.choices(), default=Gender.MALE)
    image = models.ImageField(upload_to="documents/images/animals", blank=True)
    approve_post = models.BooleanField(default=False)
    adopted = models.BooleanField(default=False)
    popularity = models.IntegerField(blank=True, default=0)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return f'{self.breed.name}:{self.description[:35]}'


class Adoption(models.Model):
    requested_by = models.ForeignKey(
        User, on_delete=models.RESTRICT, related_name="requested_by", blank=True, default=1)
    animal = models.ForeignKey(
        User, on_delete=models.RESTRICT)
    status = models.CharField(max_length=25, choices=AdoptionStatus.choices())
    message = models.TextField(max_length=255, blank=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return f'{self.animal} requested by {self.requested_by}'


class Notification(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    message = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)


class Product(models.Model):
    name = models.CharField(max_length=150)
    description = models.CharField(max_length=255, blank=True)
    image = models.ImageField(
        upload_to="documents/images/products", blank=True)
    category = models.ForeignKey(Category, on_delete=models.RESTRICT)
    price = models.DecimalField(decimal_places=2, max_digits=10)
    stock = models.DecimalField(decimal_places=2, max_digits=10)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return f'{self.name} at Rs. {self.price}'


class ProductWishlist(models.Model):
    user = models.ForeignKey(User, on_delete=models.RESTRICT)
    product = models.ForeignKey(Product, on_delete=models.RESTRICT)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return f'{self.product.name} for {self.user.name}'


class AnimalWishlist(models.Model):
    user = models.ForeignKey(
        User, on_delete=models.RESTRICT, related_name="wishlists")
    animal = models.ForeignKey(
        Animal, on_delete=models.CASCADE)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return f'{self.animal.breed.name}'


class CartSummary(models.Model):
    user = models.ForeignKey(
        User, blank=True, on_delete=models.CASCADE, related_name="carts")
    shipping_address = models.CharField(max_length=255, null=True)
    additional_info = models.CharField(max_length=255, null=True)
    sold = models.BooleanField(default=False)
    reference_id = models.CharField(max_length=20, null=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return f'{len(self.cart_details())} items of Rs. {self.amount()}'

    def cart_details(self):
        return self.details.all()

    def amount(self):
        return sum((item.quantity * item.product.price) for item in self.cart_details())


class ProductCart(models.Model):
    product = models.ForeignKey(
        Product, on_delete=models.RESTRICT, related_name="carts")
    quantity = models.DecimalField(decimal_places=2, max_digits=10)
    rate = models.DecimalField(decimal_places=2, max_digits=10, default=0)
    cart_summary = models.ForeignKey(
        CartSummary, blank=True, null=True, on_delete=models.CASCADE, related_name="details")
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return f'{self.product.name} x {self.quantity}'
