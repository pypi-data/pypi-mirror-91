from setuptools import setup, find_packages

classif = [
    'Development Status :: 5 - Production/Stable',
    'Intended Audience :: Education',
    'Operating System :: OS Independent',
    'License :: OSI Approved :: MIT License',
    'Programming Language :: Python :: 3'
]
setup(
    name="cstenv",
    version='0.0.1',
    description='a simple env-based language',
    long_description=open("README.txt", "r").read() + "\n\n===========CHANGELOG============\n\n" +
    open("CHANGELOG.txt", "r").read(),
    author="Abdulrahman Alhazmi",
    author_email="Abodialhazmi02@gmail.com",
    license="MIT",
    classifiers=classif,
    keywords=['env', 'dotenv', 'dot', 'cstenv', 'cst'
              'customdotenv', 'customenv', 'custom', 'lang', 'language'],
    packages=find_packages(),
    url="https://fxomt2-0.github.io/cst-env.github.io/",
    install_requires=['']
)
