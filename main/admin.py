from django.contrib import admin
from .models import Needy, Child, StatusHome,ExportationData
from datetime import datetime
# Register your models here.



class TabularInlineChild(admin.TabularInline):
    model=Child

class NeedyAdmin(admin.ModelAdmin):
    inlines = [TabularInlineChild,]
    readonly_fields = ('childTotal',)
    list_display = ('name','phone','status','address','iin','childTotal')
    list_filter = ['status','statusHome','isDeadMan']
    list_editable = ('status',) 
    

admin.site.register(Needy, NeedyAdmin)
admin.site.register(Child)
admin.site.register(StatusHome)
admin.site.register(ExportationData)