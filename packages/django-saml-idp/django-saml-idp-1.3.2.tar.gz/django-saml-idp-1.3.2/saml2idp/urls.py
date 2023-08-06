from __future__ import absolute_import, print_function, unicode_literals
from django.conf.urls import url
from .views import descriptor, login_begin, login_init, login_process, logout
from .metadata import get_deeplink_resources

def deeplink_url_patterns(
    url_base_pattern=r'^init/%s/$',
    login_init_func=login_init,
    ):
    """
    Returns new deeplink URLs based on 'links' from settings.SAML2IDP_REMOTES.
    Parameters:
    - url_base_pattern - Specify this if you need non-standard deeplink URLs.
        NOTE: This will probably closely match the 'login_init' URL.
    """
    resources = get_deeplink_resources()
    new_patterns = [
        url(
            url_base_pattern % resource,
            login_init_func,
            {
                'resource': resource,
            },
            )
        for resource in resources
    ]

    return new_patterns

urlpatterns = [
    url(r'^login/$', login_begin, name="saml_login_begin"),
    url(r'^login/process/$', login_process, name='saml_login_process'),
    url(r'^logout/$', logout, name="saml_logout"),
    url(r'^metadata/xml/$', descriptor, name='metadata_xml'),
    # For "simple" deeplinks:
    url(
        r'^init/(?P<resource>\w+)/(?P<target>\w+)/$',
        login_init,
        name="login_init"
    ),
]

# Issue 13 - Add new automagically-created URLs for deeplinks:
urlpatterns.extend(deeplink_url_patterns())
