from shlex import split
from os.path import join, abspath
from django.shortcuts import render, get_object_or_404, redirect
from django.db.models import Q
from django.urls import reverse
from functools import reduce
from django.http import FileResponse, Http404, HttpResponse, HttpResponseRedirect
from django.contrib.auth.models import Group
from django.contrib.auth.decorators import permission_required, user_passes_test
from django.contrib.auth import logout
from operator import __or__, __and__

from .utils import check_docx, chunks, check_images, keyword_helper, get_printer_info
from .forms import InputForm, SearchForm, TonerForm
from .models import Entry, Team, Facility, InfoType, Document, Keyword, Printer, Toner
from EnjetITWiki.settings import MEDIA_ROOT, STATIC_URL


def home(request):
    """View Function for home page of site."""
    num_entries = Entry.objects.all().count()
    all_facilities = Facility.objects.all()
    all_info_types = InfoType.objects.all()
    num_facilities = Facility.objects.all().count()
    num_info_types = InfoType.objects.all().count()

    pop_entries = Entry.objects.all().order_by("impressions").reverse()

    if(num_facilities > num_info_types):
        larger_count = num_facilities
    else:
        larger_count = num_info_types
    larger_count = range(0,larger_count)
    context = {
        'num_entries': num_entries,
        'all_facilities': all_facilities,
        'all_info_types': all_info_types,
        'larger_count': larger_count,
        'num_facilities': num_facilities,
        'num_info_types': num_info_types,
        'pop_entries':pop_entries
    }
    return render(request, 'home.html', context=context)

@permission_required("Wiki.view_entry")
def entry_detail_view(request, primary_key):
    entry = get_object_or_404(Entry, pk = primary_key)
    entry.impressions =+ 1
    entry.save()
    document_pk = None
    if(entry.document != None):
        document_pk = entry.document.pk

    access = False
    for g in request.user.groups.all():
        if(g == entry.group): 
            access = True
    if (access == False):
        return redirect(reverse('login') + '?next=/Wiki/entry/' + str(primary_key))
    htmlfile = ''
    return render(request, 'entry/entry_detail.html', context={'entry': entry, 'htmlfile': htmlfile, 'document_pk':document_pk, 'primary_key':primary_key})

@permission_required("Wiki.authenticated")
def facility_detail_view(request, primary_key):
    facility = get_object_or_404(Facility, pk = primary_key)
    entry_list = facility.entry_set.all()
    all_cols = list(chunks(entry_list))
    length = range(0, len(all_cols[0]))
    lens = [len(all_cols[0]),len(all_cols[1]),len(all_cols[2]),len(all_cols[3])]
    return render(request, 'facility/facility_detail.html', context={'all_cols':all_cols, 'length':length, 'lens':lens, 'facility':facility})

@permission_required("Wiki.authenticated")
def infotype_detail_view(request, primary_key):    
    infotype = get_object_or_404(InfoType, pk = primary_key)
    entry_list = infotype.entry_set.all()
    all_cols = list(chunks(entry_list))
    length = range(0, len(all_cols[0]))
    lens = [len(all_cols[0]),len(all_cols[1]),len(all_cols[2]),len(all_cols[3])]
    return render(request, 'infotype/infotype_detail.html', context={'all_cols':all_cols, 'length':length, 'lens':lens, 'infotype':infotype})

@permission_required("Wiki.authenticated")
def team_detail_view(request, primary_key):
    team = get_object_or_404(InfoType, pk = primary_key)
    return render(request, 'department/department_detail.html', context={'team': team})

@permission_required("Wiki.authenticated")
def entry_list_view(request):
    entry_list = Entry.objects.all().order_by('topic')
    
    entry_list_temp = Entry.objects.none()
    for g in request.user.groups.all():
        entry_list_temp = entry_list_temp | entry_list.filter(group__exact=g)

    entry_list = entry_list_temp
    all_cols = list(chunks(entry_list))
    length = range(0, len(all_cols[0]))
    lens = [len(all_cols[0]),len(all_cols[1]),len(all_cols[2]),len(all_cols[3])]
    return render(request, 'entry/entry.html', context={'all_cols':all_cols, 'length':length, 'lens':lens})

@permission_required("Wiki.authenticated")
def facility_list_view(request):
    facility_list = Facility.objects.all().order_by('name')
    all_cols = list(chunks(facility_list))
    length = range(0, len(all_cols[0]))
    lens = [len(all_cols[0]),len(all_cols[1]),len(all_cols[2]),len(all_cols[3])]
    return render(request, 'facility/facility.html', context={'all_cols':all_cols, 'length':length, 'lens':lens})

