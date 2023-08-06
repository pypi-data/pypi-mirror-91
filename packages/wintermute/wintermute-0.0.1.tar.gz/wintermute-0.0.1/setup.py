"""
Registry for machine learning models.
"""
import io
import re

from setuptools import find_packages
from setuptools import setup


with io.open("wintermute/__init__.py", "rt", encoding="utf8") as f:
    version = re.search(r'__version__ = "(.*?)"', f.read()).group(1)


INSTALL_REQUIREMENTS = []

EXTRA_REQUIREMENTS = {}

setup(
    name='wintermute',
    version=version,
    url='https://github.com/scruwys/wintermute',
    license='MIT',
    author='Scott Cruwys',
    author_email='scruwys@gmail.com',
    description='Registry for machine learning models',
    long_description=__doc__,
    packages=find_packages(exclude=['tests']),
    include_package_data=True,
    zip_safe=False,
    platforms='any',
    install_requires=INSTALL_REQUIREMENTS,
    setup_requires=[
        'setuptools',
        'wheel',
    ],
    extras_require=EXTRA_REQUIREMENTS,
    python_requires='>=3.5',
    classifiers=[
        'Development Status :: 4 - Beta',
        'Environment :: Console',
        'Intended Audience :: Developers',
        'License :: OSI Approved :: BSD License',
        'Operating System :: POSIX',
        'Operating System :: MacOS',
        'Operating System :: Unix',
        'Operating System :: Microsoft :: Windows',
        'Programming Language :: Python',
        'Programming Language :: Python :: 3',
    ]
)
