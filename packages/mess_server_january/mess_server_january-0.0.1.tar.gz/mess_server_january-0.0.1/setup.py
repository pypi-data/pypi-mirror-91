from setuptools import setup, find_packages

setup(name="mess_server_january",
      version="0.0.1",
      description="mess_server_january",
      author="Oleg Dementev",
      author_email="demeoleg@yandex.ru",
      packages=find_packages(),
      install_requires=['PyQt5', 'sqlalchemy', 'pycryptodome', 'pycryptodomex']
      )
