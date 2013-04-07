from vanda.apps.dashboard.models import Preferences
from django.contrib.auth import get_user_model

def test():
    a = Preferences()

    b = get_user_model().objects.get(username="lxsameer")
    
    print "<<< ", b
    c = a.update({"user": b}, {"op": 2})

    print ">>> ", c, type(c)

    return a, c