@permission_required("Wiki.authenticated")
def infotype_list_view(request):
    infotype_list = InfoType.objects.all().order_by('name')
    all_cols = list(chunks(infotype_list))
    length = range(0, len(all_cols[0]))
    lens = [len(all_cols[0]),len(all_cols[1]),len(all_cols[2]),len(all_cols[3])]
    return render(request, 'infotype/infotype.html', context={'all_cols':all_cols, 'length':length, 'lens':lens})

@permission_required("Wiki.edit_entry")
def upload_dialog(request):
    title = "Create New Entry"
    helper = "Use this form to create a new entry on the wiki."
    if request.method == "POST":
        form = InputForm(request.POST, request.FILES)
        if form.is_valid():
            file = form.cleaned_data.get("document")
            
            entry_exist = Entry.objects.filter(topic__exact=form.data['topic'])
            if entry_exist:
                return HttpResponseRedirect("/Wiki/entry/" + str(entry_exist[0].pk))
            
            keys_qs = keyword_helper(form.data['keywords'])

            new_document = check_docx(file)
            new_entry = Entry.objects.create(
                topic = form.data['topic'],
                facility = Facility.objects.get(id=form.data['facility']),
                infotype = InfoType.objects.get(id=form.data['infoType']),
                team = Team.objects.get(id=form.data['team']),
                group = Group.objects.get(id=form.data['group']),
                author = request.user,
                summary = form.data['summary'],
            )
            new_entry.keywords.set(keys_qs)
            if(new_document!=None): 
                new_entry.document = Document.objects.get(id=new_document.pk)
            new_entry.save()

            return HttpResponseRedirect("/Wiki/entry/" + str(new_entry.pk))
    else:
        form = InputForm()
    return render(request, 'upload/upload.html',{"form":form, "isNew":True, "title":title, "helper":helper})

@permission_required("Wiki.edit_entry")
def edit_dialog(request, primary_key):
    entry = get_object_or_404(Entry, pk=primary_key)
    title = "Edit Existing Entry: " + entry.topic
    helper = "Use this form to edit an existing entry on the wiki."
    if request.method == "POST":
        form = InputForm(request.POST, request.FILES)
        if form.is_valid():
            file = form.cleaned_data.get("document")
            
            keys_qs = keyword_helper(form.data['keywords'])

            new_document = check_docx(file)

            entry.topic = form.data['topic']
            entry.facility = Facility.objects.get(pk=form.data['facility'])
            entry.infotype = InfoType.objects.get(pk=form.data['infoType'])
            entry.team = Team.objects.get(pk=form.data['team'])
            entry.group = Group.objects.get(pk=form.data['group'])
            entry.summary = form.data['summary']
            entry.keywords.set(keys_qs)
            if(new_document!=None): 
                Document.objects.get(id=entry.document).delete
                entry.document = Document.objects.get(id=new_document.pk)

            entry.save()

            return HttpResponseRedirect("/Wiki/entry/" + str(entry.pk))
    else:
        form = InputForm(initial={
            'topic' : entry.topic, 
            'facility' : entry.facility.pk, 
            'infoType' : entry.infotype.pk,
            'team' : entry.team.pk,
            'group' : entry.group.pk,
            'summary' : entry.summary,
            'keywords' : ', '.join(x.keyword for x in entry.keywords.all())
            })
    return render(request, 'upload/upload.html',{"form":form,"isNew":False,"title":title, "helper":helper, "entry":primary_key})

