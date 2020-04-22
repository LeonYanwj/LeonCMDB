from django.forms import forms

class FileUploadForm(forms.Form):
    agentMessFile = forms.FileField()