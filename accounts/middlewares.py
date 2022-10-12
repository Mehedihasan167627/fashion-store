from django.contrib import messages
from django.shortcuts import redirect


def customer_middleware(get_response):
    def middleware(request):
        return_url=request.META["PATH_INFO"]    
        if request.user.is_authenticated==False:
            messages.warning(request,"Please Login with your account")
            return redirect(f"/login/?return_url={return_url}")
            
        response=get_response(request)
        return response

    return middleware
