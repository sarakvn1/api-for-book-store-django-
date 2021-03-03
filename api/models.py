from django.db import models
from django.contrib.auth.models import User

from django.core.validators import MaxValueValidator,MinValueValidator,MaxLengthValidator,MinLengthValidator
# Create your models here.

def media_file_name(instance, filename):
    h = instance.md5sum
    basename, ext = os.path.splitext(filename)
    return os.path.join('mediafiles', h[0:1], h[1:2], h + ext.lower())

class Profile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    dob = models.DateField(null=True, blank=True)
    first_name=models.CharField(max_length=50)
    last_name=models.CharField(max_length=50)
    CHOICES = (
        ('f', 'female'),
        ('m', 'male'),
       )
    sex=models.CharField(max_length=30,choices=CHOICES,default='f')
    @property
    def Address(self):
        AddressList=[]
        addresses=[]
        addresses=Address.objects.filter(customer=self.user.id)
        for address in addresses:
            AddressList.append({'name':address.name,'detail':address.detail,'postalCode':address.postalCode,'phoneNumber':address.phoneNumber,'staticNumber':address.staticNumber,'city':address.city,'state':address.state})
        return AddressList

class Address(models.Model):
    CITY_CHOICES = (
        ('Rasht', 'Rasht'),
        ('Shiraz','Shiraz'),
        ('Tehran','Tehran'),
        ('Esfehan','Esfehan'),
        ('Tabriz','Tabriz'),
        ('Mashhad','Mashhad'),
        # ('',''),
        # ('',''),
        # ('',''),
        # ('',''),
        # ('',''),
        
        
       )
    
    STATE_CHOICES = (
        ('Guilan', 'Guilan'),
        ('Fars','Fars'),
        ('Tehran','Tehran'),
        ('Esfehan','Esfehan'),
        ('Markazi','Markazi'),
        ('Hamedan','Hamedan'),
        # ('',''),
        # ('',''),
        # ('',''),
        # ('',''),
        # ('',''),
        
        
       )
    customer=models.ForeignKey(User,on_delete=models.CASCADE)
    name=models.CharField(max_length=50)
    first_name=models.CharField(max_length=50)
    last_name=models.CharField(max_length=50)
    detail=models.CharField(max_length=500)
    state=models.CharField(choices=STATE_CHOICES,max_length=500)
    city=models.CharField(choices=CITY_CHOICES,max_length=500)
    postalCode=models.CharField(max_length=10,blank=True,null=True)
    phoneNumber=models.CharField(max_length=11,blank=True,null=True)
    staticNumber=models.CharField(max_length=10,blank=True,null=True)
    def __str__(self):
        return self.name
    
class Author(models.Model):
    CHOICES = (
        ('f', 'female'),
        ('m', 'male'),
       )
    Fa_first_name=models.CharField(max_length=50)
    En_first_name=models.CharField(max_length=50)
    Fa_last_name=models.CharField(max_length=50)
    En_last_name=models.CharField(max_length=50)
    sex=models.CharField(max_length=30,choices=CHOICES)
    def EnlistOfBooks(self):
        bookList=[]
        books=Book.objects.filter(authors_id=self)
        for book in books:
            bookList.append(book.En_title)
        return bookList
    
    def FalistOfBooks(self):
        bookList=[]
        books=Book.objects.filter(authors_id=self)
        for book in books:
            bookList.append(book.Fa_title)
        return bookList
    
    def __str__(self):
        return self.En_first_name + ' ' +self.En_last_name
import base64

class Publisher(models.Model):
    Fa_name=models.CharField(max_length=50)
    En_name=models.CharField(max_length=50)
    
    
    def EnlistOfBooks(self):
        bookList=[]
        books=Book.objects.filter(publisher=self)
        for book in books:
            bookList.append(book.En_title)
        return bookList
    
    def FalistOfBooks(self):
        bookList=[]
        books=Book.objects.filter(publisher=self)
        for book in books:
            bookList.append(book.Fa_title)
        return bookList
    
    def __str__(self):
        return self.En_name
      
