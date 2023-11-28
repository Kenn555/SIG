from django.contrib import admin
from .models import Visiteur, Soumission
from django.utils.translation import gettext_lazy as _


admin.site.site_title = _("Ministère de Santé Publique")
admin.site.site_header = _("Administration")
admin.site.index_title = _("Tables")

class VisiteurAdmin(admin.ModelAdmin):
    list_display = ('nom', 'prenom', 'structure', 'lieu_travail', 'telephone', 'email')
    list_filter = ('structure', 'lieu_travail')
    search_fields = ('nom', 'prenom',)

class SoumissionAdmin(admin.ModelAdmin):
    list_display = ('information', 'date_soumission')
    list_filter = ('information',)

# Register your models here.
admin.site.register(Visiteur, VisiteurAdmin)
admin.site.register(Soumission, SoumissionAdmin)
