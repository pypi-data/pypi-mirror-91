import setuptools
from mutract.__init__ import __version__
with open("README.md", "r") as fh:
    long_description = fh.read()

entrys = ['mutract=mutract.mutract:main',]
entry_points={
    'console_scripts': entrys,
}

setuptools.setup(
    name="mutract",
    version=__version__,
    author="zhouyiqi",
    author_email="zhouyiqi@singleronbio.com",
    description="Extracting single cell variants from bam file",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/singleron-RD/mutract",
    packages=setuptools.find_packages(),
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
    python_requires='>=3.6',
    include_package_data=True,
    entry_points=entry_points,
    install_requires=[
        'pysam>=0.15.0',
        'scipy>=0.19.1',
        'numpy>=1.15.4',
        'pandas==0.23.4',
    ]
)