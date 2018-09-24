from django import forms

class AddGameForm(forms.Form):
    name = forms.CharField(label='Name', max_length=100,
                               widget=forms.TextInput(attrs={'class': 'form-control', 'name': 'name', 'placeholder':'Enter Game Name'}))
    price = forms.FloatField(label='price',
                               widget=forms.TextInput(attrs={'class': 'form-control', 'name': 'price', 'placeholder':'Enter Price'}))
    url = forms.CharField(label='url', max_length=100,
                               widget=forms.TextInput(attrs={'class': 'form-control', 'name': 'url', 'placeholder':'Enter Game URL'}))
    imagepath = forms.CharField(label='Image Path', max_length=100,
                               widget=forms.TextInput(attrs={'class': 'form-control', 'name':'imagepath', 'placeholder':'Enter Game Image URL'}))
    description = forms.CharField(label='Description', max_length=100,
                               widget=forms.Textarea(attrs={'class': 'form-control', 'name':'description', 'placeholder':'Enter Game description'}))

class EditGameForm(forms.Form):
    title = forms.CharField(label='title', max_length=100,
                               widget=forms.TextInput(attrs={'class': 'form-control', 'name': 'title'}))
    price = forms.FloatField(label='price',
                               widget=forms.TextInput(attrs={'class': 'form-control', 'name': 'price'}))
    game_url = forms.CharField(label='url', max_length=100,
                               widget=forms.TextInput(attrs={'class': 'form-control', 'name': 'url'}))
    thumbnail_url = forms.CharField(label='Imagepath', max_length=100,
                               widget=forms.TextInput(attrs={'class': 'form-control', 'name':'imagepath'}))
    description = forms.CharField(label='Description', max_length=100,
                               widget=forms.Textarea(attrs={'class': 'form-control', 'name':'description'}))
