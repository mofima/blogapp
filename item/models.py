from django.db import models
from django.contrib.auth.models import User 
from django.core.validators import MinLengthValidator
from django.core.exceptions import ValidationError

from ckeditor.fields import RichTextField
from sorl.thumbnail import ImageField
import readtime
from PIL import Image

class Category(models.Model):
    name = models.CharField(max_length=255)

    class Meta:
        verbose_name_plural = 'Categories'
        ordering = ('name',)

    def __str__(self):
        return self.name 
    

def validate_image_size(image):
    # mmaximum allowed image size
    max_size = 2 * 1024 * 1024 # 2MB

    if image.size > max_size:
        raise ValidationError("Max image size is 2 MB")    

class Article(models.Model):
    category = models.ForeignKey(Category, on_delete=models.CASCADE)
    topic = models.CharField(max_length=255)
    image = ImageField(upload_to='item_images', blank=True, null=True, validators=[validate_image_size])
    content = RichTextField(null=True, validators=[MinLengthValidator(9, "The content must be more than 9 characters long")])
    author = models.ForeignKey(User, on_delete=models.CASCADE)
    comments = models.ManyToManyField(User, through='Comment', related_name='comments_owned')
    created_at = models.DateTimeField(auto_now_add=True)  
    updated_at = models.DateTimeField(auto_now=True)

    def get_readtime(self):
        result = readtime.of_text(self.content)
        return result.text 
    
    def __str__(self):
        return self.topic
    
class Comment(models.Model):
    text = models.TextField(
            validators=[MinLengthValidator(2, "Comment must be greater than 2 characters")]
    )    
    article = models.ForeignKey(Article, on_delete=models.CASCADE)
    created_by = models.ForeignKey(User, on_delete=models.CASCADE)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        if len(self.text) < 15 : return self.text 
        return self.text[:11] + '...'

