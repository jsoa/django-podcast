from setuptools import setup, find_packages
import podcast

setup(
    name='django-podcast',
    version=podcast.get_version(),
    description='Django podcast app',
    packages=find_packages('.'),
    include_package_data=True,
    classifiers = ['Frameword :: Django'],
)
