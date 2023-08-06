import setuptools

with open("README.md", "r", encoding="utf-8") as fh:
    long_description = fh.read()

setuptools.setup(
    name="RoboMax",
    version="9.1",
    author="Richard White III",
    author_email="rwhit101@uncc.edu",
    description="python code for versatile Functional Ontology Assignments for Metagenomes via Hidden Markov Model (HMM) searching with environmental focus of shotgun meta'omics data",

    url="https://github.com/raw937/robomax",
    packages=['RoboMax'],
    package_dir={'RoboMax':'src/RoboMax'},
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
    python_requires='>=3.6.9',
    install_requires=[
          'setuptools',
          'scikit-bio',
          'dask',
          'pandas',
          'numpy',
          'humanize',
          'plotly',
          'psutil',
          'joblib',
          'hmmer',
          'dash'
          ],
    download_url='https://osf.io/72p6g/download'
)
