from django.shortcuts import render
from rest_framework.response import Response
from rest_framework import viewsets,status
from django.contrib.auth.models import User
from rest_framework.authentication import TokenAuthentication
from rest_framework.decorators import action
from rest_framework.permissions import IsAuthenticated,AllowAny
import logging
from azbankgateways import bankfactories, models as bank_models, default_settings as settings
from django.http import HttpResponse, Http404
from django.urls import reverse
from django.shortcuts import get_object_or_404
from .serializers import (  
                          AddressSerializer,
                            ProfileSerializer,
                            BookSerializer,
                            BookEnSerializer,
                            BookFaSerializer,
                            BookRateSerializer,
                            UserSerializer,
                            BookReviewSerializer,
                            AuthorSerializer,
                            AuthorEnSerializer,
                            AuthorFaSerializer,
                            FactorSerializer,
                            PurchaseInvoiceSerializer,
                            StoreHouseSerializer,
                            PublisherEnSerializer,
                            PublisherFaSerializer,
                            GenreEnSerializer,
                            GenreFaSerializer)

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
                    Genre,
                    Publisher)
import base64
import random
from rest_framework import generics
from django.db.models import Q
from django.views.generic import  ListView

    




class UserViewSet(viewsets.ModelViewSet):
    """
    A viewset that provides the standard actions
    """
    queryset = User.objects.all()
    serializer_class = UserSerializer
    authentication_classes=(TokenAuthentication,)
    permission_classes=(AllowAny,)
    
    @action(detail=True,methods=['POST'])
    def set_password(self, request, pk=None):
        user = self.get_object()
        serializer = PasswordSerializer(data=request.DATA)
        if serializer.is_valid():
            user.set_password(serializer.data['password'])
            user.save()
            return Response({'status': 'password set'})
        else:
            return Response(serializer.errors,
                            status=status.HTTP_400_BAD_REQUEST)

    @action(detail=True,methods=['POST'])
    def recent_users(self, request):
        recent_users = User.objects.all().order('-last_login')
        page = self.paginate_queryset(recent_users)
        serializer = self.get_pagination_serializer(page)
        return Response(serializer.data)  


class AddressViewSet(viewsets.ModelViewSet):
    queryset=Address.objects.all()
    serializer_class=AddressSerializer
    authentication_classes=(TokenAuthentication,)
    # if you wanted to be available only for login users replace allowany with  isauthenticated
    permission_classes=(AllowAny,)
    
    @action(detail=False,methods=['POST'])
    def all_address(self,request):
        if 'address' in request.data:
            user=request.user
            try: 
                address=Address.objects.filter(customer=user)
                adserializer=AddressSerializer(address,many=True)
                response={'message':'address found','result':1,'address':adserializer.data}
                return Response(response,status=status.HTTP_200_OK)
            except:
                
                response={'message':'sorry nothing found','result':2}
                return Response(response,status=status.HTTP_400_BAD_REQUEST)
            
            
        else:
            response={'message':'this is not working'}
            return Response(response,status=status.HTTP_204_NO_CONTENT)
    
    @action(detail=False,methods=['POST'])
    def new_update(self,request):
        if 'address_name' in request.data:
           
            
            
            # print('user',user.id)
            # print('profile',profile)
            try:
                user=request.user
                # profile=Profile.objects.get(id=user.id)
            
                address_name=request.data['address_name']
                firstName=request.data['first_name']
                lastName=request.data['last_name']
                city=request.data['city']
                state=request.data['state']
                detail=request.data['detail']
            
                postal_code=request.data['postalCode']
                phone_number=request.data['phoneNumber']
                static_number=request.data['staticNumber']
                address=Address.objects.create(customer=user,
                                                  name=address_name,
                                                  first_name=firstName,
                                                  last_name=lastName,
                                                  detail=detail,
                                                  state=state,
                                                  city=city,
                                                  postalCode=postal_code,
                                                  phoneNumber=phone_number
                                                  ,staticNumber=static_number)
                adserializer=AddressSerializer(address,many=False)
                response={'message':'address created','result':1,'address':adserializer.data}
                return Response(response,status=status.HTTP_200_OK)
            except:
                
                response={'message':'sorry','result':2}
                return Response(response,status=status.HTTP_400_BAD_REQUEST)
            
            
        else:
            response={'message':'this is not working'}
            return Response(response,status=status.HTTP_204_NO_CONTENT)
    
