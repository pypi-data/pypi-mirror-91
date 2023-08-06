from setuptools import find_packages
from setuptools import setup


name = 'kctzstyle_first_package'
version = '1.0.1'
url = 'https://github.com/kctzstyle/first-pypi-package/'
author = 'kctzstyle'
author_email = 'kctzstyle@gmail.com'
license = 'MIT LICENSE'
packages = find_packages()
python_requires = '>=3'
description = "kctzstyle's first package"
long_description = '''kctzstyle's first package\n
@Author: kctzstyle
@Twitter: @kctzstyle
@Reddit: u/kctzstyle
@GitHub: https://github.com/kctzstyle/
@GitHub Repository: https://github.com/kctzstyle/first-pypi-package/\n
:: Description ::
This is kctzstyle's First Package Tutorial using GitHub Python Actions!
깃허브 파이썬 액션 튜토리얼입니다! 감사합니다!
'''


setup(
    name=name,
    version=version,
    url=url,
    author=author,
    author_email=author_email,
    license=license,
    packages=packages,
    python_requires=python_requires,
    description=description,
    long_description=long_description,
)
