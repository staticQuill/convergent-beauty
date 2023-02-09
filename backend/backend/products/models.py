from django.contrib.auth.models import User
from django.contrib.postgres.fields import ArrayField, HStoreField
from django.db import models
from django.utils.translation import gettext_lazy as translate


class Sentiment(models.Model):
    class Type(models.TextChoices):
        WRONG_LOOK = "looks wrong", translate("looks wrong")
        GOOD_LOOK = "looks good", translate("looks good")
        LIKED = "liked", translate("liked")
        DISLIKED = "disliked", translate("disliked")
        NEUTRAL = "neutral", translate("neutral")
    name = models.CharField(max_length=15, choices=Type.choices)


class Enjoyment(models.Model):
    class Type(models.TextChoices):
        PLEASANT = "pleasant", translate("pleasant")
        UNPLEASANT = "unpleasant", translate("unpleasant")
        NEUTRAL = "neutral", translate("neutral")
        OVERPOWERING = "overpowering", translate("overpowering")
    name = models.CharField(max_length=15, choices=Type.choices)


class Texture(models.Model):
    class Type(models.TextChoices):
        STICKY = "sticky", translate("sticky")
        SMOOTH = "smooth", translate("smooth")
        SLIMY = "slimy", translate("slimy")
        CAKEY = "cakey", translate("cakey")
        ROUGH = "rough", translate("rough")
        WET = "wet", translate("wet")
    name = models.CharField(max_length=15, choices=Type.choices)


class Scent(models.Model):
    class Type(models.TextChoices):
        Fruity = "sticky", translate("sticky")
        SMOOTH = "smooth", translate("smooth")
        SLIMY = "slimy", translate("slimy")
        CAKEY = "cakey", translate("cakey")
        ROUGH = "rough", translate("rough")
        WET = "wet", translate("wet")
    name = models.CharField(max_length=15, choices=Type.choices)


class Brand(models.Model):
    brand_id = models.CharField(max_length=8, primary_key=True)
    name = models.CharField(max_length=100)


class Product(models.Model):
    brand = models.ForeignKey(Brand, on_delete=models.PROTECT)
    model = models.CharField(max_length=150)
    texture_ratings = HStoreField()
    scent_ratings = HStoreField()
    sentiment_ratings = HStoreField()


class UserProduct(models.Model):
    product = models.ForeignKey(Product, on_delete=models.PROTECT)
    user = models.ForeignKey(User, on_delete=models.PROTECT)
    custom_notes = models.CharField(max_length=500)
    texture_notes = ArrayField(models.ManyToManyField(Texture))
    texture_enjoyment = ArrayField(models.ManyToManyField(Enjoyment))
    scent_notes = ArrayField(models.ManyToManyField(Scent))
    scent_enjoyment = ArrayField(models.ManyToManyField(Enjoyment))
    overall_sentiments = ArrayField(models.ManyToManyField(Sentiment))
