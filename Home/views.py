from django.views.decorators.csrf import csrf_protect
from datetime import datetime, timedelta
from django.contrib.auth import authenticate, login, logout
from django.shortcuts import render, redirect
from django.contrib import messages
from django.contrib.auth.models import User
import stripe
from .models import *
from django.contrib.auth.decorators import login_required


def fst(request):

    return render(request, '1st.html')


def login_page(request):
    if request.method == 'POST':
        username = request.POST.get('username')
        password = request.POST.get('password')

        user = User.objects.filter(username=username).first()

        if user is None:
            messages.error(request, "User does not exist!")
            return redirect('/login/')
        else:
            user = authenticate(username=username, password=password)

            if user is None:
                messages.error(request, "Invalid PASSWORD!")
                return redirect('/login')

            else:
                login(request, user)
                return redirect('/home')

    return render(request, 'login.html')


def register_page(request):
    if request.method == 'POST':
        email = request.POST.get('email')
        username = request.POST.get('username')
        password = request.POST.get('password')

        user = User.objects.filter(username=username).first()
        if user:
            messages.error(request, "Username already exists!!")
            return redirect('/register')
        else:
            user = User(username=username, email=email)
            user.set_password(password)
            user.save()

            # Create a Profile object associated with the user
            profile = Profile(user=user)
            profile.save()

            print(profile)
            messages.info(request, "Account created successfully")
            return redirect('/login')

    return render(request, 'register.html')


def logout_page(request):
    logout(request)
    messages.info(request, "Logout successfully")
    return redirect('/login')


def success_page(request):

    return render(request, 'success_page.html')


@login_required(login_url="/login/")
def home(request):

    courses = Course.objects.all()
    context = {'courses': courses}

    if request.user.is_authenticated:
        profile = Profile.objects.filter(user=request.user).first()
        print(profile)
        if profile:
            request.session['profile'] = profile.is_pro

        print(request.user)
        # Set a default value if the profile is not found

    return render(request, 'home.html', context)


@login_required(login_url="/login/")
def view_course(request, slug):
    course = Course.objects.filter(slug=slug).first()
    course_modules = CourseModule.objects.filter(course=course)
    user_profile = Profile.objects.filter(user=request.user).first()

    if user_profile.is_pro == True:
        for module in course_modules:
            module.can_view = True
        print("True")
    else:
        for module in course_modules:
            module.can_view = False
        print("False")

    if course.is_premium == False:
        for module in course_modules:
            module.can_view = True

            print("Free")

    context = {'course': course, 'course_modules': course_modules}

    return render(request, 'course.html', context)


@login_required(login_url="/login/")
@csrf_protect
def become_pro(request):
    if request.method == 'POST':
        membership = request.POST.get('membership', 'Monthly')
        amount = 1000
        if membership == 'Yearly':
            amount = 11000

        stripe.api_key = "sk_test_51Nrdg6HOKyBJ9R4uHTuykRR1HVr2ZXWpipXWiyLWCT5RhNEvyUK3BkJOJBkTi6IT3t38tBSnKF1IkcXRDAuuJNwV00qO8ArHUg"

        customer = stripe.Customer.create(
            email=request.user.email,
            source=request.POST['stripeToken']
        )
        charge = stripe.Charge.create(
            customer=customer,
            amount=amount * 100,
            currency='inr',
            description="Membership"
        )
        print(charge)
        print(request.user)

        if charge['paid'] == True:
            # Add this line to debug

            user_profile = Profile.objects.filter(user=request.user).first()

            print(user_profile)

            if charge['amount'] == 100000:
                user_profile.subscription_type = 'M'
                user_profile.is_pro = True
                expiry = datetime.now() + timedelta(60)
                user_profile.pro_expiry_date = expiry
                user_profile.save()
                print(user_profile)
                print(request.user)
            else:
                user_profile.subscription_type = 'Y'
                user_profile.is_pro = True
                expiry = datetime.now() + timedelta(360)
                user_profile.pro_expiry_date = expiry
                user_profile.save()
                print(request.user)

            return redirect('/success_page')

    return render(request, 'becomepro.html')


def payment(request):
    return render(request, 'payment.html')