class Genre(models.Model):
    Fa_genre_name=models.CharField(max_length=50)
    En_genre_name=models.CharField(max_length=50)
    
    
    def EnlistOfBooks(self):
        bookList=[]
        books=Book.objects.filter(genre=self)
        for book in books:
            bookList.append(book.En_title)
        return bookList
    
    def FalistOfBooks(self):
        bookList=[]
        books=Book.objects.filter(genre=self)
        for book in books:
            bookList.append(book.Fa_title)
        return bookList   
    def __str__(self):
        return self.En_genre_name
    
# book model
class Book(models.Model):
    isbn=models.CharField(max_length=10)
    Fa_title=models.CharField(max_length=50)
    En_title=models.CharField(max_length=50)
    authors_id=models.ManyToManyField(Author)
    publication_date=models.DateTimeField(blank=True,null=True)
    image=models.FileField(upload_to='images',blank=True,null=True)
    genre=models.ManyToManyField(Genre)
    price=models.IntegerField(blank=True,null=True)
    publisher=models.ForeignKey(Publisher,on_delete=models.CASCADE )
    FaSummary=models.CharField(max_length=350,blank=True,null=True)
    EnSummary=models.CharField(max_length=350,blank=True,null=True)
    
    def __str__(self):
        return self.En_title
    
    def available(self):
        book=StoreHouse.objects.get(book_id=self)
        if book.amount>0:
           return True
        else:
            return False
        
    
    def lessThanFive(self): 
        book= StoreHouse.objects.get(book_id=self)
        if book.amount<5:
            return True
        else:
            return False
    
    def available_amount_to_order(self): 
        book= StoreHouse.objects.get(book_id=self)
        return book.amount
    

    def En_authors(self):
        
        alist=Author.objects.filter(book=self)
        authorsList=[]
        for author in alist:
            authorsList.append(author.En_first_name+' '+author.En_last_name)
        return authorsList
    
    def Fa_authors(self):
        
        alist=Author.objects.filter(book=self)
        authorsList=[]
        for author in alist:
            authorsList.append(author.Fa_first_name+' '+author.Fa_last_name)
        return authorsList
    
    def no_of_ratings(self):
        ratings=BookRate.objects.filter(book_id=self)
        return len(ratings)
    
    def avg_ratings(self):
        sum=0
        ratings=BookRate.objects.filter(book_id=self)
        for rating in ratings:
            sum+=rating.stars
        if len(ratings)>0:
            return sum/len(ratings)
        else: 
            return 0
    
    def listOfReviews(self):
        bookReviewsId=[]
        reviews=BookReview.objects.filter(book_id=self)
        for review in reviews:
            bookReviewsId.append(review.id)
        return bookReviewsId
    
   
    
    # @property
    # def get_unique_id(self):
    #     a = self.last_name[:2].upper()     #First 2 letters of last name
    #     b = self.birth_date.strftime('%d')     #Day of the month as string
    #     c = self.city_of_birth[:2].upper()     #First 2 letters of city
    #     return a + b + c 
# class Customer(models.Model):
#     user=models.ForeignKey(User,on_delete=models.CASCADE)

class BookReview(models.Model):
    book_id=models.ForeignKey(Book,on_delete=models.CASCADE)
    customer=models.ForeignKey(User,on_delete=models.CASCADE)
    # review_title=models.TextField(max_length=200,default='unknown')
    content=models.TextField(max_length=450)
    date=models.DateTimeField(blank=True,null=True,auto_now_add=True)
    
    
    @property
    def username(self):
        return self.customer.first_name +" "+ self.customer.last_name
    class Meta:
        unique_together=(('customer','book_id'),)
        index_together=(('customer','book_id'),)
        
