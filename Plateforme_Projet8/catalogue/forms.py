from django import forms

class ConnexionForm(forms.Form):

	username = forms.CharField(label="username", max_length=30)
	password = forms.CharField(label="password", widget=forms.PasswordInput)



class AssociationForm(forms.Form):

	user = forms.IntegerField(label="user")
	product = forms.IntegerField(label="product")
	product_sub = forms.IntegerField(label="product_sub")