class ProfileViewSet(viewsets.ModelViewSet):
    queryset=Profile.objects.all()
    serializer_class=ProfileSerializer
    authentication_classes=(TokenAuthentication,)
    # if you wanted to be available only for login users replace allowany with  isauthenticated
    permission_classes=(AllowAny,)
    
    @action(detail=False,methods=['POST'])
    def get_profile(self,request):
        if 'profile' in request.data:
            user=request.user
            
            try:
                user=User.objects.get(id=user.id)
                profile=Profile.objects.get(user=user)
               
                profileserializer=ProfileSerializer(profile,many=False)
                response={'message':'profile found','result':profileserializer.data}
                return Response(response,status=status.HTTP_200_OK)
            except:
                user=User.objects.get(id=user.id)
                profile=Profile.objects.get(user=user)
               
                profileserializer=ProfileSerializer(profile,many=False)
                response={'message':'profile found','result':profileserializer.data}
                return Response(response,status=status.HTTP_200_OK)
                
        else:
            response={'message':'this is not working'}
            return Response(response,status=status.HTTP_204_NO_CONTENT)
        
    
    
    @action(detail=False,methods=['POST'])
    def create_profile(self,request):
        if 'first_name' in request.data:
            
            userId=request.data['userId']
            first_name=request.data['first_name']
            last_name=request.data['last_name']
            try:
                user=User.objects.get(id=userId)
                profile=Profile.objects.create(first_name=first_name,last_name=last_name,user=user)
               
                profileserializer=ProfileSerializer(profile,many=False)
                response={'message':'profile created','result':profileserializer.data}
                return Response(response,status=status.HTTP_200_OK)
            except:
                user=User.objects.get(id=userId)
                profile=Profile.objects.create(first_name=first_name,last_name=last_name,user=user)
               
                profileserializer=ProfileSerializer(profile,many=False)
                response={'message':'profile created','result':profileserializer.data}
                return Response(response,status=status.HTTP_200_OK)
                
        else:
            response={'message':'this is not working'}
            return Response(response,status=status.HTTP_204_NO_CONTENT)        
    
    def update(self,request,*args,**kwargs):
        response={'message':'you cant update review like that'}
        return Response(response,status=status.HTTP_400_BAD_REQUEST)
    
    def create(self,request,*args,**kwargs):
        response={'message':'you cant create review like that'}
        return Response(response,status=status.HTTP_400_BAD_REQUEST)
    
    
    
    
