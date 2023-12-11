import uuid
from django.db import models
from django.utils.text import slugify
from django.db.models.signals import pre_save
from producer.models import Producer
# Create your models here.
class Product(models.Model):
    title = models.CharField(max_length=50)
    description =models.TextField()
    price = models.DecimalField(max_digits=8, decimal_places=2, default=0.0) #12121.58
    slug = models.SlugField(null=False, blank=False, unique=True)
    created_at = models.DateTimeField(auto_now_add=True)
    image = models.ImageField(upload_to='products/', null=True, blank=False)
    stock = models.IntegerField(default=0)
    comments = models.JSONField(default=dict, null=True, blank=True)
    producer = models.ForeignKey(Producer, null=True, on_delete=models.CASCADE)

    def __str__(self):
        return self.title


def set_slug(sender, instance, *args, **kwargs):
    if instance.title and not instance.slug:
        slug = slugify(instance.title)
        while Product.objects.filter(slug=slug).exists():
            slug = slugify("{}-{}".format(instance.title,str(uuid.uuid4())[:8]))

        instance.slug = slug
pre_save.connect(set_slug, sender=Product)

