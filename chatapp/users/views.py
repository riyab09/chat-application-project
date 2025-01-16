from django.shortcuts import render

# Create your views here.
from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required
from django.contrib.auth.models import User
from django.contrib.auth import authenticate, login, logout
from django.contrib import messages

def home(request):
    if request.user.is_authenticated:
        username = request.user.username  # Make sure this is set
    else:
        username = None
    return render(request, 'home.html', {'username': username})


def login_page(request):
    if request.method == 'POST':
        username = request.POST.get('username')
        password = request.POST.get('password')
        print(username)
        print(password)
        user = authenticate(request, username=username, password=password)
        if user is not None:
            login(request, user)
            messages.success(request, 'Login successful!')
            return redirect('/chat/riya09/')
        else:
            messages.error(request, 'Invalid email or password. Please try again.')
    if request.user.is_authenticated:
        return redirect('/chat/riya09/')
    return render(request,'login.html')


@login_required
def logout_page(request):
    logout(request)  
    messages.success(request, 'You have been logged out successfully.') 
    return redirect('/')


def signup_view(request):
    if request.method == 'POST':
        email = request.POST.get('email')
        username = request.POST.get('username')
        password1 = request.POST.get('password')
        confirm_password = request.POST.get('confirm_password')

        # Check if passwords match
        if password1 != confirm_password:
            messages.error(request, 'Passwords do not match. Please try again.')
            return render(request, 'signup.html')

        # Check if email is already taken
        if User.objects.filter(email=email).exists():
            messages.error(request, 'Email is already in use. Please try another.')
            return render(request, 'signup.html')

        # Create the new user
        user = User.objects.create_user(username=username, 
                                        email=email,
                                        password=password1
                                        )
        user.save()
        
        # Automatically log the user in after signup
        login(request, user)

        messages.success(request, 'Signup successful! You are now logged in.')
        return redirect('home')  # Redirect to home page after signup and login

    if request.user.is_authenticated:
        return redirect('home')  # Redirect authenticated users to the home page

    return render(request, 'signup.html')
# def signup_view(request):
#     if request.method == 'POST':
#         email = request.POST.get('email')
#         username = request.POST.get('username')
#         password1 = request.POST.get('password')
#         confirm_password = request.POST.get('confirm_password')

#         # Check if passwords match
#         if password1 != confirm_password:
#             messages.error(request, 'Passwords do not match. Please try again.')
#             return render(request, 'signup.html')

#         # Check if email is already taken
#         if User.objects.filter(email=email).exists():
#             messages.error(request, 'Email is already in use. Please try another.')
#             return render(request, 'signup.html')

#         # Create the new user
#         user = User.objects.create_user(username=username, 
#                                         email=email,
#                                         password=password1
#                                         )
#         user.save()
#         messages.success(request, 'Signup successful! You can now log in.')
#         return redirect('login')
#     if request.user.is_authenticated:
#         return redirect('/chat/kishan') #todo: pass usename
#     return render(request, 'signup.html')

# # def signup(request):
# #     if request.method == 'POST':
# #         form = UserCreationForm(request.POST)
# #         if form.is_valid():
# #             form.save()
# #             messages.success(request, 'Account created successfully!')  # Show success message
# #             return redirect('home')  # Redirect to the home page (or any other page)
# #     else:
# #         form = UserCreationForm()
# #     return render(request, 'signup.html', {'form': form})