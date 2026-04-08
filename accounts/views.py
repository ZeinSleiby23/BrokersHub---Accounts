from django.shortcuts import render, redirect
from django.contrib.auth import authenticate, login as auth_login, logout as auth_logout
from .models import User

# 1. Registration View (With Advanced Validation)
def register(request):
    if request.method == 'POST':
        u_name = request.POST.get('username')
        u_email = request.POST.get('email')
        u_phone = request.POST.get('phone')
        u_pass = request.POST.get('password')
        u_confirm = request.POST.get('confirm_password')

        # 1. Check if any field is empty
        if not all([u_name, u_email, u_phone, u_pass]):
            return render(request, 'register.html', {'error': 'All fields are required!'})

        # 2. Check if email is already registered
        if User.objects.filter(email=u_email).exists():
            return render(request, 'register.html', {'error': 'This email is already registered!'})

        # 3. Check if username is already taken
        if User.objects.filter(username=u_name).exists():
            return render(request, 'register.html', {'error': 'Username is already taken!'})

        # 4. Password validation (Minimum 8 characters)
        if len(u_pass) < 8:
            return render(request, 'register.html', {'error': 'Password must be at least 8 characters long!'})
        
        # 5. Check if passwords match
        if u_pass != u_confirm:
            return render(request, 'register.html', {'error': 'Passwords do not match!'})

        # If all checks pass, create the user
        user = User.objects.create_user(username=u_name, email=u_email, password=u_pass)
        user.phone = u_phone
        user.role = 'customer'
        user.save()

        auth_login(request, user)
        return redirect('/my-requests') 

    return render(request, 'register.html')

# 2. Login View
def login(request):
    if request.method == 'POST':
        u_name = request.POST.get('username')
        u_pass = request.POST.get('password')

        # Check if credentials are provided
        if not u_name or not u_pass:
            return render(request, 'login.html', {'error': 'Please provide both username and password'})

        # Authenticate user (Check existence and password correctness)
        user = authenticate(username=u_name, password=u_pass)

        if user is not None:
            auth_login(request, user)
            # Role-based redirection
            return redirect('/dashboard' if user.role == 'broker' else '/my-requests')
        else:
            return render(request, 'login.html', {'error': 'Invalid username or password!'})

    return render(request, 'login.html')

# 3. Logout View
def logout(request):
    auth_logout(request)
    return redirect('/login')