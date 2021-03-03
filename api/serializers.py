from rest_framework import serializers
from .models import (
                    Address,
                    Profile,
                    Book,
                    Author,
                    BookReview,
                    BookRate,
                    Factor,
                    PurchaseInvoice,
                    StoreHouse,
                    Publisher,
                    Genre)
from django.contrib.auth.models import User
from rest_framework.authtoken.models import Token
class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model=User
        fields=('id','username','password','first_name','last_name','email')
        extra_kwargs={'password':{'write_only':True,'required':True}}
    # we have to override tha create
    # method because the 'write_only' and 
    # 'required' will store the password as
    # a normal field and will not hashed
   
    # it will hash the password and create user 
    def create(self,validated_data):
        user=User.objects.create_user(**validated_data)
        
        
        # it will create token automatically for each user
        token=Token.objects.create(user=user)
        return user


class ProfileSerializer(serializers.ModelSerializer):
    address=serializers.ListField(source='Address',required=False,allow_null=True)
    class Meta:
        model=Profile
        fields=('id','user','first_name','last_name','address','sex','dob') 

class AddressSerializer(serializers.ModelSerializer):
    
    class Meta:
        model=Address  
        fields=('id','customer','city','state','name','first_name','last_name','detail','postalCode','phoneNumber','staticNumber')           




class BookSerializer(serializers.ModelSerializer):
    class Meta:
        model=Book
        fields=('id','isbn','image','available_amount_to_order','lessThanFive')
        # exclude=['Fa_title','En_title','Fa_authors','En_authors']

class BookEnSerializer(serializers.ModelSerializer):
    title=serializers.CharField(source='En_title')
    summary=serializers.CharField(source='EnSummary')
    author=serializers.ListField(source='En_authors')
    image = serializers.ImageField(
            max_length=None, use_url=True
        )
    class Meta:
        model=Book
        fields=('id','title','author','summary','isbn','image','price','publication_date','available','available_amount_to_order','lessThanFive','no_of_ratings','avg_ratings','listOfReviews')

class BookFaSerializer(serializers.ModelSerializer):
    title=serializers.CharField(source='Fa_title')
    summary=serializers.CharField(source='FaSummary')
    author=serializers.ListField(source='Fa_authors')
    image = serializers.ImageField(
            max_length=None, use_url=True
        )
    class Meta:
        model=Book
        fields=('id','title','author','summary','isbn','image','price','publication_date','available','available_amount_to_order','lessThanFive','no_of_ratings','avg_ratings','listOfReviews')
        # exclude=['Fa_title','En_title']
    
 
 
 
 
    
class AuthorSerializer(serializers.ModelSerializer):
    class Meta:
        model=Author
        exclude=['Fa_first_name','En_first_name','Fa_last_name','En_last_name']

class AuthorEnSerializer(serializers.ModelSerializer):
    first_name=serializers.CharField(source='En_first_name')
    last_name=serializers.CharField(source='En_last_name')
    listOfBooks=serializers.CharField(source='EnlistOfBooks')
    
    class Meta:
        model=Author
        fields=('id','first_name','sex','last_name','listOfBooks')

class AuthorFaSerializer(serializers.ModelSerializer):
    first_name=serializers.CharField(source='Fa_first_name')
    last_name=serializers.CharField(source='Fa_last_name')
    listOfBooks=serializers.CharField(source='FalistOfBooks')
    
    class Meta:
        model=Author
        fields=('id','first_name','last_name','sex','listOfBooks')
    
class GenreSerializer(serializers.ModelSerializer):
    class Meta:
        model=Genre
        exclude=['Fa_genre_name','En_genre_name']

class GenreEnSerializer(serializers.ModelSerializer):
    name=serializers.CharField(source='En_genre_name')
    listOfBooks=serializers.CharField(source='EnlistOfBooks')
    
    class Meta:
        model=Genre
        fields=('id','name','listOfBooks')

class GenreFaSerializer(serializers.ModelSerializer):
    name=serializers.CharField(source='Fa_genre_name')
    listOfBooks=serializers.CharField(source='FalistOfBooks')
    
    class Meta:
        model=Genre
        fields=('id','name','listOfBooks')
# //////////////////////////////////////////////////////
class PublisherSerializer(serializers.ModelSerializer):
    class Meta:
        model=Publisher
        exclude=['Fa_name','En_name']

class PublisherEnSerializer(serializers.ModelSerializer):
    name=serializers.CharField(source='En_name')
    listOfBooks=serializers.CharField(source='EnlistOfBooks')
    
    class Meta:
        model=Publisher
        fields=('id','name','listOfBooks')

class PublisherFaSerializer(serializers.ModelSerializer):
    name=serializers.CharField(source='Fa_name')
    listOfBooks=serializers.CharField(source='FalistOfBooks')
    
    class Meta:
        model=Publisher
        fields=('id','name','listOfBooks')
# ///////////////////////////////////////////////////////

   
# class CustomerSerializer(serializers.ModelSerializer):
#     class Meta:
#         model=Customer
#         fields=('id','user')
        
class BookReviewSerializer(serializers.ModelSerializer):
    class Meta:
        model=BookReview
        fields=('id','book_id','customer','content','date','username')

class BookRateSerializer(serializers.ModelSerializer):
    class Meta:
        model=BookRate
        fields=('id','book_id','customer','date','stars')

class FactorSerializer(serializers.ModelSerializer):
    class Meta:
        model=Factor
        fields=('id','code','customer','createDate','addressDetail','verified','successfulPayment','deliveredToTheCustomer','deliveredToThePost','postCost','TotalCost','TotalCostWithPost')
        
        
class PurchaseInvoiceSerializer(serializers.ModelSerializer):
    class Meta:
        model=PurchaseInvoice
        fields=('id','book_id','factorCode','EnBookName','FaBookName','customer','date','quantity','single_cost','total_cost')
        
class StoreHouseSerializer(serializers.ModelSerializer):
    class Meta:
        model=StoreHouse
        fields=('id','book_id','date','amount')
        