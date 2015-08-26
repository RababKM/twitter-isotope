from django.db import models

# Create your models here.

class Tweet(models.Model):
    user = models.CharField(max_length=255)
    text = models.TextField(null=True)
    image = models.ImageField(upload_to='tweet_images', default='tweet_image.jpg')
    search = models.CharField(max_length=255)

    def __unicode__(self):
        return self.user