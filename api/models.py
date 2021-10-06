from django.db import models
from django.db.models.fields.related import ForeignKey, ManyToManyField

# Create your models here.


class Address(models.Model):
    address = models.CharField(max_length=42)

    def __str__(self):
        return str(self.address)


class LogEvent(models.Model):
    from_address = ForeignKey(
        Address, on_delete=models.CASCADE, related_name='from_address')
    to_address = ForeignKey(
        Address, on_delete=models.CASCADE, related_name='to_address')
    # IntegerField and BigInt cannot hold ethereum values
    value = models.DecimalField(max_digits=30, decimal_places=0)

    def __str__(self):
        return str(self.value)


class Block(models.Model):
    block_height = models.IntegerField()
    events = ManyToManyField(LogEvent)

    def __str__(self):
        return str(self.block_height)


class ContractAddress(models.Model):
    address = models.CharField(max_length=42)
    ticker_symbol = models.CharField(max_length=100)
    deployed_block = models.IntegerField()
    synced_block_height = models.IntegerField()

    def __str__(self):
        return str(self.ticker_symbol) + " | " + str(self.address)


class SyncedProgress(models.Model):
    contract_address = ForeignKey(ContractAddress, on_delete=models.CASCADE)
    synced_block_height = models.IntegerField()
    syncing = models.BooleanField(default=False)

    def __str__(self):
        return str(self.contract_address.ticker_symbol) + " | " + str(self.contract_address.address)
