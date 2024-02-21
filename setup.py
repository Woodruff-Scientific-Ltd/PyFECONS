from setuptools import setup, find_packages

setup(
    name='pyfecons',
    version='0.0.1',
    author='nTtau Digital LTD',
    author_email='info@nttaudigital.com',
    description='Library for nTtau PyFECONS costing calculations.',
    long_description=open('README.md').read(),
    long_description_content_type='text/markdown',
    url='https://github.com/nTtau/PyFECONS',
    packages=find_packages(),
    install_requires=[],
    classifiers=[
        'Development Status :: 3 - Alpha',
        'Intended Audience :: Science/Research',
        'License :: OSI Approved :: MIT License',
        'Programming Language :: Python :: 3.9',
    ],
    python_requires='>=3.9',
    package_data={
        '': ['*.tex'],
    },
    include_package_data=True,
)