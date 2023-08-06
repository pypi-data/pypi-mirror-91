from setuptools import setup

with open("README.md", "r", encoding="utf-8") as fh:
    long_description = fh.read()


setup(name='k_ege',
      version='0.1',
      description='Gaussian and Binomial distributions',
      packages=['k_ege'],
      author_email='stepan.kazancev.04@bk.ru',
      zip_safe=False)
