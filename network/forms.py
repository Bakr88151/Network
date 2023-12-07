from django import forms

class new_post_form(forms.Form):
    content = forms.CharField(max_length=2064, required=True, widget=forms.Textarea(attrs={'class': 'content-input'}), label="")