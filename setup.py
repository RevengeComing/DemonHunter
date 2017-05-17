from setuptools import setup, find_packages

long_description = """
DemonHunter is a framework to create a Honeypot network very simple and easy.
"""

setup(
    name='demonhunter',
    version='1.1.1',

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
    install_requires=['httptools'],
    packages=find_packages(),

    keywords='honeypot honeynet agent',
    scripts = [
            'bin/dh_test'
        ],
    package_data = {
        '': ['*.html'],
        'demonhunter': ['nodes/honeypots/http/nginx/*.html', 'nodes/honeypots/http/apache/*.html'],
    }
)