class BookViewSet(viewsets.ModelViewSet):
    queryset=Book.objects.all()
    authentication_classes=(TokenAuthentication,)
    permission_classes=(AllowAny,)
    
    def get_serializer_class(self):
        if 'Fa' in self.request.META['HTTP_ACCEPT_LANGUAGE']:
                # using 'in' because it can be set to something like 'es-ES; es'
            return BookFaSerializer
        return BookEnSerializer
    
    @action(detail=True,methods=['POST'])
    def write_book_review(self,request,pk=None):
        if 'review_content' in request.data:
            user=request.user
            print("this is id",user.id)
            book=Book.objects.get(id=pk)
            reviewContent=request.data['review_content']
            
            print('user',user.username)
            try:
                bookReview=BookReview.objects.get(customer=user.id,book_id=book.id)
                bookReview.content=reviewContent
               
                bookReview.save()
                brserializer=BookReviewSerializer(bookReview,many=False)
                response={'message':'review updated','result':brserializer.data}
                return Response(response,status=status.HTTP_200_OK)
            except:
                bookReview=BookReview.objects.create(customer=user,book_id=book,content=reviewContent)
                brserializer=BookReviewSerializer(bookReview,many=False)
                response={'message':'review created','result':brserializer.data}
                return Response(response,status=status.HTTP_200_OK)
            
        else:
            response={'message':'this is not working'}
            return Response(response,status=status.HTTP_204_NO_CONTENT)
    
    @action(detail=True,methods=['POST'])
    def rate_book(self,request,pk=None):
        if 'stars' in request.data:
            # print('------------------------')
            book=Book.objects.get(id=pk)
            user=request.user
            stars=request.data['stars']
            print('user',user.username)
            try:
                rateMovie=BookRate.objects.get(customer=user.id,book_id=book.id)
                rateMovie.stars=stars
                rateMovie.save()
                brateserializer=BookRateSerializer(rateMovie,many=False)
                response={'message':'rate updated','result':brateserializer.data}
                return Response(response,status=status.HTTP_200_OK)
            except:
                rateMovie=BookRate.objects.create(customer=user,book_id=book,stars=stars)
                brateserializer=BookRateSerializer(rateMovie,many=False)
                response={'message':'rate created','result':brateserializer.data}
                return Response(response,status=status.HTTP_200_OK)     
        else:
            response={'message':'this is not working'}
            return Response(response,status=status.HTTP_204_NO_CONTENT)
        
        
    @action(detail=False,methods=['POST'])
    def search_book(self,request):
        if 'search' in request.data:
            search=request.data['search']
            if 'Fa' in self.request.META['HTTP_ACCEPT_LANGUAGE']:
                book_list = Book.objects.filter(Q(Fa_title__icontains=search))
                genre_list = Genre.objects.filter(Q(Fa_genre_name__icontains=search))
                publisher_list = Publisher.objects.filter(Q(Fa_name__icontains=search))
                author_list = Author.objects.filter(Q(Fa_first_name__icontains=search) |
                                                    Q(Fa_last_name__icontains=search))
                try:
            
                    bookserializer=BookFaSerializer(book_list,many=True,context={'request': request})
                    genreserializer=GenreFaSerializer(genre_list,many=True,context={'request': request})
                    publisherserializer=PublisherFaSerializer(publisher_list,many=True,context={'request': request})
                    authorserializer=AuthorFaSerializer(author_list,many=True,context={'request': request})
                    response={'message':'success','result':{'genre':genreserializer.data,
                                                            'book':bookserializer.data, 
                                                            'publisher':publisherserializer.data,
                                                            'authors':authorserializer.data}}
                    return Response(response,status=status.HTTP_200_OK)
                except:
                    response={'message':'nothing found'}
                    return Response(response,status=status.HTTP_200_OK)  
            else:
                book_list = Book.objects.filter(Q(En_title__icontains=search))
                genre_list = Genre.objects.filter(Q(En_genre_name__icontains=search))
                publisher_list = Publisher.objects.filter(Q(En_name__icontains=search))
                author_list = Author.objects.filter(Q(En_first_name__icontains=search) |
                                                    Q(En_last_name__icontains=search))
                try:
                    bookserializer=BookEnSerializer(book_list,many=True,context={'request': request})
                    genreserializer=GenreEnSerializer(genre_list,many=True,context={'request': request})
                    publisherserializer=PublisherEnSerializer(publisher_list,many=True,context={'request': request})
                    authorserializer=AuthorEnSerializer(author_list,many=True,context={'request': request})
                    response={'message':'success','result':{'book':bookserializer.data,
                                                                 'genre':genreserializer.data,
                                                                 'publisher':publisherserializer.data,
                                                                 'authors':authorserializer.data}}
                    return Response(response,status=status.HTTP_200_OK)
                except:  
                    response={'message':'nothing found'}
                    return Response(response,status=status.HTTP_200_OK)    
        else:
            response={'message':'this is not working'}
            return Response(response,status=status.HTTP_204_NO_CONTENT)
        
    @action(detail=False,methods=['POST'])
    def homePage(self,request):
            if 'Fa' in self.request.META['HTTP_ACCEPT_LANGUAGE']:
                book_list = Book.objects.all()
                randomBook=random.sample(list(book_list), 10)
               
                
                try:
            
                    bookserializer=BookFaSerializer(randomBook,many=True,context={'request': request})
                    
                    response={'message':'success','book':bookserializer.data}
                    return Response(response,status=status.HTTP_200_OK)
                except:
                    response={'message':'nothing found'}
                    return Response(response,status=status.HTTP_200_OK)  
            else:
                book_list = Book.objects.all()
                randomBook=random.sample(list(book_list),10)
                try:
                    bookserializer=BookEnSerializer(randomBook,many=True,context={'request': request})
                    
                    response={'message':'success', 'book':bookserializer.data}
                    return Response(response,status=status.HTTP_200_OK)
                except:  
                    response={'message':'nothing found'}
                    return Response(response,status=status.HTTP_200_OK)    
        
    # @action(detail=True,methods=['POST'])
    # def author_name(self,request,pk=None):
    #     response={'author':'this is authors names'}
    #     return Response(response,status=status.HTTP_200_OK)
    
    # @action(detail=True,methods=['POST'])
    # def author_name(self,request,pk=None):
    #     if 'author' in request.data:
    #         print('------------------------')
    #         book=Book.objects.get(id=pk)
    #         user=request.user
    #         # user=User.objects.get(id=1)
    #         print('user',user.username)
    #         print('------------------------')
    #         print(book.title ,"is  my favorite book")
    #         response={'author':'this is authors names'}
    #         return Response(response,status=status.HTTP_200_OK)
    #     else:
    #         response={'message':'this is not working'}  
    #         return Response(response,status=status.HTTP_204_NO_CONTENT)

