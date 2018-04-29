from setuptools import setup, find_packages

long_description = """
DemonHunter is a framework to create a Honeypot network very simple and easy.
"""


def requirements():
    reqs = []
    with open('requirements.txt', 'r') as f:
        for line in f:
            reqs.append(line.replace('\n', ''))
    return reqs


setup(
    name='demonhunter',
    version='2.0.0',

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
    install_requires=requirements(),
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