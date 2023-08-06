import setuptools

with open("README.md", "r", encoding='utf-8') as fh:
    long_description = fh.read()

setuptools.setup(
    name="gfs",
    version="1.0.1",
    author="ican",
    author_email="1414463123@qq.com",
    description="A GeneticFuzzySystem implemented by Python.",
    url="https://github.com/HarderThenHarder/GeneticFuzzySystem",
    packages=setuptools.find_packages(),
    license='LGPL',
    keywords=['gfs'],
    install_requires=[
        "dearpygui",
        "numpy",
        "matplotlib"
    ]
)