from django.urls import path
from . import views

urlpatterns = [
    path('', views.home, name='home'),
    path('search', views.search_bar_query),
    path('facility/', views.facility_list_view, name='facilities'),
    path('facility/<int:primary_key>', views.facility_detail_view, name='facility-detail'),
    path('infotype/', views.infotype_list_view, name='infotype'),
    path('infotype/<int:primary_key>', views.infotype_detail_view, name='infotype-detail'),
    path('entry/', views.entry_list_view, name='index'),
    path('entry/<int:primary_key>', views.entry_detail_view, name='entry-detail'),
    path('upload/', views.upload_dialog, name='upload'),
    path('edit/<primary_key>', views.edit_dialog, name='edit'),
    path('documents/<primary_key>', views.pdf_view, name="pdf_template"),
    path('logout/', views.logout_view, name='logout_view'),
    path('images/delete/',  views.delete_images, name='delete_images'),
    path('printer/', views.printer_dca_facility_list, name='printer-dca-facility-list'),
    path('printer/<int:primary_key>/', views.printer_dca_detail_list, name='printer-dca-detail-list'),
    path('printer/detail/<int:primary_key>/', views.printer_dca_single_detail, name='printer-dca-detail-single'),
    path('edittoner/<int:primary_key>/', views.printer_edit_toner, name='edit-toner')
]