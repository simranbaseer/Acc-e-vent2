from django.db import models
from django.utils.timesince import timesince
from .utils import unique_client_id_generator
from .utils import unique_event_id_generator
from django.db.models.signals import pre_save


# Create your models here.
class LocTags(models.Model):
    tagname = models.CharField( max_length=50, primary_key= True)
 
    def __str__(self):
        return self.tagname

    def get_absolute_url(self):
        return reversed("_detail", kwargs={"pk": self.pk})

class PartTags(models.Model):
    tagname = models.CharField( max_length=50, primary_key= True)
 
    def __str__(self):
        return self.tagname

    def get_absolute_url(self):
        return reversed("_detail", kwargs={"pk": self.pk})



class Users(models.Model):

    uid = models.CharField(max_length=8,primary_key=True)
    tags = models.TextField()

    def __str__(self):
        return self.uid

    def get_absolute_url(self):
        return reversed("_detail", kwargs={"pk": self.pk})

class MID(models.Model):
    mid = models.CharField(max_length=12,primary_key=True)

    def __str__(self):
        return self.mid 

class location(models.Model):
    mid = models.ForeignKey(MID, on_delete=models.CASCADE)
    Lname = models.CharField(max_length = 50)
    tags = models.TextField()
    
    def __str__(self):
        return self.Lname

    def get_absolute_url(self):
        return reversed("_detail", kwargs={"pk": self.pk})   
    
class client(models.Model):
    client_id = models.CharField(max_length=120,blank=True,primary_key=True)

    def __str__(self_):
        return self.client_id

    def get_absolute_url(self):
        return reversed("_detail", kwargs={"pk": self.pk})
    

def pre_save_create_client_id(sender,instance,*args,**kwargs):
    if not instance.client_id:
        instance.client_id=unique_client_id_generator(instance)
pre_save.connect(pre_save_create_client_id,sender=client)
    
    
class client_details(models.Model):
    client_id = models.ForeignKey(client, on_delete=models.CASCADE)    
    name = models.CharField(max_length = 30)
    email = models.EmailField(max_length = 254)
    
    def get_absolute_url(self):
        return reversed("_detail", kwargs={"pk": self.pk})
    
    
class event(models.Model):
    event_id = models.CharField(max_length=120,blank=True,primary_key=True)

    def __str__(self_):
        return self.event_id

    def get_absolute_url(self):
        return reversed("_detail", kwargs={"pk": self.pk})
    

def pre_save_create_event_id(sender,instance,*args,**kwargs):
    if not instance.event_id:
        instance.event_id=unique_event_id_generator(instance)
pre_save.connect(pre_save_create_event_id,sender=event)
    


class event_details(models.Model):
    event_id = models.ForeignKey(event, on_delete=models.CASCADE)
    Ename = models.CharField(max_length = 50)
    client_id = models.ForeignKey(client, on_delete=models.CASCADE)
    mid = models.ForeignKey(MID, on_delete=models.CASCADE)
    start_time = models.DateTimeField()
    end_time = models.DateTimeField()
    duration = models.CharField(max_length = 20)
    allow_user = models.TextField()

    def time_diff(self):
        dt1=self.start_time
        dt2=self.end_time
        duration=timesince(dt1,dt2)
        return duration

    def get_absolute_url(self):
        return reversed("_detail", kwargs={"pk": self.pk})    

            

class visitor_log(models.Model):
    uid = models.CharField(max_length=8,primary_key=True)
    mid = models.ForeignKey(MID, on_delete=models.CASCADE)
    event_id = models.ForeignKey(event, on_delete=models.CASCADE)
    time=models.DateTimeField(auto_now_add=True)
    attempt=models.BooleanField()

    def get_absolute_url(self):
        return reversed("_detail", kwargs={"pk": self.pk})