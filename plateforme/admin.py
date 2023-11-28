from django.contrib import admin
from .models import Visiteur, Soumission
from django.utils.translation import gettext_lazy as _


admin.site.site_title = _("KENN SITE")
admin.site.site_header = _("KENN SITE")
admin.site.index_title = _("KENN SITE")

class VisiteurAdmin(admin.ModelAdmin):
    list_display = ('id', 'nom', 'prenom', 'structure', 'lieu_travail', 'telephone', 'email')
    list_filter = ('structure', 'lieu_travail')
    search_fields = ('nom', 'prenom',)

class SoumissionAdmin(admin.ModelAdmin):
    list_display = ('information', 'date_soumission')

# Register your models here.
admin.site.register(Visiteur, VisiteurAdmin)
admin.site.register(Soumission, SoumissionAdmin)
