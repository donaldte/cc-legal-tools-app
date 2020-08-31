from django.urls import path
from django.urls import register_converter
from django_distill import distill_path

from .utils import get_licenses_code_and_version
from .utils import get_licenses_code_version_jurisdiction
from .utils import get_licenses_code_version_jurisdiction_lang
from .utils import get_licenses_code_version_lang
from i18n import LANGUAGE_CODE_REGEX
from licenses.views import deed_detail
from licenses.views import license_deed_view_code_version_english
from licenses.views import license_deed_view_code_version_jurisdiction
from licenses.views import license_deed_view_code_version_jurisdiction_language
from licenses.views import license_deed_view_code_version_language
from licenses.views import license_detail
from licenses.views import sampling_detail

"""
Example deeds at

https://creativecommons.org/licenses/by/4.0/
https://creativecommons.org/licenses/by/4.0/deed.it
https://creativecommons.org/licenses/by-nc-sa/4.0/
https://creativecommons.org/licenses/by-nc-sa/4.0/deed.es

"""


class LicenseCodeConverter:
    """
    Licenses codes look like "MIT" or "by-sa" or "by-nc-nd" or "CC0".
    We accept any mix of letters, digits, and dashes.
    """

    regex = r"(?i)[-a-z0-9+]+"

    def to_python(self, value):
        return value

    def to_url(self, value):
        return value


register_converter(LicenseCodeConverter, "code")


class JurisdictionConverter:
    """
    jurisdiction should be ISO 3166-1 alpha-2 country code (ISO 3166-1 alpha-2 - Wikipedia)
    https://en.wikipedia.org/wiki/ISO_3166-1_alpha-2

    BUT it also looks as if we use "igo" and "scotland".
    """

    regex = r"[a-z]{2}|igo|scotland"

    def to_python(self, value):
        return value

    def to_url(self, value):
        return value


register_converter(JurisdictionConverter, "jurisdiction")


class VersionConverter:
    """
    These mostly APPEAR to have the format X.Y, where X and Y are digits.
    To be forgiving, we accept any mix of digits and ".".
    There's also at least one with an empty version (MIT).
    """

    regex = r"[0-9.]+|"

    def to_python(self, value):
        return value

    def to_url(self, value):
        return value


register_converter(VersionConverter, "version")


class LangConverter:
    """
    language should be RFC 5646 language tag (RFC 5646)
    https://tools.ietf.org/html/rfc5646.html
    However, RFC 5646 was finalized after most of the legacy ccEngine was written.
    Some of the language tags are based on older specs.

    A more specific RFC 5646 regex might be
    ^((?:(en-GB-oed|i-ami|i-bnn|i-default|i-enochian|i-hak|i-klingon|i-lux|i-mingo|i-navajo|i-pwn|i-tao|i-tay|i-tsu|sgn-BE-FR|sgn-BE-NL|sgn-CH-DE)|(art-lojban|cel-gaulish|no-bok|no-nyn|zh-guoyu|zh-hakka|zh-min|zh-min-nan|zh-xiang))|((?:([A-Za-z]{2,3}(-(?:[A-Za-z]{3}(-[A-Za-z]{3}){0,2}))?)|[A-Za-z]{4}|[A-Za-z]{5,8})(-(?:[A-Za-z]{4}))?(-(?:[A-Za-z]{2}|[0-9]{3}))?(-(?:[A-Za-z0-9]{5,8}|[0-9][A-Za-z0-9]{3}))*(-(?:[0-9A-WY-Za-wy-z](-[A-Za-z0-9]{2,8})+))*(-(?:x(-[A-Za-z0-9]{1,8})+))?)|(?:x(-[A-Za-z0-9]{1,8})+))$
    but that might exclude some older tags, so let's just keep it simple for now
    and match any combination of letters, underscores, and dashes.

    (Why underscores? Because of en_GB being used some places.)
    """

    regex = LANGUAGE_CODE_REGEX

    def to_python(self, value):
        return value

    def to_url(self, value):
        return value


register_converter(LangConverter, "lang")

"""
/licenses/ - overview and links to the licenses (part of this project?)
/licenses/?lang=es - overview and links to the licenses (part of this project?) in Spanish

/licenses/by/4.0 - deed for BY 4.0 English
/licenses/by/4.0/deed.es - deed for BY 4.0 Spanish
/licenses/by/4.0/legalcode - license BY 4.0 English
/licenses/by/4.0/legalcode.es - license BY 4.0 Spanish
...
/licenses/by/3.0/ - deed for BY 3.0 Unported in English
/licenses/by/3.0/legalcode - license for BY 3.0 Unported in English

/licenses/by-nc-sa/3.0/de/ - deed for by-nc-sa, 3.0, jurisdiction Germany, in German
/licenses/by-nc-sa/3.0/de/deed.it - deed for by-nc-sa, 3.0, jurisdiction Germany, in Italian
/licenses/by-nc-sa/3.0/de/legalcode - license for by-nc-sa, 3.0, jurisdiction Germany, in German
(I CANNOT find license for by-nc-sa 3.0 jurisdiction Germany in other languages (/legalcode.it is a 404))

/licenses/by-sa/2.5/ca/ - deed for BY-SA 2.5, jurisdiction Canada, in English
/licenses/by-sa/2.5/ca/deed.it - deed for BY-SA 2.5, jurisdiction Canada, in Italian
/licenses/by-sa/2.5/ca/legalcode.en - license for BY-SA 2.5, jurisdiction Canada, in English
/licenses/by-sa/2.5/ca/legalcode.fr - license for BY-SA 2.5, jurisdiction Canada, in French

/licenses/by-sa/2.0/uk/ - deed for BY-SA 2.0, jurisdiction England and Wales, in English
/licenses/by-sa/2.0/uk/deed.es - deed for BY-SA 2.0, jurisdiction England and Wales, in Spanish
/licenses/by-sa/2.0/uk/legalcode - license for BY-SA 2.0, jurisdiction England and Wales, in English
"""

# DEEDS
urlpatterns = [
    path("license/", license_detail, name="license_detail"),
    path("sampling/", sampling_detail, name="sampling_detail"),
    path("deed/", deed_detail, name="deed_detail"),
    # distill_path(
    #     "<code:license_code>/<version:version>",
    #     license_deed_view_code_version_english,
    #     name="license_deed_view_code_version_english",
    #     distill_func=get_licenses_code_and_version,
    # ),
    distill_path(
        "<code:license_code>/<version:version>/deed.<lang:target_lang>",
        license_deed_view_code_version_language,
        name="license_deed_view_code_version_language",
        distill_func=get_licenses_code_version_lang,
    ),
    # distill_path(
    #     "<code:license_code>/<version:version>/<jurisdiction:jurisdiction>/",
    #     license_deed_view_code_version_jurisdiction,
    #     name="license_deed_view_code_version_jurisdiction",
    #     distill_func=get_licenses_code_version_jurisdiction,
    # ),
    # distill_path(
    #     "<code:license_code>/<version:version>/<jurisdiction:jurisdiction>/deed.<lang:target_lang>",
    #     license_deed_view_code_version_jurisdiction_language,
    #     name="license_deed_view_code_version_jurisdiction_language",
    #     distill_func=get_licenses_code_version_jurisdiction_lang,
    # ),
]