class BookRate(models.Model):
    book_id=models.ForeignKey(Book,on_delete=models.CASCADE)
    customer=models.ForeignKey(User,on_delete=models.CASCADE)
    date=models.DateTimeField(blank=True,null=True,auto_now_add=True)
    stars=models.IntegerField(validators=[MinValueValidator(1),MaxValueValidator(5)])
    class Meta:
        unique_together=(('customer','book_id'),)
        index_together=(('customer','book_id'),)


       
class PurchaseInvoice(models.Model):
    book_id=models.ForeignKey(Book,on_delete=models.CASCADE)
    factorCode=models.CharField(max_length=10)
    date=models.DateTimeField(blank=True,null=True,auto_now_add=True)
    quantity=models.IntegerField()
    customer=models.ForeignKey(User,on_delete=models.CASCADE,blank=True,null=True)
    # singleCost=models.IntegerField(blank=True,null=True)
    # totalCost=models.IntegerField(blank=True,null=True)
    # def totalCost(self):
    #     total=0
    #     book=Book.objects.get(id=self.book_id)
    #     # item=PurchaseInvoice.objects.get(id=self)
    #     # quantity=item.quantity
    #     cost=book.price
    #     return cost*quantity
    @property
    def EnBookName(self):
        return self.book_id.En_title
    
    @property
    def FaBookName(self):
        return self.book_id.Fa_title
    
    @property
    def single_cost(self):
        return self.book_id.price
        
    @property
    def total_cost(self):
        return self.book_id.price*self.quantity
        
    def __str__(self):
        return str(self.factorCode)

class Factor(models.Model):
    customer=models.ForeignKey(User,on_delete=models.CASCADE)
    code=models.CharField(max_length=10)
    createDate=models.DateTimeField(blank=True,null=True,auto_now_add=True)
    successfulPayment=models.BooleanField(default=False)
    verified=models.BooleanField(default=False)
    deliveredToTheCustomer=models.BooleanField(default=False)
    deliveredToThePost=models.BooleanField(default=False)
    address=models.OneToOneField(Address,blank=True,null=True,on_delete=models.DO_NOTHING)
    timeOfDeliveringToThePost=models.DateTimeField(blank=True,null=True,auto_now_add=True)
    postCost=models.IntegerField(blank=True,null=True,default=80000)
    
    @property
    def TotalCostWithPost(self):
        total=0
        items=PurchaseInvoice.objects.filter(factorCode=self)
        for item in items:
            total=total+item.total_cost
        return total+self.postCost
    
    @property
    def TotalCost(self):
        total=0
        items=PurchaseInvoice.objects.filter(factorCode=self)
        for item in items:
            total=total+item.total_cost
        return total
    
    @property
    def addressDetail(self):
        if self.address:
            address={'last_name':self.address.last_name,'first_name':self.address.first_name,'state':self.address.state,'city':self.address.last_name,'phoneNumber':self.address.phoneNumber,'staticNumber':self.address.staticNumber,'detail':self.address.detail,'postalCode':self.address.postalCode}
            return address
        else:
            return "unknown"
            
    def __str__(self):
        return self.code
    
class StoreHouse(models.Model):
    book_id=models.ForeignKey(Book,on_delete=models.CASCADE)
    date=models.DateTimeField(blank=True,null=True,auto_now_add=True)
    amount=models.IntegerField()
    
    def __str__(self):
        return str(self.book_id)
    
    class Meta:
        unique_together=(('amount','book_id'),)
        index_together=(('amount','book_id'),)
    
# class User(models.Model):
    
#     # def authors(self):
        
#     #     alist=Author.objects.filter(book=self)
#     #     authorsList=[]
#     #     for author in alist:
#     #         authorsList.append(author.first_name+' '+author.last_name)
#     #     return authorsList
#     def user_invoice(self):
#         invoiceList=Factors.objects.filter(user=self)
#         bookIdList=[]
#         for item in invoiceList:
#             bookIdList.append(item.book_id)
        
#         return bookIdList
           
        
        