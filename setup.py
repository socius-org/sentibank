from distutils.core import setup

setup(
  name = 'sentibank', 
  packages = ['sentibank'],   
  version = '0.0.1.2',      
  license='MIT',        
  description = 'TYPE YOUR DESCRIPTION HERE',   
  author = 'Nick S.H Oh',                   
  author_email = 'nick.sh.oh@socialscience.ai',      
  url = 'https://github.com/socius-org/sentibank',  
  download_url = 'https://github.com/socius-org/sentibank/archive/refs/tags/0.0.1.2.tar.gz', 
  keywords = ['AI', 'Social Science', 'Sentiment Analysis'],   # Keywords that define your package best
  install_requires=[
          'spacy',
          'spacymoji',
          'rich'
      ],
  include_package_data=True
)
