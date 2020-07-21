from django.shortcuts import render, redirect
from django.contrib import messages, auth
from django.contrib.auth.models import User
from contacts.models import Contact


def signup(request):
    if request.method == 'post':
        # Get form values
        first_name = request.POST['first_name']
        last_name = request.POST['last_name']
        username = request.POST['username']
        email = request.POST['email']
        password = request.POST['password']
        password2 = request.POST['password2']

        # check password
        if password == password2:
            # check username
            if User.objects.filter(username=username).exists():
                messages.error(request, 'Username is already existed')
                return redirect('signup')
            else:
                if User.objects.filter(email=email).exists():
                    messages.error(request, 'Username is already existed')
                    return redirect('signup')
                else:
                    user = User.objects.create(username=username, email=email, first_name=first_name,
                                               last_name=last_name)
                    # login after register
                    # auth.login(request, user)
                    # messages.success(request, 'You are now logged in')
                    # return redirect('index')
                    user.save()
                    messages.success('You are now registered. you can now login')
                    return redirect('login')
        else:
            messages.error(request, 'Passwords does not match')
            return redirect('signup')
    else:
        return render(request, 'accounts/signup.html')


def login(request):
    if request.method == 'POST':
        username = request.POST['username']
        password = request.POST['password']

        user = auth.authenticate(username=username, password=password)

        if user is not None:
            auth.login(request, user=user)
            messages.success(request, 'You are now loggedIn.')
            return redirect('dashboard')
        else:
            messages.error(request, 'Invalid credentials')
            return redirect('login')
    else:
        return render(request, 'accounts/login.html')


def logout(request):
    if request.method == 'POST':
        auth.logout(request)
        messages.success(request, 'You are now logout')
        return redirect('index')


def dashboard(request):
    user_contacts = Contact.objects.order_by('-contact_date').filter(user_id=request.user.id)

    context = {
        'contacts': user_contacts
    }

    return render(request, 'accounts/dashboard.html', context)
