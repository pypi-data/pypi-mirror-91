from setuptools import setup, find_packages
from accessmysqlconverter.application import version, author

with open("README.md", "r") as readme_file:
    readme = readme_file.read()

requirements = ["pyodbc>=4"]

setup(
    name="accessmysqlconverter",
    version=version,
    author=author,
    author_email="miguel.granel.f@gmail.com",
    description="A package to convert MS Access (.mdb, .accdb) into a SQL file (Optionally with It's data)",
    long_description=readme,
    long_description_content_type="text/markdown",
    url="https://github.com/miguel93041/accessmysqlconverter/",
    packages=find_packages(),
    install_requires=requirements,
    classifiers=[
        'Development Status :: 5 - Production/Stable',
        'Intended Audience :: Developers',
        'Topic :: Database :: Database Engines/Servers',
        'Operating System :: Microsoft :: Windows',
        'Programming Language :: Python :: 3',
        'Programming Language :: Python :: 3.0',
        'Programming Language :: Python :: 3.1',
        'Programming Language :: Python :: 3.2',
        'Programming Language :: Python :: 3.3',
        'Programming Language :: Python :: 3.4',
        'Programming Language :: Python :: 3.5',
        'Programming Language :: Python :: 3.6',
        'Programming Language :: Python :: 3.7',
        'Programming Language :: Python :: 3.8',
        'License :: OSI Approved :: GNU General Public License v3 (GPLv3)',
    ],
    include_package_data=True,
    package_data={
        'images': [
            'images/hide_pwd.png',
            'images/watch_pwd.png',
            'images/icon.ico',
        ],
    },
)