class AuthorViewSet(viewsets.ModelViewSet):
    queryset=Author.objects.all()
    # serializer_class=AuthorSerializer
    authentication_classes=(TokenAuthentication,)
    permission_classes=(AllowAny,)
    def get_serializer_class(self):
        if 'Fa' in self.request.META['HTTP_ACCEPT_LANGUAGE']:
                # using 'in' because it can be set to something like 'es-ES; es'
            return AuthorFaSerializer
        return AuthorEnSerializer
    
    
    @action(detail=False,methods=['POST'])
    def bookList(self,request):
        if 'authorId' in request.data:
            authorId=request.data['authorId']
            books=Book.objects.filter(authors_id=authorId)
            if 'Fa' in self.request.META['HTTP_ACCEPT_LANGUAGE']:
                try:    
                    bookserializer=BookFaSerializer(books ,many=True, context={'request': request})    
                    response={'book':bookserializer.data}
                    return Response(response,status=status.HTTP_200_OK)
                except:
                    bookserializer=BookFaSerializer(books,many=Truecontext,  context={'request': request})    
                    response={'book':bookserializer.data}
                    return Response(response,status=status.HTTP_200_OK)
            else:
                try:    
                    bookserializer=BookEnSerializer(books,many=True,context={'request': request})    
                    response={'book':bookserializer.data}
                    return Response(response,status=status.HTTP_200_OK)
                except:
                    bookserializer=BookEnSerializer(books,many=True,context={'request': request})    
                    response={'book':bookserializer.data}
                    return Response(response,status=status.HTTP_200_OK)
        else:
            response={'message':'this is not working'}
            return Response(response,status=status.HTTP_204_NO_CONTENT)   
        

class GenreViewSet(viewsets.ModelViewSet):
    queryset=Genre.objects.all()
    # serializer_class=AuthorSerializer
    authentication_classes=(TokenAuthentication,)
    permission_classes=(AllowAny,)
    def get_serializer_class(self):
        if 'Fa' in self.request.META['HTTP_ACCEPT_LANGUAGE']:
                # using 'in' because it can be set to something like 'es-ES; es'
            return GenreFaSerializer
        return GenreEnSerializer
    
    @action(detail=False,methods=['POST'])
    def bookList(self,request):
        if 'genreId' in request.data:
            genreId=request.data['genreId']
            books=Book.objects.filter(genre=genreId)
            if 'Fa' in self.request.META['HTTP_ACCEPT_LANGUAGE']:
                try:    
                    bookserializer=BookFaSerializer(books,many=True,context={'request': request})    
                    response={'message':'this is working','book':bookserializer.data}
                    return Response(response,status=status.HTTP_200_OK)
                except:
                    bookserializer=BookFaSerializer(books,many=True,context={'request': request})    
                    response={'message':'this is working','book':bookserializer.data}
                    return Response(response,status=status.HTTP_200_OK)
            else:
                try:    
                    bookserializer=BookEnSerializer(books,many=True,context={'request': request})    
                    response={'message':'this is working','book':bookserializer.data}
                    return Response(response,status=status.HTTP_200_OK)
                except:
                    bookserializer=BookEnSerializer(books,many=True,context={'request': request})    
                    response={'message':'this is working','book':bookserializer.data}
                    return Response(response,status=status.HTTP_200_OK)
        else:
            response={'message':'this is not working'}
            return Response(response,status=status.HTTP_204_NO_CONTENT)   
        
    
    
