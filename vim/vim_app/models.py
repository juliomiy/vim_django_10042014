# This is an auto-generated Django model module.
# You'll have to do the following manually to clean this up:
#   * Rearrange models' order
#   * Make sure each model has one field with primary_key=True
#   * Remove `managed = False` lines if you wish to allow Django to create and delete the table
# Feel free to rename the models, but don't rename db_table values or field names.
#
# Also note: You'll have to insert the output of 'django-admin.py sqlcustom [appname]'
# into your database.
from __future__ import unicode_literals

from datetime import datetime   
from django.db import models
from django.core.exceptions import ValidationError
from django.core.validators import validate_email
from common import normalize_string 

class CommonInfo(models.Model):
    createtimestamp = models.DateTimeField(default=datetime.now)
    updatetimestamp = models.DateTimeField(blank=True, null=True)
    latitude = models.DecimalField(max_digits=8, decimal_places=5, default=0,blank=True, null=True)
    longitude = models.DecimalField(max_digits=8, decimal_places=5,default=0,blank=True,null=True)

    class Meta:
        managed = False
        abstract = True

class Appointments(CommonInfo):
    idappointments = models.AutoField(primary_key=True)
    idcustomer = models.IntegerField()
    idstylist_assigned = models.IntegerField()
    reservationdatetime = models.DateTimeField()
    reservationschedued = models.DateTimeField(blank=True, null=True)
    idmarkets = models.IntegerField()
    address1 = models.CharField(max_length=45)
    address2 = models.CharField(max_length=45, blank=True)
    city = models.CharField(max_length=45)
    state = models.CharField(max_length=45)
    postalcode = models.CharField(max_length=15)
    services = models.CharField(max_length=255)
    price = models.FloatField()
    mobile = models.CharField(max_length=15, blank=True)
    customername = models.CharField(max_length=100)
    iddispatcher = models.IntegerField()
    dispatchername = models.CharField(max_length=100, blank=True)

    class Meta(CommonInfo.Meta):
        db_table = 'appointments'

class Customer(CommonInfo):
    MOBILE_EXISTS,EMAIL_EXISTS ,INVALID_EMAIL,MISSING_MOBILE, MISSING_EMAIL, MISSING_POSTALCODE,MISSING_FIRSTNAME, MISSING_LASTNAME, MISSING_PASSWORD = range(-1, 8)
    ERROR = {
       MISSING_MOBILE:'Invalid Mobile Phone',
       MISSING_EMAIL:'Email Required',
       MISSING_FIRSTNAME: 'First Name Required',
       MISSING_LASTNAME: 'Last Name Required',
       MISSING_PASSWORD: 'Password  Required',
       MISSING_POSTALCODE: 'Postalcode  Required',
       MOBILE_EXISTS: 'Mobile Exists',
       EMAIL_EXISTS: 'Email Exists',
       INVALID_EMAIL: 'Invalid Email',
    }   

    idcustomer = models.AutoField(primary_key=True,blank=True)
    firstname = models.CharField(max_length=45)
    lastname = models.CharField(max_length=45)
    middlename = models.CharField(max_length=45, blank=True,null=True)
    email = models.EmailField(max_length=255,blank=True,null=False)
    address1 = models.CharField(max_length=255)
    address2 = models.CharField(max_length=255, blank=True)
    city = models.CharField(max_length=45)
    postalcode = models.CharField(max_length=20)
    mobile = models.CharField(max_length=15, blank=False, null=False)
    active = models.SmallIntegerField(default=0)
    facebook = models.CharField(max_length=45, blank=True)
    facebook_token = models.CharField(max_length=45, blank=True)
    twitter = models.CharField(max_length=45, blank=True, null=True)
    twitter_token = models.CharField(max_length=45, blank=True, null=True)
    wallet = models.CharField(max_length=45, blank=True, null=True)
    wallet_token = models.CharField(max_length=45, blank=True,null=True)
    paypal = models.CharField(max_length=45, blank=True,null=True)
    paypal_token = models.CharField(max_length=45, blank=True,null=True)
    password = models.CharField(max_length=255)
    class Meta(CommonInfo.Meta):
        db_table = 'customer'


    def createCustomer(self,*args, **kwargs):
    	"""
        Create a new customer. Leaves the Customer inactive
        THe class attribute idcustomer will be set to the customer ID and is also returned in the
        response object
    	"""
        response  = {'status': None , 'error': None , 'errorcnt': 0 , 'idcustomer': 0 }
        errorlist=[]
        self.idcustomer=None

        if not self.mobile:
           errorlist.append(self.ERROR[self.MISSING_MOBILE])
           response['errorcnt']+=1
        if not self.firstname:
           errorlist.append(self.ERROR[self.MISSING_FIRSTNAME])
           response['errorcnt']+=1
        if not self.lastname:
           errorlist.append(self.ERROR[self.MISSING_LASTNAME])
           response['errorcnt']+=1
        if not self.email:
           errorlist.append(self.ERROR[self.MISSING_EMAIL])
           response['errorcnt']+=1
        if not self.postalcode:
           errorlist.append(self.ERROR[self.MISSING_POSTALCODE])
           response['errorcnt']+=1
        if not self.password:
           errorlist.append(self.ERROR[self.MISSING_PASSWORD])
           response['errorcnt']+=1
  
        if response['errorcnt'] == 0:
	   exist = self.doesMobileExist(self.mobile)
           if 0 != exist['idcustomer']:
              errorlist.append(self.ERROR[self.MOBILE_EXISTS])
              response['errorcnt']+=1
 
        if response['errorcnt'] == 0:
           try:
               validate_email(self.email)
           except ValidationError as e:
                errorlist.append(self.ERROR[self.INVALID_EMAIL])
                response['errorcnt']+=1
           else:
	       exist = self.doesEmailExist(self.email)
               if 0 != exist['idcustomer']:
                    errorlist.append(self.ERROR[self.EMAIL_EXISTS])
                    response['errorcnt']+=1

        if response['errorcnt'] != 0:
           response['error'] = errorlist
           return response

        self.active=0
        super(Customer, self).save(*args, **kwargs) # Call the "real" save() method.
        response['idcustomer'] = self.idcustomer
	response['status']=True
        return response

    def updateCustomer(self,*args, **kwargs):
	pass

    def doesMobileExist(self, mobile):
        response  = {'status': None , 'error': None , 'errorcnt': 0 , 'idcustomer': 0 }
	exist = Customer.objects.raw('select idcustomer from customer where mobile = %s',[mobile])
        for c in exist:
	    response['idcustomer'] = c.idcustomer
            response['status'] = True
        else:
            response['status'] = False

        return response 

    def doesEmailExist(self, email):
        response  = {'status': None , 'error': None , 'errorcnt': 0 , 'idcustomer': 0 }
	exist = Customer.objects.raw('select idcustomer from customer where email = %s',[email])
        for c in exist:
	    response['idcustomer'] = c.idcustomer
            response['status'] = True
        else:
            response['status'] = False

        return response 

    def __unicode__(self):
        return u'Firstname %s Lastname %s Mobile %s Postalcode %s Active %s' % (self.firstname, self.lastname, self.postalcode,self.mobile, self.active)

