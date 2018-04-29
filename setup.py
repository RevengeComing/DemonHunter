from setuptools import setup, find_packages

long_description = """
DemonHunter is a framework to create a Honeypot network very simple and easy.
"""


requirements = [
    "httptools==0.0.11",
    "aiohttp==2.3.10",
    "bcrypt==3.1.4",
    "flask==0.12.2",
    "flask-login==0.4.1",
    "flask-sqlalchemy==2.3.2",
    "flask-sockets==0.2.1",
    "meinheld==0.6.1",
    "click==6.7",
]


setup(
    name='demonhunter',
    version='2.0.3',

    description='A Distributed Honeypot',
    long_description=long_description,

    url='https://github.com/RevengeComing/DemonHunter',
    author='Sepehr Hamzelooy',
    author_email='s.hamzelooy@gmail.com',
    license='MIT',

    classifiers=[
        'Development Status :: 3 - Alpha',

        'Intended Audience :: Developers',

        'License :: OSI Approved :: MIT License',

        'Programming Language :: Python :: 3.5',
    ],
    install_requires=requirements,
    packages=find_packages(),

    keywords='honeypot honeynet agent',
    scripts = [
            'bin/dh_run'
        ],
    package_data = {
        '': ['*.html', '*.js', '*.css'],
        'demonhunter': [
            'nodes/honeypots/http/nginx/*.html',
            'nodes/honeypots/http/apache/*.html',
            'nodes/master/templates/*',
            'nodes/master/static/css/*',
            'nodes/master/static/js/*'
        ],
    }
)