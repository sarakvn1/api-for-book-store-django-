
from django.urls import path , include
from rest_framework import routers
from .views import (
                    BookViewSet,
                    ProfileViewSet,
                    BookRateViewSet,
                    UserViewSet,
                    BookReviewViewSet,
                    AuthorViewSet,
                    FactorViewSet,
                    PurchaseInvoiceViewSet,
                    StoreHouseViewSet,
                    PublisherViewSet,
                    GenreViewSet,
                    AddressViewSet
                    )
router=routers.DefaultRouter()
router.register('books',BookViewSet)
router.register('authors',AuthorViewSet)
router.register('bookreviews',BookReviewViewSet)
router.register('bookrating',BookRateViewSet)
router.register('users',UserViewSet)
router.register('factors',FactorViewSet)
router.register('purchaseInvoice',PurchaseInvoiceViewSet)
router.register('storehouse',StoreHouseViewSet)
router.register('genres',GenreViewSet)
router.register('publishers',PublisherViewSet)
router.register('address',AddressViewSet)
router.register('profiles',ProfileViewSet)



urlpatterns = [
  
    path('',include(router.urls)),]
   




