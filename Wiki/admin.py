from django.contrib import admin

# Register your models here.

from .models import Facility, InfoType, Team, Entry, Document, Keyword, Printer, PrinterModel, Toner


admin.site.register(Facility)
admin.site.register(InfoType)
admin.site.register(Team)
admin.site.register(Entry)
admin.site.register(Document)
admin.site.register(Keyword)
admin.site.register(Printer)
admin.site.register(PrinterModel)
admin.site.register(Toner)