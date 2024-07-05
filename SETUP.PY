from setuptools import setup, find_packages

setup(
    name="string_search_server",
    version="1.0.0",
    author="SAMUEL NWABUEZE",
    author_email="realsmind@gmail.com",
    description="A server for performing string search operations using various algorithms.",
    long_description=open('README.md').read(),
    long_description_content_type='text/markdown',
    url="https://github.com/AVIO1/string_search_server",
    packages=find_packages(),
    include_package_data=True,
    install_requires=[
        "Flask==2.0.2",
        "pytest"
    ],
    entry_points={
        'console_scripts': [
            'string_search_server=server:main',
        ],
    },
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
    python_requires='>=3.6',
)
