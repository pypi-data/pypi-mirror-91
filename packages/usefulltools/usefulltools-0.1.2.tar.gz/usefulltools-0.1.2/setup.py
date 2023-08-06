from distutils.core import setup
setup(
  name = 'usefulltools',
  author_email = 'example@example.com',
  version = '0.1.2',
  classifiers = [
      "Programming Language :: Python :: 3",
  ],
  description = 'random tools you can use in python',
  licence = 'MIT',
  instal_requires =['requests','os','sys','inspect','linecache'],
  packages = ['usefulltools'],
  author = 'ninjamar',
  python_require = '>=3.7',
  url = 'https://github.com/ninjamar/usefulltools'
)