from setuptools import setup, find_packages

setup(
    name='iqt',
    version='0.1.0',
    author='9ft6',
    author_email='9ft6.dev@gmail.com',
    description='IQT - PySide6 framework',
    long_description=open('README.md').read(),
    long_description_content_type='text/markdown',
    url='https://github.com/9ft6/IQT',
    packages=find_packages(),
    include_package_data=True,
    classifiers=[
        'Programming Language :: Python :: 3',
        'License :: OSI Approved :: MIT License',
        'Operating System :: OS Independent',
    ],
    python_requires='>=3.11',
    install_requires=[
        'PySide6',
        'loguru',
        'pydantic',
    ],
)
