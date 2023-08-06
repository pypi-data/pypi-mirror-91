from setuptools import find_packages, setup

with open('README.md', 'r', encoding='utf-8') as file:
    long_description = file.read()

setup(
    name                ='json-csv-combiner',
    packages            =find_packages(include=['jce']),
    version             ='0.1.1',
    description         ='Combine multiple JSON/CSV/EXCEL into single file',
    long_description    = long_description,
    long_description_content_type='text/markdown',
    author              ='Shrikrishna Joisa',
    author_email        ='shrikrishnajois@gmail.com',
    license             ='MIT',
    url                 ='https://github.com/falcon-head/json-csv-combiner',
    platforms           =['Any'],
    py_modules          =[],
    install_requires    =['pandas', 'tqdm'],
    classifiers         =[
        'Development Status :: 3 - Alpha',
        'License :: OSI Approved :: MIT License',
        'Operating System :: OS Independent',
        'Programming Language :: Python',
    ],
)