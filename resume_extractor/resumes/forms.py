from django import forms

class MultiFileInput(forms.ClearableFileInput):
    allow_multiple_selected = True #for handling multiple files
class UploadFilesForm(forms.Form):
    files = forms.FileField(
        widget=MultiFileInput(attrs={'multiple': True}),
        required=True
    )
