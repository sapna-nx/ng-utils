"""
URL conf for user invitation, using the ng-utils invite registration backend.

If the default behavior of these views is acceptable to you, simply use a line like this
in your root URLconf to set up the default URLs for registration::

    (r'^', include('itng.registration.backends.invite.urls.invitation')),

If you'd like to customize registration behavior, feel free to set up
your own URL patterns for these views instead.

"""

from django.urls import re_path, path

from itng.registration.backends.invite import views


urlpatterns = [
    re_path('^invite/',           views.InvitationView.as_view(),         name='invite'),                # flake8: noqa
    re_path('^invite/complete/',  views.InvitationCompleteView.as_view(), name='invitation_complete'),   # flake8: noqa
]
