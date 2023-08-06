from setuptools import setup, find_packages

classifiers = [
    'Development Status :: 1 - Planning',
    'Intended Audience :: Developers',
    'License :: OSI Approved :: MIT License',
    'Programming Language :: Python :: 3'
]

with open('README.txt', 'r') as f:
    readme = f.read()

with open('README.txt', 'r') as f:
    changelog = f.read()

setup(
    name='yiff',
    version='0.0.1',
    description='Yiff package. No idea what I honestly want to do with it, at the moment, though.',
    long_description=f"{readme}\n{changelog}",
    url='',
    author='Josh Colden',
    author_email='nanofaux@hotmail.com',
    license='MIT',
    classifiers=classifiers,
    keywords='yiff',
    find_packages=find_packages(),
    install_requires=['']
)
