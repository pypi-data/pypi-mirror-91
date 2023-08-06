import os
from distutils.command.build import build

from django.core import management
from setuptools import find_packages, setup

from pretix_limit_phone_country import __version__


try:
    with open(
        os.path.join(os.path.dirname(__file__), "README.rst"), encoding="utf-8"
    ) as f:
        long_description = f.read()
except:
    long_description = ""


class CustomBuild(build):
    def run(self):
        management.call_command("compilemessages", verbosity=1)
        build.run(self)


cmdclass = {"build": CustomBuild}


setup(
    name="pretix-limit-phone-country",
    version=__version__,
    description="Limit the available phone number country code in pretix phone number questions. Caution! Applies to the whole server!",
    long_description=long_description,
    url="https://github.com/rixx/pretix-limit-phone-country",
    author="Tobias Kunze",
    author_email="r@rixx.de",
    license="Apache",
    install_requires=[],
    packages=find_packages(exclude=["tests", "tests.*"]),
    include_package_data=True,
    cmdclass=cmdclass,
    entry_points="""
[pretix.plugin]
pretix_limit_phone_country=pretix_limit_phone_country:PretixPluginMeta
""",
)
