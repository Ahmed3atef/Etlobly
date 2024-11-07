from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required
# from .utils import send_otp, format_phone_number, is_valid_phone_number
from django.contrib import messages
from .forms import UserRegistrationForm

def signup(request):
    if request.method == 'POST':
        form = UserRegistrationForm(request.POST, request.FILES) 
        if form.is_valid():
            form.save()
            # mobile_number = form.cleaned_data.get('phone_number')
            # formatted_phone_number = format_phone_number(mobile_number)
            
            # # Validate formatted phone number before saving
            # if is_valid_phone_number(formatted_phone_number):
            #     messages.error(request, 'Invalid phone number. Please check and try again.')
            # else:
            #     # Save the form data and send the OTP
            #     form.instance.phone_number = formatted_phone_number  # Set formatted number before saving
                
                
            #     otp = send_otp(formatted_phone_number)
                
            #     # Store OTP and phone number in session for verification
            #     request.session['otp'] = otp
            #     request.session['phone_number'] = formatted_phone_number
                
            #     messages.success(request, 'OTP has been sent to your phone.')
            #     return redirect('verify_otp')
            return redirect('signup_success')
    else:
        form = UserRegistrationForm()

    return render(request, 'account/signup.html', {'form': form})

def signup_success(request):
    return render(request, 'account/signup_success.html')

def verify_otp(request):
    if request.method == 'POST':
        user_otp = request.POST.get('otp')
        session_otp = request.session.get('otp')
        
        if user_otp == str(session_otp):
            messages.success(request, 'Phone number verified successfully!')
            # Proceed with the rest of the registration or login process
            return redirect('signup_success')
        else:
            messages.error(request, 'Invalid OTP. Please try again.')
            return redirect('verify_otp')
    
    return render(request, 'account/verify_otp.html')


@login_required
def profile(request):
    return render(request, 'core/profile.html', {'user': request.user})