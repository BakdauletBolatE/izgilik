from django.contrib import admin
from .models import Needy, Child, StatusHome
from datetime import datetime
# Register your models here.



class TabularInlineChild(admin.TabularInline):
    model=Child

class NeedyAdmin(admin.ModelAdmin):
    inlines = [TabularInlineChild,]
    readonly_fields = ('childTotal',)
    

admin.site.register(Needy, NeedyAdmin)
admin.site.register(Child)
admin.site.register(StatusHome)