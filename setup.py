from setuptools import setup

with open("README.md", "r") as f:
    long_description = f.read()

setup(name='pytmangadex',
      packages = [
          "pytmangadex"
      ],
      version='1.3',
      description='an library to scrape data from mangadex.org',
      long_description=long_description,
      long_description_content_type='text/markdown',
      url='https://github.com/Sibyl666/pytmangadex',
      download_url= 'https://github.com/Sibyl666/pytmangadex/archive/1.3.tar.gz',
      author='Sibyl666',
      author_email='metinkorkmaz417@gmail.com',
      license='MIT',
      install_requires=[
          'requests',
          'bs4',
          "aiohttp"
      ],
      zip_safe=False
      )
