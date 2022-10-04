from django import forms
from ckeditor.fields import RichTextField
from ckeditor.widgets import CKEditorWidget

class docTypeForm(forms.Form):
    text = forms.CharField(widget=CKEditorWidget(), min_length=10)