from django.shortcuts import render, redirect
from django.contrib import messages
from tracker.models import Transaction
from django.db.models import Sum, Q
from django.contrib.auth.models import User
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required

@login_required(login_url='/login/')
def index(request):
    """
    View for displaying and creating transactions.
    """
    if request.method == 'POST':
        desc = request.POST.get('desc')
        amount = request.POST.get('amount')

        if desc is None:
            messages.info(request, "Description cannot be blank")
            return redirect('/')
        try:
            float(amount)
        except:
            messages.info(request, "Amount should be a number")
            return redirect('/')
        
        Transaction.objects.create(
            description = desc,
            amount = amount,
            created_by = request.user
        )

        return redirect('/')
    
    context = {
        'transactions': Transaction.objects.filter(created_by=request.user),
        'balance': Transaction.objects.filter(created_by=request.user).aggregate(total=Sum('amount'))['total'] or 0,
        'income': Transaction.objects.filter(created_by=request.user, amount__gte=0).aggregate(income=Sum('amount'))['income'] or 0,
        'expense': Transaction.objects.filter(created_by=request.user, amount__lte=0).aggregate(expense=Sum('amount'))['expense'] or 0
    }
    return render(request, 'index.html', context)

@login_required(login_url='/login/')
def del_transaction(request, uid):
    """
    View for deleting a transaction by its UUID.
    """
    Transaction.objects.get(uuid=uid).delete()
    return redirect('/')

def registration(request):
    """
    View for user registration.
    """
    if request.method == 'POST':
        first_name = request.POST.get('first_name')
        last_name = request.POST.get('last_name')
        username = request.POST.get('username')
        email = request.POST.get('email')
        password = request.POST.get('password')

        user = User.objects.filter(Q(email=email) | Q(username=username))
        if user.exists():
            messages.info(request, "Username or email already exists")
            return redirect('/register/')
        
        user = User.objects.create(
            first_name=first_name,
            last_name=last_name,
            username=username,
            email=email,
        )
        user.set_password(password)
        user.save()
        messages.info(request, "Account created successfully")
        return redirect('/login/')

    return render(request, 'register.html')

def login_page(request):
    """
    View for user login.
    """
    if request.method == 'POST':
        username = request.POST.get('username')
        password = request.POST.get('password')

        user = User.objects.filter(username=username)

        if not user.exists():
            messages.info(request, "Error: Username not found!")
            return redirect('/login/')
        user = authenticate(username=username, password=password)

        if not user:
            messages.info(request, "Error: Invalid credentials!")
            return redirect('/login/')
        login(request, user)

        return redirect('/')

    return render(request, 'login.html')

def logout_page(request):
    """
    View for user logout.
    """
    logout(request)
    return redirect('login')