@permission_required("Wiki.authenticated")
def search_bar_query(request):
    form = SearchForm(request.POST)
    query = request.GET.get('q') 
    facility = None
    infotype = None 
    team = None
    advSearch = None
    if request.method == "POST":
        form = SearchForm(request.POST)
        if form.is_valid():
            query = form.data['search']
            facility = form.data['facility']
            infotype = form.data['infoType']
            team = form.data['team']
            advSearch = form.data.get('advSearch', False)
    
    entry_list = Entry.objects.all().order_by('topic')
    
    query = split(query)
    if query:
        if advSearch:
            key_query = Keyword.objects.filter(reduce(__or__, (Q(keyword__iexact=x) for x in query)))
            entry_list = (entry_list & ((Entry.objects.filter(keywords__in=key_query))
                                |(Entry.objects.filter(reduce(__and__, (Q(topic__icontains=x) for x in query))))
                                |(Entry.objects.filter(reduce(__and__, (Q(summary__icontains=x) for x in query))))
                                )).distinct()    
        else:
            key_query = Keyword.objects.filter(reduce(__or__, (Q(keyword__iexact=x) for x in query)))
            entry_list = (entry_list & ((Entry.objects.filter(keywords__in=key_query))
                                |(Entry.objects.filter(reduce(__and__, (Q(topic__icontains=x) for x in query))))
                                )).distinct()

    if((facility != '') & (facility != None)):
        entry_list = entry_list.filter(facility__exact=facility)
    if((infotype != '') & (infotype != None)):
        entry_list = entry_list.filter(infotype__exact=infotype)
    if((team != '') & (team != None)):
        entry_list = entry_list.filter(team__exact=team)
    
    entry_list_temp = entry_list.none()
    
    print(entry_list_temp)

    for g in request.user.groups.all():
        entry_list_temp = entry_list_temp | entry_list.filter(group__exact=g)
        print(g)
        print(entry_list_temp)

    entry_list = entry_list_temp

    all_cols = list(chunks(entry_list))
    length = range(0, len(all_cols[0]))
    lens = [len(all_cols[0]),len(all_cols[1]),len(all_cols[2]),len(all_cols[3])]
    return render(request, 'search/search.html', context={'all_cols':all_cols, 'length':length, 'lens':lens, 'form':form})
    
@permission_required("Wiki.view_entry")    
def pdf_view(request, primary_key):
    document = get_object_or_404(Document, pk=primary_key)
    entry = Entry.objects.filter(document=document)[0]
    access = False
    for g in request.user.groups.all():
        if(g == entry.group): 
            access = True
    if (access == False):
        return redirect(reverse('login') + '?next=/Wiki/documents/' + str(primary_key))
    htmlfile = ''
    try:
        return FileResponse(document.file.open('rb'), content_type='application/pdf')
    except FileNotFoundError:
        raise Http404()

def logout_view(request):
    loggedIn = request.user.is_authenticated
    if loggedIn == True:
        logout(request)
        return redirect(reverse('login') + '?next=/Wiki/')

@user_passes_test(lambda u: u.is_superuser)
def delete_images(request):
    check_images()
    return redirect(reverse('home'))

@permission_required("Wiki.view_printer")
def printer_dca_facility_list(request):
    facility_list = Facility.objects.all().order_by('name')
    all_cols = list(chunks(facility_list))
    length = range(0, len(all_cols[0]))
    lens = [len(all_cols[0]),len(all_cols[1]),len(all_cols[2]),len(all_cols[3])]
    return render(request, 'printer/printer_facility.html', context={'all_cols':all_cols, 'length':length, 'lens':lens})

@permission_required("Wiki.view_printer")
def printer_dca_detail_list(request, primary_key):
    facility = get_object_or_404(Facility, pk=primary_key)
    printer_list = Printer.objects.filter(facility=facility).order_by('model')
    printers = list()
    for printer in printer_list:
        printers.append(printer.pk)

    length = range(0,len(printers))

    return render(request, 'printer/printer.html', {'printers':printers, 'length':length})

@permission_required("Wiki.view_printer")
def printer_dca_single_detail(request, primary_key):
    printer = get_object_or_404(Printer, pk=primary_key)
    printerInfo = list()
    tonerQuantity = (Toner.objects.filter(facility=printer.facility) & Toner.objects.filter(model=printer.model)).first()
    info = get_printer_info(printer.IP)
    for oid, val in info:
            printerInfo.append((printer.name, oid, val))
    return render(request, 'printer/printer_detail.html', {'printer':printerInfo, 
                                                                 'blackToner':tonerQuantity.black,
                                                                 'cyanToner':tonerQuantity.cyan,
                                                                 'yellowToner':tonerQuantity.yellow,
                                                                 'magentaToner':tonerQuantity.magenta,
                                                                 'toner_key':tonerQuantity.pk,
                                                                 'printer_ip':printer.IP})

@permission_required("Wiki.edit_toner")
def printer_edit_toner(request, primary_key):
    toner = get_object_or_404(Toner, pk=primary_key) 
    if request.method == "POST":
        form = TonerForm(request.POST)
        if form.is_valid():
            toner.black = form.data['black']
            toner.cyan = form.data['cyan']
            toner.yellow = form.data['yellow']
            toner.magenta = form.data['magenta']
            toner.save()
    else:
        form = TonerForm(instance=toner)        
    return render(request, 'upload/upload_toner.html',{"form":form, "toner":toner.name, "primary_key":primary_key})

def custom_404(request, exception):
    return render(request, 'errors/404.html', status=404)
def custom_500(request):
    return render(request, 'errors/500.html', status=404)