from django.contrib import admin

from .models import *

# Register your models here.
admin.site.register(Address)
admin.site.register(LogEvent)
admin.site.register(Block)
admin.site.register(ContractAddress)
admin.site.register(SyncedProgress)
