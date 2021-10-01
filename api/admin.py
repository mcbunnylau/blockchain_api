from django.contrib import admin

from .models import Address, Block, ContractAddress, Event

# Register your models here.
admin.site.register(Address)
admin.site.register(Event)
admin.site.register(Block)
admin.site.register(ContractAddress)