class PublisherViewSet(viewsets.ModelViewSet):
    queryset=Publisher.objects.all()
    # serializer_class=AuthorSerializer
    authentication_classes=(TokenAuthentication,)
    permission_classes=(AllowAny,)
    def get_serializer_class(self):
        if 'Fa' in self.request.META['HTTP_ACCEPT_LANGUAGE']:
                # using 'in' because it can be set to something like 'es-ES; es'
            return PublisherFaSerializer
        return PublisherEnSerializer
    
    @action(detail=False,methods=['POST'])
    def bookList(self,request):
        if 'publisherId' in request.data:
            publisherId=request.data['publisherId']
            books=Book.objects.filter(publisher=publisherId)
            if 'Fa' in self.request.META['HTTP_ACCEPT_LANGUAGE']:
                try:    
                    bookserializer=BookFaSerializer(books,many=True,context={'request': request})    
                    response={'message':'this is working','book':bookserializer.data}
                    return Response(response,status=status.HTTP_200_OK)
                except:
                    bookserializer=BookFaSerializer(books,many=True,context={'request': request})    
                    response={'message':'this is working','book':bookserializer.data}
                    return Response(response,status=status.HTTP_200_OK)
            else:
                try:    
                    bookserializer=BookEnSerializer(books,many=True,context={'request': request})    
                    response={'message':'this is working','book':bookserializer.data}
                    return Response(response,status=status.HTTP_200_OK)
                except:
                    bookserializer=BookEnSerializer(books,many=True,context={'request': request})    
                    response={'message':'this is working','book':bookserializer.data}
                    return Response(response,status=status.HTTP_200_OK)
        else:
            response={'message':'this is not working'}
            return Response(response,status=status.HTTP_204_NO_CONTENT)   
        
    
# class CustomerViewSet(viewsets.ModelViewSet):
#     queryset=Customer.objects.all()
#     serializer_class=CustomerSerializer
#     authentication_classes=(TokenAuthentication,)
    
class BookReviewViewSet(viewsets.ModelViewSet):
    queryset=BookReview.objects.all()
    serializer_class=BookReviewSerializer
    authentication_classes=(TokenAuthentication,)
    permission_classes=(AllowAny,)
    
    @action(detail=False,methods=['POST'])
    def reviewList(self,request):
        if 'bookId' in request.data:
            bookId=request.data['bookId']
            reviews=BookReview.objects.filter(book_id=bookId)
            reviewL=[]
            try:    
                brevieweserializer=BookReviewSerializer(reviews,many=True)    
                response={'message':'this is working','result':brevieweserializer.data}
                return Response(response,status=status.HTTP_200_OK)
            except:
                brevieweserializer=BookReviewSerializer(reviews,many=True)      
                response={'message':'this is working','result':brevieweserializer.data}
                return Response(response,status=status.HTTP_200_OK)
            
        else:
            response={'message':'this is not working'}
            return Response(response,status=status.HTTP_204_NO_CONTENT)   
        
    # because we have our own method for creating and updating
    def update(self,request,*args,**kwargs):
        response={'message':'you cant update review like that'}
        return Response(response,status=status.HTTP_400_BAD_REQUEST)
    
    def create(self,request,*args,**kwargs):
        response={'message':'you cant create review like that'}
        return Response(response,status=status.HTTP_400_BAD_REQUEST)
    
class BookRateViewSet(viewsets.ModelViewSet):
    queryset=BookRate.objects.all()
    serializer_class=BookRateSerializer
    authentication_classes=(TokenAuthentication,)
    permission_classes=(IsAuthenticated,)
    
    # because we have our own method for creating and updating
    def update(self,request,*args,**kwargs):
        response={'message':'you cant update rating like that'}
        return Response(response,status=status.HTTP_400_BAD_REQUEST)
    
    def create(self,request,*args,**kwargs):
        response={'message':'you cant create rating like that'}
        return Response(response,status=status.HTTP_400_BAD_REQUEST)


