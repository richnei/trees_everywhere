from django import forms
from .models import PlantedTree, Account

class PlantedTreeForm(forms.ModelForm):
    class Meta:
        model = PlantedTree
        fields = ['tree', 'account', 'age', 'location_lat', 'location_lon']

    def __init__(self, *args, **kwargs):
        user = kwargs.pop('user')  # get the logged-in user
        super().__init__(*args, **kwargs)
        # Limit accounts to those the user belongs to
        self.fields['account'].queryset = Account.objects.filter(users=user)
