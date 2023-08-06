import copy
from collections import defaultdict
from django.conf import settings
from django.utils.translation import gettext_lazy

try:
    from pretix.base.plugins import PluginConfig
except ImportError:
    raise RuntimeError("Please use pretix 2.7 or above to run this plugin!")

__version__ = "1.0.0"


def patch_phone_numbers(module, countries):
    module._COUNTRY_CODE_TO_REGION_CODE = copy.deepcopy(countries)


class PluginApp(PluginConfig):
    name = "pretix_limit_phone_country"
    verbose_name = "Limit Phone Number Country"

    class PretixPluginMeta:
        name = gettext_lazy("Limit Phone Number Country")
        author = "Tobias Kunze"
        description = gettext_lazy(
            "Limit the available phone number country code in pretix phone number questions. Caution! Applies to the whole server!"
        )
        visible = True
        version = __version__
        category = "FEATURE"
        compatibility = "pretix>=2.7.0"

    def ready(self):
        import pretix.base.forms.questions as questions_form
        import pretix.presale.forms.checkout as base_form

        countries = defaultdict(list)
        if settings.CONFIG_FILE.has_section("plugin:limit_phone_country"):
            for country, code in settings.CONFIG_FILE.cp[
                "plugin:limit_phone_country"
            ].items():
                countries[int(code)].append(country.upper())

        if not len(countries):
            countries = {1: ("US",)}
        patch_phone_numbers(questions_form, countries)
        patch_phone_numbers(base_form, countries)


default_app_config = "pretix_limit_phone_country.PluginApp"