class FactorViewSet(viewsets.ModelViewSet):
    queryset=Factor.objects.all()
    serializer_class=FactorSerializer
    authentication_classes=(TokenAuthentication,)
    permission_classes=(IsAuthenticated,)
    
   
    
    def create(self,request,*args,**kwargs):
        response={'message':'you cant create factor like that'}
        return Response(response,status=status.HTTP_400_BAD_REQUEST) 
    
    @action(detail=False,methods=['POST'])
    def all_user_factors(self,request):
            user=request.user
            try:
                factor=Factor.objects.filter(customer=user.id)
                factorserializer=FactorSerializer(factor,many=True)
                response={'message':'successfully find these factors','result':1,'factor':factorserializer.data}
                return Response(response,status=status.HTTP_200_OK)
            except:
                response={'message':'there is no factor'}
                return Response(response,status=status.HTTP_204_NO_CONTENT)  
       
    
    @action(detail=False,methods=['POST'])
    def change_factor_status(self,request):
        if 'code' in request.data:
            user=request.user
            payment=request.data['payment']
            delivered=request.data['delivered']
            customerReceived=request.data['send']
            verify=request.data['verified']
            user=request.user
            fcode=request.data['code']
            try:
                factor=Factor.objects.get(customer=user.id,code=fcode)
                factor.successfulPayment=payment
                factor.deliveredToTheCustomer=customerReceived
                factor.deliveredToThePost=delivered
                factor.verified=verify
                factor.save()
                factorserializer=FactorSerializer(factor,many=False)
                response={'message':'successfully updated verified field of factor','result':1,'factor':factorserializer.data}
                return Response(response,status=status.HTTP_200_OK)
            except:
                
                factor=Factor.objects.create(customer=user,code=fcode
                                             ,successfulPayment=payment,
                                             deliveredToTheCustomer=customerReceived,
                                             deliveredToThePost=delivered,
                                             verified=verify)
                
                factorserializer=FactorSerializer(factor,many=False)
                response={'message':'successfully created factor','result':1,'factor':factorserializer.data}
                return Response(response,status=status.HTTP_200_OK)
        else:
            response={'message':'this is not working','result':2}
            return Response(response,status=status.HTTP_400_BAD_REQUEST)
        
    @action(detail=False,methods=['POST'])
    def create_factor(self,request):
        if 'code' in request.data:
            user=request.user
            fcode=request.data['code']
            try:
                factor=Factor.objects.get(customer=user.id,code=fcode)
                
                factorserializer=FactorSerializer(factor,many=False)
                response={'message':'successfully find that factor','result':1,'factor':factorserializer.data}
                return Response(response,status=status.HTTP_200_OK)
            except:
                factor=Factor.objects.create(customer=user,code=fcode)
                factorserializer=FactorSerializer(factor,many=False)
                response={'message':'factor created','result':2,'factor':factorserializer.data}
                return Response(response,status=status.HTTP_200_OK)     
        else:
            response={'message':'this is not working'}
            return Response(response,status=status.HTTP_204_NO_CONTENT)
    
    # @action(detail=False,methods=['POST'])
    # def set_factor_post_price(self,request):
    #     if 'code' in request.data:
    #         user=request.user
    #         postPrice=request.data['price']
    #         fcode=request.data['code']
    #         try:
    #             factor=Factor.objects.get(customer=user.id,code=fcode)
    #             factor.postCost=postPrice
    #             factor.save()
    #             factorserializer=FactorSerializer(factor,many=False)
    #             response={'message':'successfully edit that factor','result':1,'factor':factorserializer.data}
    #             return Response(response,status=status.HTTP_200_OK)
    #         except:
                
    #             response={'message':'factor not found','result':2}
    #             return Response(response,status=status.HTTP_400_BAD_REQUEST)     
    #     else:
    #         response={'message':'this is not working'}
    #         return Response(response,status=status.HTTP_204_NO_CONTENT)
    @action(detail=False,methods=['POST'])
    def pay(self,request):
        delivered=request.data['factorCode']
       
    
    @action(detail=False,methods=['POST'])
    def factors_status(self,request):
        # fcode=request.data['code']
        payment=request.data['payment']
        delivered=request.data['delivered']
        customerReceived=request.data['send']
        user=request.user
        factors=Factor.objects.filter(successfulPayment=payment,deliveredToThePost=delivered,deliveredToTheCustomer=customerReceived)
        try:
            factors=Factor.objects.filter(successfulPayment=payment,deliveredToThePost=delivered,deliveredToTheCustomer=customerReceived)
            if len(factors)>0:
                factorserializer=FactorSerializer(factors,many=True)
                response={'message':'successfully find these factors ','result':1,'factor':factorserializer.data}
                return Response(response,status=status.HTTP_200_OK)
            else:
                response={'message':'there is no factor'}
                return Response(response,status=status.HTTP_204_NO_CONTENT)
        except:
            factors=Factor.objects.filter(successfulPayment=payment,deliveredToThePost=delivered,deliveredToTheCustomer=customerReceived)
            if len(factors)>0:
                factorserializer=FactorSerializer(factors,many=True)
                response={'message':'successfully find these factors ','result':1,'factor':factorserializer.data}
                return Response(response,status=status.HTTP_200_OK)
            else:
                response={'message':'there is no factor'}
                return Response(response,status=status.HTTP_204_NO_CONTENT) 
    
    
    # its for manager 
    @action(detail=False,methods=['POST'])
    def Ready_To_Send_Orders(self,request):
        factors=Factor.objects.filter(successfulPayment=True)
        OrderItems=[]
        orderSerializer=[]
        orders=[]
        for factor in factors:
            OrderItems=(PurchaseInvoice.objects.filter(factorCode=factor.code)) 
            orderSerializer=(PurchaseInvoiceSerializer(OrderItems,many=True).data)
            orders.append(orderSerializer)
            
        user=request.user
        try:
            response={'message':'this is working','result':orders}
            return Response(response,status=status.HTTP_200_OK)
        except:
            response={'message':'this is working','result':orders}
            return Response(response,status=status.HTTP_200_OK)
            
        # else:
        #     response={'message':'this is not working'}
        #     return Response(response,status=status.HTTP_204_NO_CONTENT)
        

