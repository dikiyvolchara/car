from django import forms
from .models import QuickOrderNewTire


class QuickOrderNewTireForm(forms.ModelForm):

    class Meta:
        model = QuickOrderNewTire
        fields = ('phone',)

        widgets={
            'phone':forms.TextInput(attrs={'placeholder':'прик.:0971234455', 'id':'inputTel', 'class':'form-control', 'type':'tel', 
            'pattern':'[0]{1}[4-9]{1}[3-9]{1}[0-9]{7}'}),
        }
