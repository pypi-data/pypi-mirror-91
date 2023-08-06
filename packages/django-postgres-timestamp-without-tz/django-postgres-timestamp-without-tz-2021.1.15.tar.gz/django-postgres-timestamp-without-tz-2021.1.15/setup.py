import setuptools

setuptools.setup(
    name='django-postgres-timestamp-without-tz',
    version='2021.1.15',
    install_requires=open('requirements.txt').read().splitlines(),
    packages=setuptools.find_packages()
)
