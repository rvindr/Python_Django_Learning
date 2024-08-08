from django.shortcuts import render, redirect
from django.http import HttpResponse
from home.forms import StudentForm
from .models import StudentData, Student
from django.db.models import Q # it is used to search in data in different field

def index(request):

    if request.method == 'POST':
        
        data = StudentForm(request.POST)
        if data.is_valid():
            data.save()
            # print(f'Data Before cleaned {data}')
            # print(f'Data After cleaned {data.cleaned_data}')


            # name = data.cleaned_data['name']
            # age = data.cleaned_data['age']
            # phone_number = data.cleaned_data['phone_number']
            # dob = data.cleaned_data['dob']
            # father_name = data.cleaned_data['father_name']

            # StudentData.objects.create(
            #     name = name,
            #     age = age,
            #     phone_number = phone_number,
            #     dob = dob,
            #     father_name = father_name
            # )
            
        else:
            print(request.method)

        

    context = {
        'forms':StudentForm
    }
    return render(request,'index.html', context)
def contact(request):
    return HttpResponse("Thank you for contact us 😀")


def dynamic_route(request, number):
    print(type(number))
    return HttpResponse(f"You entered {number}")
    

def search_page(request):
    student = Student.objects.all()

    search = request.GET.get('search')
    age = request.GET.get('age')

    if search:
        print('entered in search')
        # data = Student.objects.filter(college__college_name__icontains =search)
        # data = Student.objects.filter(email__endswith = search)
        student = student.filter(
            Q(name__icontains = search) |
            Q(email__icontains = search) |
            Q(college__college_name__icontains = search) |
            Q(gender__icontains = search))
    if age:
        print('entered in age')

        if age == '1':
            student = student.filter(age__gte =18, age__lte=22).order_by('age')
        if age =='2':
            student = student.filter(age__gte =23, age__lte=26).order_by('age')
        if age == '3':
            student = student.filter(age__gte =27, age__lte=30).order_by('age')

        context ={
            'students':student,
            'search':search
            }
        return render(request,'search.html', context)

    context = {
        'students':student
    }
    return render(request,'search.html', context)