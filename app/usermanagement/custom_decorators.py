from django.http import HttpResponseRedirect


def user_is_dev(f):
    def wrap(request, *args, **kwargs):
        if request.user.is_dev:
            return f(request, *args, **kwargs)

        return HttpResponseRedirect('/home')

    wrap.__doc__ = f.__doc__
    wrap.__name__ = f.__name__
    return wrap


def user_is_player(f):
    def wrap(request, *args, **kwargs):
        if not request.user.is_dev:
            return f(request, *args, **kwargs)

        return HttpResponseRedirect('/home')

    wrap.__doc__ = f.__doc__
    wrap.__name__ = f.__name__
    return wrap
