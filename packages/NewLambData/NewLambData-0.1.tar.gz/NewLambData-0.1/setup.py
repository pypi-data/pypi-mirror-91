from distutils.core import setup

setup(
    name='NewLambData',
    packages=['Lambdata22'],
    version= '0.1',
    license= 'MIT',
    description= 'Collection of helper functions',
    author= 'Ricky Chance',
    author_email= 'chance-ricky@lambdastudents.com',
    url= 'https://github.com/Rick1310/NewLambData.git',
    download_url= 'https://github.com/Rick1310/NewLambData/archive/v_01.tar.gz',
    install_requires= ['pandas', 'numpy', 'sklearn'],
    classifiers=[
    'Development Status :: 3 - Alpha',      
    'Intended Audience :: Developers',      
    'Topic :: Software Development :: Build Tools',
    'License :: OSI Approved :: MIT License',   
    'Programming Language :: Python :: 3',      
    'Programming Language :: Python :: 3.4',
    'Programming Language :: Python :: 3.5',
    'Programming Language :: Python :: 3.6',
  ],
)