from setuptools import setup
from setuptools.command.install import install
import subprocess
import sys

class CustomInstallCommand(install):
    def run(self):
        install.run(self)
        subprocess.check_call([sys.executable, "-m", "spacy", "download", "en_core_web_sm"])

setup(
    name='sentibank',
    packages=['sentibank'],
    version='0.0.5',
    license='CC BY-NC-SA 4.0',
    description='Unifying sentiment lexicons and dictionaries into an accessible open python package',
    author='Nick S.H Oh',
    author_email='nick.sh.oh@socialscience.ai',
    url='https://github.com/socius-org/sentibank',
    download_url='https://github.com/socius-org/sentibank/archive/refs/tags/0.0.5.tar.gz',
    keywords=[
        'AI', 
        'Social Science', 
        'Sentiment Analysis', 
        'Sentiment Dictionary', 
        'Sentiment Lexicon', 
        'Semantic Orientation'
    ],
    install_requires=[
        'spacy == 3.7.2',
        'spacymoji == 3.1.0',
        'rich == 13.4.2',
        'pandas == 2.1.4'
    ],
    include_package_data=True,
    cmdclass={
        'install': CustomInstallCommand,
    }
)
