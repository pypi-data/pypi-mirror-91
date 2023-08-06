from distutils.core import setup

# read the contents of your README file
from os import path
this_directory = path.abspath(path.dirname(__file__))
with open(path.join(this_directory, 'README.rst'), encoding='utf-8') as f:
    long_description = f.read()

setup(
    name='pyStaticAnalyzer',  # How you named your package folder (MyLib)
    packages=['pyStaticAnalyzer'],  # Chose the same as "name"
    version='0.6',  # Start with a small number and increase it with every change you make
    license='MIT',  # Chose a license from here: https://help.github.com/articles/licensing-a-repository
    description='Simple Python Static Analyzer',  # Give a short description about your library
    long_description=long_description,
    author='Andrew Marchenko',  # Type in your name
    author_email='zeroday343@gmail.com',  # Type in your E-Mail
    url='https://github.com/noname19871/pyStaticAnalyzer',  # Provide either the link to your github or to your website
    download_url='https://github.com/noname19871/pyStaticAnalyzer/archive/v0.6.tar.gz',  # I explain this later on
    keywords=['Static Analysis', 'AST', 'Parser', 'Checker'],  # Keywords that define your package best
    classifiers=[
        'Development Status :: 3 - Alpha',  # Chose either "3 - Alpha", "4 - Beta" or "5 - Production/Stable" as the
        # current state of your package
        'Intended Audience :: Developers',  # Define that your audience are developers
        'Topic :: Software Development :: Build Tools',
        'License :: OSI Approved :: MIT License',  # Again, pick a license
        'Programming Language :: Python :: 3.6',  # Specify which pyhton versions that you want to support
        'Programming Language :: Python :: 3.7',
        'Programming Language :: Python :: 3.8',
        'Programming Language :: Python :: 3.9',
    ],
)
