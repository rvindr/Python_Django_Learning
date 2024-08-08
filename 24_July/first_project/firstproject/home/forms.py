from django import forms
from .models import Student
# class StudentForm(forms.Form):

#     name = forms.CharField()
#     age = forms.IntegerField()
#     phone_number = forms.CharField()
#     dob = forms.DateField()
#     father_name = forms.CharField()

class StudentForm(forms.ModelForm):
    class Meta:
        model = Student
        fields = '__all__'