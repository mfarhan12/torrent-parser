import os
import setuptools

def setup(**kwargs):
      setuptools.setup(zip_safe=False, **kwargs)

exec(open(os.path.join("bt_parser", "version.py")).read())
release = __version__

setup(name='bt_parser',
      version=release,
      description='Python Library that parses torrent files',
      author='Mohammad Farhan',
      author_email='mfarhan102@gmail.com',
      url='https://github.com/mfarhan12/torrent-parser',
      test_suite='bt_parser.tests',
      packages=['bt_parser']
     )
