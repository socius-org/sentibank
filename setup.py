from distutils.core import setup

setup(
  name = 'sentibank', 
  packages = ['sentibank'],   
  version = '0.0.1.8',      
  license='MIT',        
  description = 'Unifying sentiment lexicons and dictionaries into an accessible open python package',   
  author = 'Nick S.H Oh',                   
  author_email = 'nick.sh.oh@socialscience.ai',      
  url = 'https://github.com/socius-org/sentibank',  
  download_url = 'https://github.com/socius-org/sentibank/archive/refs/tags/0.0.1.8.tar.gz', 
  keywords = ['AI', 'Social Science', 'Sentiment Analysis'],   # Keywords that define your package best
  install_requires=[
          'spacy',
          'spacymoji',
          'rich'
      ],
  include_package_data=True
)