class PurchaseInvoiceViewSet(viewsets.ModelViewSet):
    queryset=PurchaseInvoice.objects.all()
    serializer_class=PurchaseInvoiceSerializer
    authentication_classes=(TokenAuthentication,)
    permission_classes=(AllowAny,)
    
    @action(detail=False,methods=['POST'])
    def id(self,request):
        if 'id' in request.data:
            user=request.user
            try:
                response={'message':'this is working','result':user.id}
                return Response(response,status=status.HTTP_200_OK)
            except:
                response={'message':'this is working','result':user.id}
                return Response(response,status=status.HTTP_200_OK)
            
        else:
            response={'message':'this is not working'}
            return Response(response,status=status.HTTP_204_NO_CONTENT)
    
    # @action(detail=False,methods=['POST'])
    # def unverified_basket(self,request):
    #   if 'code' in request.data:
          
    @action(detail=False,methods=['POST'])
    def basket(self,request):
        if 'userId' in request.data:
            userId=request.data['userId']
            factor=request.data['factorCode']
            basket=PurchaseInvoice.objects.filter(customer=userId,factorCode=factor)
            try:       
                basketserializer=PurchaseInvoiceSerializer(basket,many=True)   
                response={'result':basketserializer.data}
                return Response(response,status=status.HTTP_200_OK)
            except:
                basketserializer=PurchaseInvoiceSerializer(basket,many=True)
                response={'message':'this is working','result':basketserializer.data}
                return Response(response,status=status.HTTP_200_OK)
        else:
            response={'message':'this is not working'}
            return Response(response,status=status.HTTP_204_NO_CONTENT)   
    
    @action(detail=False,methods=['POST'])
    def basketItems(self,request):
        if 'factorCode' in request.data:
            fcode=request.data['factorCode']
            basket=PurchaseInvoice.objects.filter(factorCode=fcode)
            try:       
                basketserializer=PurchaseInvoiceSerializer(basket,many=True)   
                response={'result':basketserializer.data}
                return Response(response,status=status.HTTP_200_OK)
            except:
                basketserializer=PurchaseInvoiceSerializer(basket,many=True)
                response={'message':'this is working','result':basketserializer.data}
                return Response(response,status=status.HTTP_200_OK)
        else:
            response={'message':'this is not working'}
            return Response(response,status=status.HTTP_204_NO_CONTENT) 
    @action(detail=False,methods=['POST'])
    def delete(self,request):
        if 'factorCode' in request.data:
            fcode=request.data['factorCode']
            bookId=request.data['bookId']
            
            try:
                orders=PurchaseInvoice.objects.filter(factorCode=fcode)
                PurchaseInvoice.objects.get(factorCode=fcode,book_id=bookId).delete()     
                orderserializer=PurchaseInvoiceSerializer(orders,many=True)   
                response={'message':'successfully deleted the item from the database','result':orderserializer.data}
                return Response(response,status=status.HTTP_200_OK)
            except:
                orders=PurchaseInvoice.objects.filter(factorCode=fcode)
                PurchaseInvoice.objects.get(factorCode=fcode,book_id=bookId).delete()     
                orderserializer=PurchaseInvoiceSerializer(orders,many=True)   
                response={'message':'successfully deleted the item from the database','result':orderserializer.data}
                return Response(response,status=status.HTTP_200_OK)
        else:
            response={'message':'this is not working'}
            return Response(response,status=status.HTTP_204_NO_CONTENT)
        
    # because we have our own method for creating and updating
    def update(self,request,*args,**kwargs):
        response={'message':'you cant update rating like that'}
        return Response(response,status=status.HTTP_400_BAD_REQUEST)
    
    def create(self,request,*args,**kwargs):
        response={'message':'you cant create rating like that'}
        return Response(response,status=status.HTTP_400_BAD_REQUEST)    
        
