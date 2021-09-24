from django.contrib import admin
from .models import Needy, Child, StatusHome,ExportationData,Region

# Register your models here.



class TabularInlineChild(admin.TabularInline):
    model=Child


class NeedyAdmin(admin.ModelAdmin):
    inlines = [TabularInlineChild,]
    readonly_fields = ('childTotal','owner','changed_onwer')
    list_display = ('name','phone','status','address','iin','childTotal')
    list_filter = ['status','statusHome','isDeadMan','region']
    list_editable = ('status',) 
    search_fields = ('name', 'surName', 'iin',)

    def save_model(self, request, obj, form, change):
        if obj.owner is None:     
            obj.owner = request.user
        else:
            obj.changed_onwer = request.user
        super(NeedyAdmin, self).save_model(request, obj, form, change)
    

admin.site.register(Needy, NeedyAdmin)
admin.site.register(Child)
admin.site.register(StatusHome)
admin.site.register(Region)
admin.site.register(ExportationData)