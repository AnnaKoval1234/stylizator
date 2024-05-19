from django import forms
 
class TextAreaForm(forms.Form):
    text = forms.CharField(widget=forms.Textarea(attrs={"placeholder": "Введите текст"}), label="")
