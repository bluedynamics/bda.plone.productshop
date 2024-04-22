# -*- coding: utf-8 -*-
from setuptools import find_packages
from setuptools import setup
import os


def read_file(name):
    with open(os.path.join(os.path.dirname(__file__), name)) as f:
        return f.read()


version = '1.0b1'
shortdesc = "Product shop extension based on bda.plone.shop"
longdesc = '\n\n'.join([read_file(name) for name in [
    'README.rst',
    'CHANGES.rst',
    'LICENSE.rst'
]])


setup(
    name='bda.plone.productshop',
    version=version,
    description=shortdesc,
    long_description=longdesc,
    classifiers=[
        "Framework :: Plone",
        "Framework :: Plone :: 6.0",
        "Framework :: Plone :: Addon",
        "Framework :: Zope",
        "Framework :: Zope :: 5",
        "License :: OSI Approved :: GNU General Public License (GPL)",
        "Programming Language :: Python",
        "Programming Language :: Python :: 3.8",
        "Programming Language :: Python :: 3.9",
        "Programming Language :: Python :: 3.10",
        "Programming Language :: Python :: 3.11",
        "Programming Language :: Python :: 3.12",
        "Topic :: Software Development :: Libraries :: Python Modules",
    ],
    keywords='Python Plone e-commerce',
    author='Bluedynamics Alliance',
    author_email='dev@bluedynamics.com',
    url='https://github.com/bluedynamics/bda.plone.productshop',
    project_urls={
        'PyPI': 'https://pypi.python.org/pypi/bda.plone.productshop',
        'Source': 'https://github.com/bluedynamics/bda.plone.productshop',
        'Tracker': 'https://github.com/bluedynamics/bda.plone.productshop/issues'
    },
    license='GPL version 2',
    packages=find_packages('src', exclude=['ez_setup']),
    namespace_packages=['bda', 'bda.plone'],
    package_dir={'': 'src'},
    include_package_data=True,
    zip_safe=False,
    install_requires=[
        'setuptools',
        'Products.CMFPlone>=6.0.0',
        'bda.plone.shop',
        'collective.instancebehavior',
    ],
    extras_require={
        'test': [
            'plone.app.testing',
            'plone.app.robotframework[debug]',
        ],
    },
    entry_points="""
    [z3c.autoinclude.plugin]
    target = plone
    [console_scripts]
    update_locale = bda.plone.productshop.locales.update:update_locale
    """,
)
