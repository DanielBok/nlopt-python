import platform

from setuptools import find_packages, setup

install_requires = [
    'numpy >=1.14'
]

if platform.system() == "Windows":
    package_data = {'nlopt': ['nlopt.dll', '_nlopt.pyd']}
else:
    package_data = {'nlopt': ['nlopt.so', '_nlopt.pyd']}

with open('README.md') as f:
    long_description = f.read()

setup(
    name='nlopt',
    version='2.6.1',
    description='Library for nonlinear optimization, wrapping many algorithms for global and local, constrained or '
                'unconstrained, optimization',
    packages=find_packages(include=['nlopt']),
    package_data=package_data,
    include_package_data=True,
    zip_safe=False,
    license="MIT",  # placeholder, refer to the LICENSE file for more details
    python_requires='>=2.7,!=3.0.*,!=3.1.*,!=3.2.*,!=3.3.*,!=3.4.*',
    install_requires=install_requires,
    url='https://nlopt.readthedocs.io/en/latest/',
    long_description=long_description,
    maintainer='Daniel Bok',
    maintainer_email='daniel.bok@outlook.com',
    classifiers=[
        'Development Status :: 4 - Beta',
        'Intended Audience :: Education',
        'Intended Audience :: End Users/Desktop',
        'Operating System :: MacOS',
        'Operating System :: Microsoft :: Windows',
        'Operating System :: Unix',
        'Programming Language :: C++',
        'Programming Language :: Python :: 3.6',
        'Programming Language :: Python :: 3.7',
        'Topic :: Scientific/Engineering',
    ]
)
