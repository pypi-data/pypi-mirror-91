import setuptools

with open('README.md', 'r', encoding='utf-8') as fh:
    long_description = fh.read()

setuptools.setup(
    name='matrad',
    version='0.0.7',
    author='Manuel Capel',
    author_email='manuel.capel82@gmail.com',
    description='A Python interface to the Binance API',
    long_description=long_description,
    long_description_content_type='text/markdown',
    url='https://github.com/mancap314/matrad',
    packages=setuptools.find_packages(),
    classifiers=[
        'Programming Language :: Python :: 3',
        'License :: OSI Approved :: MIT License',
        'Operating System :: OS Independent',
    ],
    python_requires='>=3.6',
    install_requires=[
        'requests>=2.25.1',
    ]
)
