

from django.contrib import admin
from .models import (
    Profile,
Address,
Book,Author,Publisher,Genre, BookReview,BookRate,Factor,PurchaseInvoice,StoreHouse)
# Register your models here.
admin.site.register(Book)
admin.site.register(Author)
# admin.site.register(Customer)

admin.site.register(BookRate)
admin.site.register(Publisher)
admin.site.register(Genre)

admin.site.register(Address)




class PurchaseInvoiceAdmin(admin.ModelAdmin):
    list_display=('book_id','factorCode','date','single_cost','quantity','total_cost')
admin.site.register(PurchaseInvoice,PurchaseInvoiceAdmin)

class FactorAdmin(admin.ModelAdmin):
    list_display=('customer','code','createDate','timeOfDeliveringToThePost',
                  'address','addressDetail','TotalCost','postCost','TotalCostWithPost','verified','successfulPayment','deliveredToTheCustomer','deliveredToThePost')
admin.site.register(Factor,FactorAdmin)


class StoreHouseAdmin(admin.ModelAdmin):
    list_display=('book_id','amount')
admin.site.register(StoreHouse,StoreHouseAdmin)

class ProfileAdmin(admin.ModelAdmin):
    list_display=('id','dob','first_name','last_name','sex','Address')
admin.site.register(Profile,ProfileAdmin)

class ReviewAdmin(admin.ModelAdmin):
    list_display=('id','customer','content','date','username')
admin.site.register(BookReview,ReviewAdmin)