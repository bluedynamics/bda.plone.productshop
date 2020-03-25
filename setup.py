# -*- coding: utf-8 -*-
"""Installer for the bda.plone.productshop package."""

from setuptools import find_packages
from setuptools import setup


long_description = '\n\n'.join([
    open('README.rst').read(),
    open('CHANGES.rst').read(),
])


setup(
    name='bda.plone.productshop',
    version='1.0a1.dev0',
    description="Product shop extension based on bda.plone.shop",
    long_description=long_description,
    # Get more from https://pypi.org/classifiers/
    classifiers=[
        "Environment :: Web Environment",
        "Framework :: Plone",
        "Framework :: Plone :: Addon",
        "Framework :: Plone :: 5.2",
        "Programming Language :: Python",
        "Programming Language :: Python :: 2.7",
        "Programming Language :: Python :: 3.6",
        "Programming Language :: Python :: 3.7",
        "Programming Language :: Python :: 3.8",
        "Operating System :: OS Independent",
        "License :: OSI Approved :: GNU General Public License v2 (GPLv2)",
    ],
    keywords='Python Plone e-commerce',
    author='Bluedynamics Alliance',
    author_email='dev@bluedynamics.com',
    url='https://github.com/collective/bda.plone.productshop',
    project_urls={
        'PyPI': 'https://pypi.python.org/pypi/bda.plone.productshop',
        'Source': 'https://github.com/collective/bda.plone.productshop',
        'Tracker': 'https://github.com/collective/bda.plone.productshop/issues',
        # 'Documentation': 'https://bda.plone.productshop.readthedocs.io/en/latest/',
    },
    license='GPL version 2',
    packages=find_packages('src', exclude=['ez_setup']),
    namespace_packages=['bda', 'bda.plone'],
    package_dir={'': 'src'},
    include_package_data=True,
    zip_safe=False,
    python_requires="==2.7, >=3.6",
    install_requires=[
        'setuptools',
        'Products.CMFPlone>=5.2.1',
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
