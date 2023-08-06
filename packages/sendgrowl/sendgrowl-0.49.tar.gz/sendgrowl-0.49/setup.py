from setuptools import setup, find_packages
import __version__
version = __version__.version
setup(
    name = 'sendgrowl',
    version = version,
    author = 'Hadi Cahyadi LD',
    author_email = 'cumulus13@gmail.com',
    description = ('simple send notify to growl'),
    license = 'MIT',
    keywords = "youtube downloader download channel",
    url = 'https://github.com/cumulus13/sendgrowl',
    scripts = [],
    py_modules = ['sendgrowl'],
    packages = find_packages(),
    download_url = 'https://github.com/cumulus13/sendgrowl/tarball/master',
    install_requires=[
        'gntplib',
        'argparse'
    ],
    # TODO
    #entry_points={
    #    "console_scripts": ["drawille=drawille:__main__"]
    #},
    entry_points = {
         "console_scripts": ["sendgrowl = sendgrowl:usage",]
    },
    classifiers = [
        "Development Status :: 4 - Beta",
        "Topic :: Utilities",
        'Environment :: Console',
        'License :: OSI Approved :: GNU Affero General Public License v3',
        'Intended Audience :: Developers',
        'Natural Language :: English',
        'Programming Language :: Python',
        'Programming Language :: Python :: 2.6',
        'Programming Language :: Python :: 2.7',
        'Programming Language :: Python :: 3',
        'Programming Language :: Python :: 3.3',
        'Programming Language :: Python :: 3.7',
        'Programming Language :: Python :: 3.8',
    ],
)
