from distutils.core import setup
setup(
  name = 'auto_nlp',         # How you named your package folder (MyLib)
  packages = ['auto_nlp'],   # Chose the same as "name"
  version = '0.015',      # Start with a small number and increase it with every change you make
  license='MIT',        # Chose a license from here: https://help.github.com/articles/licensing-a-repository
  description = 'Automated NLP tools. Plug N Play.',   # Give a short description about your library
  author = 'Aryan Sharma',                   # Type in your name
  author_email = 'aryansharma.prime@gmail.com',      # Type in your E-Mail
  url = 'https://github.com/aryxns/auto_nlp',   # Provide either the link to your github or to your website
  download_url = 'https://github.com/aryxns/auto_nlp/archive/v_015.tar.gz',    # I explain this later on
  keywords = ['ASPECT BASED', 'SENTIMENT', 'ANALYSIS'],   # Keywords that define your package best
  install_requires=[            # I get to this in a second
          'nltk',
          'stanza',
          'numpy',
          'pandas'
      ],
  classifiers=[      
  'Development Status :: 4 - Beta'
  ],
)