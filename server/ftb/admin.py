from ftb.models import Patient, Address, PatientDetails, FamilyHistory
from django.contrib import admin
from django.contrib.auth.models import Group
from django.contrib.auth.models import User as AuthUser
from django.contrib.sites.models import Site
from locking.admin import LockableAdmin

admin.site.unregister(AuthUser)
admin.site.unregister(Group)
admin.site.unregister(Site)

class PatientDetailsInline(admin.StackedInline):
    model = PatientDetails
    verbose_name = 'Patient Details'
    verbose_name_plural = 'Patient Details'
    template = 'admin/edit_inline/stacked_one2one.html'

class AddressInline(admin.StackedInline):
    model = Address
    verbose_name = 'Address'
    verbose_name_plural = 'Address'
    template = 'admin/edit_inline/stacked_one2one.html'

class FamilyHistoryInline(admin.StackedInline):
    model = FamilyHistory
    verbose_name = 'Family history'
    verbose_name_plural = 'Family history'
    template = 'admin/edit_inline/stacked_one2one.html'
    
class PatientAdmin(LockableAdmin):

    list_display = ('name', 'home_town', 'lock')
    search_fields = ('name', 'address__town')
    list_filter = ('address__town', 'details__sex')
    
    fieldsets = [
        (None, {'fields': ['name']}),
    ]
    inlines = [AddressInline, PatientDetailsInline, FamilyHistoryInline]

    def home_town(self, obj):
        return obj.address.town
    home_town.short_description = 'Town/Village'
    
admin.site.register(Patient, PatientAdmin)


