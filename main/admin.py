from django.contrib import admin
from main.models import (User, Product, Animal, ProductWhislist,
                         ProductSales, AnimalWhislist, Adoption, ProductCart,
                         Breed, Category, CartSummary
                         )
from django.contrib.auth.admin import UserAdmin as BaseUserModelAdmin


class UserModelAdmin(BaseUserModelAdmin):
    # The forms to add and change user instances
    # form = UserChangeForm
    # add_form = UserCreationForm

    # The fields to be used in displaying the User model.
    # These override the definitions on the base UserModelAdmin
    # that reference specific fields on auth.User.
    list_display = ('email', 'name', 'is_admin', 'mobile')
    list_filter = ('is_admin',)
    fieldsets = (
        ('User Credentials', {'fields': ('email', 'password')}),
        ('Personal info', {'fields': ('name', 'mobile')}),
        ('Permissions', {'fields': ('is_admin',)}),
    )
    # add_fieldsets is not a standard ModelAdmin attribute. UserModelAdmin
    # overrides get_fieldsets to use this attribute when creating a user.
    add_fieldsets = (
        (None, {
            'classes': ('wide',),
            'fields': ('email', 'name', 'mobile', 'password1', 'password2'),
        }),
    )
    search_fields = ('email', 'name', 'mobile')
    ordering = ('email', 'id', 'name')
    filter_horizontal = ()


# Now register the new UserModelAdmin...
admin.site.register(User, UserModelAdmin)

# Register your models here.


class ProductModelAdmin(admin.ModelAdmin):
    # The forms to add and change user instances
    # form = UserChangeForm
    # add_form = UserCreationForm

    # The fields to be used in displaying the User model.
    # These override the definitions on the base UserModelAdmin
    # that reference specific fields on auth.User.
    list_display = ('name', 'stock', 'price')
    list_filter = ('name',)
    fieldsets = (
        ('Info', {'fields': ('description', 'name', 'category', 'image')}),
        ('Market', {'fields': ('stock', 'price')})
    )
    # add_fieldsets is not a standard ModelAdmin attribute. UserModelAdmin
    # overrides get_fieldsets to use this attribute when creating a user.
    add_fieldsets = (
        (None, {
            'classes': ('wide',),
            'fields': ('name', 'stock', 'price', 'description', 'category'),
        }),
    )
    search_fields = ('name', 'category')
    ordering = ('name', 'stock', 'category')
    filter_horizontal = ()


admin.site.register(Product, ProductModelAdmin)
admin.site.register(Animal, admin.ModelAdmin)
admin.site.register(AnimalWhislist, admin.ModelAdmin)
admin.site.register(Adoption, admin.ModelAdmin)
admin.site.register(ProductWhislist, admin.ModelAdmin)
admin.site.register(ProductCart, admin.ModelAdmin)
admin.site.register(ProductSales, admin.ModelAdmin)
admin.site.register(Breed, admin.ModelAdmin)
admin.site.register(Category, admin.ModelAdmin)
admin.site.register(CartSummary, admin.ModelAdmin)
