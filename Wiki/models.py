import os

from django.db import models
from django.urls import reverse
from django.dispatch import receiver
from django.contrib.auth.models import Group
from django.contrib.auth.models import User
from ckeditor_uploader.fields import RichTextUploadingField

class Toner(models.Model):
    name = models.CharField(max_length=200, help_text='Enter Toner Name')
    model = models.ForeignKey('PrinterModel',on_delete=models.SET_NULL, null=True, help_text='What is the model of this printer?')
    facility = models.ForeignKey('Facility',on_delete=models.SET_NULL, null=True, help_text='What facility does this information pertain to?')
    yellow = models.IntegerField(help_text='Yellow Ink')
    magenta = models.IntegerField(help_text='Magenta Ink')
    cyan = models.IntegerField(help_text='Cyan Ink')
    black = models.IntegerField(help_text='Black Ink')

    def __str__(self):
        """String for representing printer"""
        return self.name


class Printer(models.Model):
    name = models.CharField(max_length=200, help_text='Enter Name')
    IP = models.CharField(max_length=40, help_text='Enter Printer IP')
    facility = models.ForeignKey('Facility',on_delete=models.SET_NULL, null=True, help_text='What facility does this information pertain to?')
    model = models.ForeignKey('PrinterModel',on_delete=models.SET_NULL, null=True, help_text='What is the model of this printer?')

    def get_absolute_url(self):
        return reverse('printer-detail', args=[str(self.id)])

    def __str__(self):
        """String for representing printer"""
        return self.name

class PrinterModel(models.Model):
    """Model representing the make/model of printer"""
    name = models.CharField(max_length=200, help_text='Enter printer model')

    def get_absolute_url(self):
        return reverse('printer-model-detail', args=[str(self.id)])
    
    def __str__(self):
        """String for representing facility"""
        return self.name
    

class Facility(models.Model):
    """Model representing facility the topic may be about"""
    name = models.CharField(max_length=200, help_text='Enter facility name (e.g. Overland Park, Terre Haute, N/A)')

    def get_absolute_url(self):
        return reverse('facility-detail', args=[str(self.id)])
    
    def get_dca_url(self):
        return reverse('printer-dca-detail-list', args=[str(self.id)])
    
    def __str__(self):
        """String for representing facility"""
        return self.name

class InfoType(models.Model):
    """Model representing what type of information is being relayed in the post"""
    name = models.CharField(max_length=200, help_text='Enter Information Type (e.g. General, Software, Network)')
    
    def get_absolute_url(self):
        return reverse('infotype-detail', args=[str(self.id)])

    def __str__(self):
        """String for representing infotype"""
        return self.name
    
class Team(models.Model):
    """Model representing which team this information relates to"""
    team = models.CharField(max_length=200, help_text='Enter the team this information relates to')
    
    def get_absolute_url(self):
        return reverse('team-detail', args=[str(self.id)])

    def __str__(self):
        return self.team
    
class Keyword(models.Model):
    keyword = models.CharField(max_length=200, help_text='Enter One Keyword/keyphrase')

    def get_absolute_url(self):
        return reverse('keyword-detail', args=[str(self.id)])
    
    def __str__(self):
        return self.keyword

class Entry(models.Model):
    """Model representing a website entry"""

    topic = models.CharField(max_length=200, help_text='Enter a topic for this entry (e.g. Installing Windows)')

    
    infotype = models.ForeignKey('InfoType', on_delete=models.SET_NULL, null=True, help_text='What sort of information does this entry contain?')
    facility = models.ForeignKey('Facility',on_delete=models.SET_NULL, null=True, help_text='What facility does this information pertain to?')
    team = models.ForeignKey('Team', on_delete=models.SET_NULL, null=True, help_text='What team does this information pertain to?')
    group = models.ForeignKey(Group, on_delete=models.SET_NULL, null=True, help_text='Which groups should have access to this information?')
    author = models.ForeignKey(User, on_delete=models.SET_NULL, null=True ,help_text='Who created this information?')

    date_published = models.DateField(auto_now=True)
    date_modified = models.DateField(auto_now_add=True)

    summary = RichTextUploadingField(max_length=100000, blank=True, help_text='Enter a brief description of the information included in this post.')
    
    document = models.ForeignKey('Document', blank=True, on_delete=models.SET_NULL, null=True, help_text='Upload a PDF or DOCX file.')

    keywords = models.ManyToManyField('Keyword', blank=True, help_text='Enter keywords with a comma separation.')

    def get_absolute_url(self):
        return reverse('entry-detail', args=[str(self.id)])

    def __str__(self):
        """String for representing the object"""
        return self.topic
    
class Document(models.Model):
    file = models.FileField(upload_to='', max_length=100000, null=True)

@receiver(models.signals.post_delete, sender=Entry)
def auto_delete_document_on_delete(sender, instance, **kwargs):
    """
    Deletes Document key from database 
    When corresponding 'Entry' is deleted
    """
    if instance.document:
        instance.document.delete()

@receiver(models.signals.post_delete, sender=Document)
def auto_delete_file_on_delete(sender, instance, **kwargs):
    """
    Deletes file from filesystem
    when corresponding `MediaFile` object is deleted.
    """
    if instance.file:
        if os.path.isfile(instance.file.path):
            os.remove(instance.file.path)

"""
@receiver(models.signals.pre_save, sender=Document)
def auto_delete_file_on_change(sender, instance, **kwargs):
    """"""
    Deletes old file from filesystem
    when corresponding `MediaFile` object is updated
    with new file.
    """"""
    if not instance.pk:
        return False

    try:
        old_file = Document.objects.get(pk=instance.pk).file
    except Document.DoesNotExist:
        return False

    new_file = instance.file
    if not old_file == new_file:
        if os.path.isfile(old_file.path):
            os.remove(old_file.path)

"""