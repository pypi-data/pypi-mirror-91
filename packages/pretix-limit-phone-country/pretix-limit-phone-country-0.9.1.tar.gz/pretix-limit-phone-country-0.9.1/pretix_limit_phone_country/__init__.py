from django.utils.translation import gettext_lazy

try:
    from pretix.base.plugins import PluginConfig
except ImportError:
    raise RuntimeError("Please use pretix 2.7 or above to run this plugin!")

__version__ = "0.9.1"


def patch_phone_numbers(module):
    module._COUNTRY_CODE_TO_REGION_CODE = {1: ("US",)}


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

        from . import signals  # NOQA

        patch_phone_numbers(questions_form)
        import pretix.presale.forms.checkout as base_form

        patch_phone_numbers(base_form)


default_app_config = "pretix_limit_phone_country.PluginApp"
