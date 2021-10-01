from django.db import models
from django.db.models.fields.related import ForeignKey

# Create your models here.


class Address(models.Model):
    address = models.CharField(max_length=42)


class Event(models.Model):
    from_address = ForeignKey(
        Address, on_delete=models.CASCADE, related_name='from_address')
    to_address = ForeignKey(
        Address, on_delete=models.CASCADE, related_name='to_address')
    value = models.IntegerField()


class Block(models.Model):
    block_height = models.IntegerField()


class ContractAddress(models.Model):
    address = models.CharField(max_length=42)
    ticker_symbol = models.CharField(max_length=100)
    synced_block_height = models.IntegerField()
