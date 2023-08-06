import setuptools

from configly.version import VERSION

with open('README.md', encoding='utf-8') as fh:
    long_description = fh.read()

setuptools.setup(
    name='configly-python',
    version=VERSION,
    author='Configly',
    author_email='configlyco@gmail.com',
    description=(
        'The Official Python Library for Configly - the modern config/static data key/value store'
    ),
    long_description=long_description,
    long_description_content_type='text/markdown',
    url='https://github.com/configly/python',
    packages=setuptools.find_packages(),
    classifiers=[
        'Programming Language :: Python :: 3',
        'License :: OSI Approved :: MIT License',
        'Operating System :: OS Independent',
    ],
    license='MIT License',
    python_requires='>=3.6',
    install_requires=[
      'requests; python_version>="3" and python_version<"4"',
    ]
)
