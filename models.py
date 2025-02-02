from django.db import models
from django.contrib.auth.models import AbstractUser
from django.utils import timezone

class User(AbstractUser):
    username = models.CharField(max_length=50,unique=True)
    email = models.EmailField(max_length=100)
    date_of_birth = models.DateField(default='1970-01-01')
    messages = models.ManyToManyField(to='self',symmetrical=False,blank=True)
    Profile  = models.OneToOneField(to='Profile',null=True,on_delete=models.CASCADE)

    def __str__(self):
        return self.username
    
    def to_dict(self):
        return{
            'id':self.id,
            'username':self.username,
            'email':self.email,
            'date_of_birth':self.date_of_birth,
            'messages':self.messages,
            'Profile':self.Profile,
        }
    
    def messages_senrec(self,other):
        #someone sends you a message
        m1 = Messages.objects.filter(sender = other)

        #you send a message to someone
        m2 = Messages.objects.filter(receiver = other)

        return m1.union(m2).order_by('-time_sent')

class Profile(models.Model):
    image = models.ImageField(upload_to='profile_pics',blank=True)
    bio = models.TextField(max_length=500,blank=True)
    
    def __str__(self) -> str:
        return f"{self.bio}"

    def to_dict(self) -> dict:
        return {
            'bio': self.text,
            'image': self.image.url if self.image else None,
        }

class Item(models.Model):
    start_bid = models.DecimalField(max_digits=6,decimal_places=2)
    bid = models.DecimalField(max_digits=6,decimal_places=2)
    title = models.CharField(max_length=50)
    description = models.TextField(max_length=500)
    image = models.ImageField(upload_to='item_pics',blank=True)
    bid_time_finish = models.DateTimeField(default=timezone.now)
    bought = models.BooleanField(default=False)
    owner = models.ForeignKey(User, related_name='item_owner', on_delete=models.CASCADE, default=None)
    last_bidder = models.ForeignKey(User, related_name='last_bidder', on_delete=models.CASCADE, default=None)

    def __str__(self):
        return f"{self.title}" f"{self.description}"
    
    def to_dict(self):
        return{
            'id':self.id,
            'start_bid':self.start_bid,
            'bid':self.bid,
            'title':self.title,
            'description':self.description,
            'image': self.image.url if self.image else None,
            'bid_time_finish':self.bid_time_finish,
            'bought':self.bought,
            'owner_id': self.owner.id,
            'owner': self.owner.username,
            'last_bidder_id': self.last_bidder.id,
            'last_bidder': self.last_bidder.username,
        }

class Messages(models.Model):
    question_message = models.CharField(max_length=500)
    time_sent = models.DateTimeField(auto_now_add=True)
    sender = models.ForeignKey(User, related_name='sent_messages', on_delete=models.CASCADE)
    receiver = models.ForeignKey(User, related_name='received_messages', on_delete=models.CASCADE)
    item = models.ForeignKey(Item, related_name='related_messages', on_delete=models.CASCADE, default=None)

    def __str__(self):
        return f"Message from {self.sender} to {self.receiver} about {self.item.title}"

    def to_dict(self):
        return {
            'id': self.id,
            'text': self.question_message,
            'time_sent': self.time_sent,
            'sender_id': self.sender.id,
            'sender': self.sender.username,
            'recipient_id': self.receiver.id,
            'recipient': self.receiver.username,
            'item_id': self.item.id,
            'item': self.item.title,
        }