class Dispatcher(CommonInfo):
    iddispatcher = models.AutoField(primary_key=True)
    firstname = models.CharField(max_length=45)
    middlename = models.CharField(max_length=45)
    lastname = models.CharField(max_length=45)
    email = models.EmailField(max_length=255, blank=False,null=False)
    address1 = models.CharField(max_length=255)
    address2 = models.CharField(max_length=255, blank=True)
    city = models.CharField(max_length=45)
    state = models.CharField(max_length=45)
    postalcode = models.CharField(max_length=20)
    mobile = models.CharField(max_length=15)
    class Meta(CommonInfo.Meta):
        db_table = 'dispatcher'

class Markets(CommonInfo):
    MISSING_MARKETNAME,MARKET_EXISTS = range(-1,1)
    ERROR = {
       MISSING_MARKETNAME:'Missing Market Name',
       MARKET_EXISTS: 'Market Exists',
    }
    idmarkets = models.AutoField(primary_key=True)
    name = models.CharField(max_length=45)
    normalizedname = models.CharField(max_length=45)
    
    class Meta(CommonInfo.Meta):
        db_table = 'markets'

    def createMarket(self,*args, **kwargs):
    	"""
        Create a new market - solely an administrative operation
        THe class attribute idmarket will be set to the mrket ID and is also returned in the
        response object
    	"""
        response  = {'status': None , 'error': None , 'errorcnt': 0 , 'idmarket': 0 }
        errorlist=[]
        self.idmarket=None

        if not self.name:
           errorlist.append(self.ERROR[self.MISSING_MARKETNAME])
           response['errorcnt']+=1
  
        if response['errorcnt'] == 0:
	   exist = self.doesMarketExist(self.name)
           if 0 != exist['idmarket']:
              errorlist.append(self.ERROR[self.MARKET_EXISTS])
              response['errorcnt']+=1

        if response['errorcnt'] != 0:
           response['error'] = errorlist
           return response

        self.normalizedname= normalize_string(self.name)

        super(Markets, self).save(*args, **kwargs) # Call the "real" save() method.
        response['idmarket'] = self.idmarkets
	response['status']=True
        return response

    def doesMarketExist(self, name):
        '''
        check if market represented by name exists in markets table
        >>>doesMarketExist('Lower East Side')
        {u'error': None, u'errorcnt': 0, u'idmarket': 5, u'status': False}
        '''
        response  = {'status': None , 'error': None , 'errorcnt': 0 , 'idmarket': 0 }
	exist = Markets.objects.raw('select idmarkets from markets  where name = %s',[name])
        for c in exist:
	    response['idmarket'] = c.idmarkets
            response['status'] = True
        else:
            response['status'] = False

        return response 

    def __unicode__(self):
        return u'Market Name %s' % (self.name)

class Stylist(CommonInfo):
    idstylist = models.AutoField(primary_key=True)
    firstname = models.CharField(max_length=45)
    middlename = models.CharField(max_length=45)
    lastname = models.CharField(max_length=45)
    email = models.EmailField(max_length=255, blank=False,null=False)
    address1 = models.CharField(max_length=45)
    address2 = models.CharField(max_length=45, blank=True)
    city = models.CharField(max_length=45)
    state = models.CharField(max_length=45)
    postalcode = models.CharField(max_length=20)
    active = models.SmallIntegerField()
    mobile = models.CharField(max_length=15)
    idmarket = models.ForeignKey(Markets, db_column='idmarket')
    avatar = models.CharField(max_length=255, blank=True)
    password = models.CharField(max_length=255)

    class Meta(CommonInfo.Meta):
        db_table = 'stylist'


if __name__ == "__main__":
    import doctest
    doctest.testmod()
