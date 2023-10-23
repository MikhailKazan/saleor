from django.contrib.sites.models import Site
from django.contrib.staticfiles.storage import staticfiles_storage

from ..utils import build_absolute_uri

LOGO_URL = "images/saleor-logo-sign.png"

# TODO: SiteContext should be dynamical created
SUPPORT_EMAIL = "email:support@enversio.com"
SUPPORT_TELEFON_COUNTRY_CODE = "+49"
SUPPORT_TELEFON_NUMBER = "12345-67-89"

def get_site_context():
    site: Site = Site.objects.get_current()
    site_context = {
        "domain": site.domain,
        "site_name": site.name,
        "logo_url": build_absolute_uri(staticfiles_storage.url(LOGO_URL)),
        "support_email": SUPPORT_EMAIL,
        "support_telefon_country_code": SUPPORT_TELEFON_COUNTRY_CODE,
        "support_telefon_number": SUPPORT_TELEFON_NUMBER,
    }
    return site_context
