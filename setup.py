from setuptools import setup, find_packages

with open('requirements.txt', encoding='utf-8') as f:
    required = f.read().splitlines()

setup(
    name='pyfecons',
    version='0.0.36',
    author='Woodruff Scientific LTD',
    author_email='info@woodruffscientific.com',
    description='Library for PyFECONS costing calculations.',
    long_description=open('README.md').read(),
    long_description_content_type='text/markdown',
    url='https://github.com/Woodruff-Scientific-Ltd/PyFECONS',
    packages=find_packages(),
    install_requires=required,
    classifiers=[
        'Development Status :: 3 - Alpha',
        'Intended Audience :: Science/Research',
        'License :: OSI Approved :: BSD License',
        'Programming Language :: Python :: 3.10',
    ],
    python_requires='>=3.10',
    include_package_data=True,
)
