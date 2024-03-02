from django import forms


class CreateComment(forms.Form):

    rating = forms.IntegerField(widget=forms.TextInput(
        attrs={'class': "field", 'id': "form-rating", 'placeholder': "Введите вашу оценку (1-10)", 'data-min': "1",
               'data-max': "5"}))

    text = forms.CharField(widget=forms.Textarea(attrs={'id': "form-text", 'cols': "30", 'rows': "10"}))
