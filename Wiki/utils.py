import uuid
import math
import os
import sys
import glob
from pysnmp.entity.rfc3413.oneliner import cmdgen
from pysnmp.hlapi import *
from docx2pdf import convert as docxToPDF
from django.core.files.storage import default_storage
from django.core.files.base import ContentFile
from os import remove
from os.path import join,splitext

from .models import Document, Entry, Keyword
from EnjetITWiki.settings import MEDIA_ROOT

def check_docx(file):
    if(file == None):
        return
    filename, fileext = splitext(file.name)
    pdf_file_name = str(uuid.uuid4()) + ".pdf"
    if(fileext == ".docx"):
        path = default_storage.save('tmp/' + file.name, ContentFile(file.read()))
        tmp_file = join(MEDIA_ROOT, path)
        new_document = convertToPDF(tmp_file, pdf_file_name)
        new_document.save()
        remove(tmp_file)
        return new_document
    if(fileext == ".pdf"):
        new_document = Document.objects.create()
        path = default_storage.save(pdf_file_name, ContentFile(file.read()))
        new_document.file = pdf_file_name
        print(new_document.file)
        new_document.save()
        return new_document

def convertToPDF(doc, filename):
    wdFormatPDF = 17
    in_file = os.path.abspath(doc)
    out_file = os.path.abspath(MEDIA_ROOT + filename)
    
    docxToPDF(in_file, out_file)
    new_document = Document.objects.create()
    new_document.file = filename
    return new_document

def chunks(lst):
    """Yield successive n-sized chunks from lst."""
    list_num = math.ceil(len(lst) / 4)
    if(list_num == 0):
        list_num = 1
    for i in range(0, len(lst), list_num):
        yield lst[i:i + list_num]
    for i in range(0, 4):
        yield []

def get_filename(filename, request):
    return filename.upper()

def check_images():
    all_entries = Entry.objects.all()
    all_images = glob.glob(MEDIA_ROOT + "ck_uploads/**/*.*", recursive=True)
    all_images_dict = {}
    for index, element in enumerate(all_images):
        all_images_dict[index] = element.replace('\\', '/')

    for x in all_entries:
        for key in list(all_images_dict):
            if x.summary.__contains__(all_images_dict[key]):
                del all_images_dict[key]

    for x in all_images_dict:
        os.remove(all_images_dict[x])

def keyword_helper(formdata):
    keys = [x.strip() for x in formdata.split(',')]
    list_ids = []
    for x in keys:
        if x == '': continue
        curKey = Keyword.objects.filter(keyword__iexact=x)
        if not curKey:
            curKey = Keyword.objects.create(keyword=x)
            list_ids.append(curKey.id)
        else:
            list_ids.append(curKey[0].id)
    
    keys_qs = Keyword.objects.filter(id__in=list_ids)

    return keys_qs

def get_printer_info(host):

    response = os.popen(f"ping -n 1 {host} ").read()
    print(response)
    if("Destination host unreachable") in response:
        return

    oid='1.3.6.1.2.1.43.11.1.1.9.1'

    # Query a network device using the getCmd() function, providing the auth object, a UDP transport
    # our OID for SYSNAME, and don't lookup the OID in PySNMP's MIB's
    for (errorIndication,
         errorStatus,
         errorIndex,
         varBinds) in nextCmd(SnmpEngine(),
                                CommunityData('public'),
                                UdpTransportTarget((host, 161)),
                                ContextData(),
                                ObjectType(ObjectIdentity(oid)),
                                lookupMib=False,
                                lexicographicMode=False):
        if errorIndication:
            print(errorIndication, file=sys.stderr)
            break

        elif errorStatus:
            print('%s at %s' % (errorStatus.prettyPrint(),
                                errorIndex and varBinds[int(errorIndex) - 1][0] or '?'), file=sys.stderr)
            break

        else:
            for oid,val in varBinds:
                 yield(oid.prettyPrint(), val.prettyPrint())