from setuptools import setup, find_packages

classifiers = [
    'Development Status :: 5 - Production/Stable',
    'Intended Audience :: Education',
    'Operating System :: Microsoft :: Windows :: Windows 10',
    'License :: OSI Approved :: MIT License',
    'Programming Language :: Python :: 3'
]

setup(
    name='chaithramc99_hamming_code_v1',
    version='0.0.1',
    description='Hamming code generator and validator',
    long_description=open('README.txt').read() + '\n\n' + open('CHANGELOG.txt').read(),
    url='',
    author='Chaithra M C',
    author_email='chaithra.mc99@gmail.com',
    license='MIT',
    classifiers=classifiers,
    keywords='hamming',
    packages=find_packages(),
    install_requires=['']
)
