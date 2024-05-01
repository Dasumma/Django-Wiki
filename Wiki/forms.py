from django import forms

from .models import Team, Facility, InfoType, Toner
from django.contrib.auth.models import Group
from ckeditor_uploader.widgets import CKEditorUploadingWidget

class InputForm(forms.Form):
    topic = forms.CharField(max_length=100)
    facility = forms.ModelChoiceField(queryset=Facility.objects.all())
    infoType = forms.ModelChoiceField(queryset=InfoType.objects.all())
    team = forms.ModelChoiceField(queryset=Team.objects.all())
    group = forms.ModelChoiceField(queryset=Group.objects.all())
    summary = forms.CharField(widget=CKEditorUploadingWidget(), required=False)
    document = forms.FileField(required=False)
    keywords = forms.CharField(widget=forms.Textarea(attrs={'name':'keywords', 'rows':3, 'cols':40}), required=False)
    def __init__(self, *args, **kwargs):
        super(InputForm, self).__init__(*args, **kwargs)
        for visible in self.visible_fields():
            visible.field.widget.attrs['class'] = 'form-control'

class SearchForm(forms.Form):
    advSearch = forms.BooleanField(required=False, label="Advanced\nSearch")
    facility = forms.ModelChoiceField(queryset=Facility.objects.all(), required=False, label=False)
    infoType = forms.ModelChoiceField(queryset=InfoType.objects.all(), required=False, label=False)
    team = forms.ModelChoiceField(queryset=Team.objects.all(), required=False, label=False)
    search = forms.CharField(required=False, label=False)
    def __init__(self, *args, **kwargs):
        super(SearchForm, self).__init__(*args, **kwargs)
        for visible in self.visible_fields():
            visible.field.widget.attrs['class'] = 'form-control me-2 form-dan'
            self.fields['facility'].widget.attrs['placeholder'] = 'Facility'
            self.fields['infoType'].widget.attrs['placeholder'] = 'InfoType'
            self.fields['team'].widget.attrs['placeholder'] = 'Team'
            self.fields['search'].widget.attrs['placeholder'] = 'Search'
            self.fields['advSearch'].widget.attrs['placeholder'] = 'advSearch'
            self.fields['advSearch'].widget.attrs['class'] = 'form-check-input form-dan'

class TonerForm(forms.ModelForm):
    class Meta:
        model = Toner
        fields = ["black", "cyan", "magenta", "yellow"]