from django.db import models
from django.utils import timezone
# Create your models here.

class AdsCategory(models.Model):
    title = models.CharField(max_length=100, blank=True)
    catid=models.IntegerField(blank=False)
    created = models.DateTimeField(default=timezone.now)
    def __str__(self):
        return self.title
    #admin site display, easy to debug and view objects
    class Meta:
        db_table = 'tb_category' #modify table name
        verbose_name = 'Category management' #admin site display
        verbose_name_plural = verbose_name


from users.models import User
from django.utils import timezone
class Ad(models.Model):
    #on_delete: When the data in the user table is deleted, the article information is also deleted synchronously
    landlord = models.ForeignKey(User,on_delete=models.CASCADE)
    adid = models.IntegerField(null=True, blank=True)
    telephone = models.CharField(null=True, blank=True,max_length=20)
    #author = models.CharField(max_length=50, blank=True)
    address=models.CharField(max_length=120,blank=False)
    metro=models.CharField(max_length=120,blank=False)
    square=models.CharField(max_length=50,blank=False)
    title = models.CharField(max_length=120,blank=False)
    price=models.IntegerField(blank=False)
    category = models.ForeignKey(AdsCategory,null=True,blank=True,on_delete=models.CASCADE,related_name='ad')
    photo = models.ImageField(upload_to='imgcian/', blank=True)
    #tags = models.CharField(max_length=50,blank=True)
    #summary = models.CharField(max_length=600,null=False,blank=False)
    description = models.TextField()
    total_views = models.PositiveIntegerField(default=0)
    comments_count = models.PositiveIntegerField(default=0)
    created = models.DateTimeField(default=timezone.now)
    updated = models.DateTimeField(auto_now=True)
    #Modify the table name and configuration information.
    class Meta:
        db_table = 'tb_ad'
        ordering = ('-created',)
        verbose_name = 'Ad management'
        verbose_name_plural = verbose_name
        unique_together = (("address", "title", "category", "photo"),)
    def __str__(self):
        return self.title


class Comment(models.Model):
    content = models.TextField()
    ad = models.ForeignKey(Ad,on_delete=models.SET_NULL,null=True)
    user = models.ForeignKey('users.User',on_delete=models.SET_NULL, null=True)
    created = models.DateTimeField(auto_now=True)
    def __str__(self):
        return self.ad.title
    class Meta:
        db_table = 'tb_comment'
        verbose_name = 'Comment management'
        verbose_name_plural = verbose_name

class RPESModel(models.Model):
    r1 = models.FloatField()
    m1 = models.FloatField()
    m2 = models.FloatField()
    m3 = models.FloatField()
    m4 = models.FloatField()
    m5 = models.FloatField()
    m6 = models.FloatField()
    m7 = models.FloatField()
    m8 = models.FloatField()
    m9 = models.FloatField()
    m10 = models.FloatField()
    m11 = models.FloatField()
    m12 = models.FloatField()
    m13 = models.FloatField()
    m14 = models.FloatField()
    m15 = models.FloatField()
    s1 = models.FloatField()
    c1 = models.FloatField()
    def __str__(self):
        return str(self.r1)+' * room + '+str(self.m1)+' * metro1 + '+str(self.m2)+' * metro2 + '+str(self.m3)+' * metro3 + '+str(self.m4)+\
               ' * metro4 + '+str(self.m5)+' * metro5 + '+str(self.m6)+' * metro6 + '+str(self.m7)+' * metro7 + '+str(self.m8)+' * metro8 + '+\
               str(self.m9)+' * metro9 + '+str(self.m10)+' * metro10 + '+str(self.m11)+' * metro11 + '+str(self.m12)+' * metro12 + '+\
               str(self.m13)+' * metro13 + '+str(self.m14)+' * metro14 + '+str(self.m15)+' * metro15 + '+str(self.s1)+' * area + ' + str(self.c1)
    class Meta:
        db_table = 'tb_tempModel'
        verbose_name = 'Model management'
        verbose_name_plural = verbose_name