class StoreHouseViewSet(viewsets.ModelViewSet):
    queryset=StoreHouse.objects.all()
    serializer_class=StoreHouseSerializer
    authentication_classes=(TokenAuthentication,)
    permission_classes=(AllowAny,)
    http_method_names = ['post', ]
    lookup_field="book_id"
    
    @action(detail=False,methods=['POST'])
    def create_order(self,request):
        if 'factorCode' in request.data:
            bookId=int(request.data['book_id'])
            quantity=int(request.data['quantity'])
            customer=request.user
            fCode=request.data['factorCode']
            date=request.data['date']
            bookInstance=Book.objects.get(id=bookId)
            
            # price=bookInstance.price
            # print("this is price",price)
            book=StoreHouse.objects.get(book_id=bookId)
            # check if book is available
            if book.amount >= quantity:
                user=request.user
                try:
                    purchaseItem=PurchaseInvoice.objects.get(customer=customer.id,book_id=bookId,factorCode=fCode)
                    purchaseItem.quantity=quantity
                    purchaseItem.date=date
                    # purchaseItem.singleCost=price
                    
                    # purchaseItem.totalCost=price*quantity
                    
                    purchaseItem.save()
                    p=PurchaseInvoice.objects.get(customer=customer.id,book_id=bookId,factorCode=fCode)
                    print("this is item",bookId,p.quantity,"----",quantity)
                    orderserializer=PurchaseInvoiceSerializer(purchaseItem,many=False)
                    response={'message':'purchase updated','result':orderserializer.data}
                    return Response(response,status=status.HTTP_200_OK)
                except:
                    purchaseItem=PurchaseInvoice.objects.create(customer=customer,book_id=bookInstance,quantity=quantity,factorCode=fCode)
                    orderserializer=PurchaseInvoiceSerializer(purchaseItem,many=False)
                    p=PurchaseInvoice.objects.get(customer=customer.id,book_id=bookId,factorCode=fCode)
                    print("this is item",bookId,p.quantity,"----",quantity)
                    response={'message':'purchase created','result':orderserializer.data}
                    return Response(response,status=status.HTTP_200_OK)
            else:
                response={'message':'sorry we dont have that much of book'}
            return Response(response,status=status.HTTP_203_NON_AUTHORITATIVE_INFORMATION)
            
        else:
            response={'message':'this is not working'}
            return Response(response,status=status.HTTP_204_NO_CONTENT)