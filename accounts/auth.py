from django.shortcuts import redirect

# to check whether user is logged in or not

def unauthenticated_user(view_function):
    def wrapper_function(request,*args,**kwargs):
        if request.user.is_authenticated:
            return redirect('/')
        else:
            return view_function(request,*args,**kwargs)

    return wrapper_function

# give access to admin pages if request comes from admin
# if request is from normal user redirect to user_dashboard

def admin_only(view_function):
    def wrapper_function(request,*args,**kwargs):
        if request.user.is_staff:
            return view_function(request,*args,**kwargs)
        else:
            return redirect("/")
    
    return wrapper_function

# give access to user_pages if request comes form user
# if request is from admin redirect to admin_dashboard

def user_only(view_function):
    def wrapper_function(request,*args,**kwargs):
        if request.user.is_staff:
            return redirect("/account/dashboard")
        else:
            return view_function(request,*args,**kwargs)
    
    return wrapper_function