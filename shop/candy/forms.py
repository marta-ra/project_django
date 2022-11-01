from django import forms


class AddCandyAmount(forms.Form):

    amount = forms.FloatField()


class Order(forms.Form):

    firstname = forms.CharField(
        max_length=255,
        required=True)
    lastname = forms.CharField(
        max_length=255,
        required=True)
    email = forms.CharField(
        max_length=255,
        required=True)
    phone = forms.IntegerField(
        required=True)
    delivery_time = forms.DateField(widget=forms.SelectDateWidget)
    address = forms.CharField(
        max_length=255,
        required=True)
    comment = forms.CharField(
        max_length=255,
        required=False)
