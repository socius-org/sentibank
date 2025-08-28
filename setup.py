from setuptools import setup

setup(
    name='sentibank',
    packages=['sentibank'],
    package_data={'sentibank': ['dict_arXiv/*.csv', 'dict_arXiv/*.pickle', 'dict_arXiv/*.json']}, 
    version='1.1.0', 
    license='CC BY-NC-SA 4.0',
    description='Unifying sentiment lexicons and dictionaries into an accessible open python package',
    author='Nick Oh',
    author_email='nick.sh.oh@socius.org',
    url='https://github.com/socius-org/sentibank',
    download_url='https://github.com/socius-org/sentibank/archive/refs/tags/0.2.4.tar.gz',  # Updated
    keywords=[
        'Sentiment Analysis', 
        'Sentiment Dictionary', 
        'Sentiment Lexicon', 
        'Semantic Orientation'
    ],
    install_requires=[
        'spacy>=3.7.2', 
        'spacymoji>=3.1.0',
        'rich>=13.4.2',
        'pandas>=2.1.4',
        'pyenchant>=3.2.2'
    ],
    python_requires='>=3.8', 
    include_package_data=True,
)