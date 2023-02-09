from django.contrib.auth.models import User
from django.contrib.postgres.fields import ArrayField, HStoreField
from django.db import models
from django.db.migrations import Migration
from django.utils.translation import gettext_lazy as translate

from django.contrib.postgres.operations import HStoreExtension


class Migration(Migration):
    operations = [
        HStoreExtension(),
    ]


class Brand(models.Model):
    name = models.CharField(max_length=100)


class Product(models.Model):
    brand = models.ForeignKey(Brand, on_delete=models.PROTECT)
    name = models.CharField(max_length=150)
    texture_ratings = HStoreField()
    scent_ratings = HStoreField()
    sentiment_ratings = HStoreField()


class UserProduct(models.Model):
    class Sentiment(models.TextChoices):
        WRONG_LOOK = "looks wrong", translate("looks wrong")
        GOOD_LOOK = "looks good", translate("looks good")
        LIKED = "liked", translate("liked")
        DISLIKED = "disliked", translate("disliked")
        NEUTRAL = "neutral", translate("neutral")

    class Enjoyment(models.TextChoices):
        PLEASANT = "pleasant", translate("pleasant")
        UNPLEASANT = "unpleasant", translate("unpleasant")
        NEUTRAL = "neutral", translate("neutral")
        OVERPOWERING = "overpowering", translate("overpowering")

    class Texture(models.TextChoices):
        STICKY = "sticky", translate("sticky")
        SMOOTH = "smooth", translate("smooth")
        SLIMY = "slimy", translate("slimy")
        CAKEY = "cakey", translate("cakey")
        ROUGH = "rough", translate("rough")
        WET = "wet", translate("wet")

    class Scent(models.TextChoices):
        FRUITY = "fruity", translate("fruity")
        CLEAN = "clean", translate("clean")
        FLORAL = "floral", translate("floral")
        SWEET = "sweet", translate("sweet")

    user_product_id = models.CharField(max_length=8, primary_key=True)
    product = models.ForeignKey(Product, on_delete=models.PROTECT)
    user = models.ForeignKey(User, on_delete=models.PROTECT)
    custom_notes = models.CharField(max_length=500)
    texture_notes = ArrayField(models.CharField(max_length=15, choices=Texture.choices))
    texture_enjoyment = ArrayField(models.CharField(max_length=15, choices=Enjoyment.choices))
    scent_notes = ArrayField(models.CharField(max_length=15, choices=Scent.choices))
    scent_enjoyment = ArrayField(models.CharField(max_length=15, choices=Enjoyment.choices))
    overall_sentiments = ArrayField(models.CharField(max_length=15, choices=Sentiment.choices))
