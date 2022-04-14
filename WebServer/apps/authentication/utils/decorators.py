from rest_framework import  exceptions

def auth(view):
    def wrapper(request, *args, **kw):
        if request.headers.get('Authorization', None) is None:
            msg = 'Request must include token'
            raise exceptions.AuthenticationFailed(msg)
        return view(request, *args, **kw)
    return wrapper

