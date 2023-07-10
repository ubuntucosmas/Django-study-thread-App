from django.db import models
from django.contrib.auth.models import User #already django has a built in user model {refrence= google "django user model"}

# Create your models here.

class Topic(models.Model):
    name = models.CharField(max_length=200) # the topic model has only one attribute 'name' (topic name).

    def __str__(self):
        return self.name

class Room(models.Model):
    host = models.ForeignKey(User, on_delete=models.SET_NULL, null=True)
    topic = models.ForeignKey(Topic, on_delete=models.SET_NULL, null=True) #null=true allows this field to null in the db
    name = models.CharField(max_length=200)
    description = models.TextField(null=True, blank=True)
    participants = models.ManyToManyField(User, related_name='participants', blank=True)
    updated = models.DateTimeField(auto_now=True)
    created = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ['-updated', '-created'] #makes the last updated item to be first e.g last comments are always seem first above old ones

    def __str__(self):    #string representation of this room
        return self.name
    

class Message(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    room = models.ForeignKey(Room, on_delete=models.CASCADE) #here we are just setting relationship#(Room is the parent name) this establishes the relationship in db and thats how we know is connected to what
    body = models.TextField()
    updated = models.DateTimeField(auto_now=True)
    created = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.body[0:50]   # [0:50]<== we only want th first 50 characters in our django admin
    
