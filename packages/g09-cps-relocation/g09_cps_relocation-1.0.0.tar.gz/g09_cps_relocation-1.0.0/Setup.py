### Within this file we should define the dependency between our different folders!!

import setuptools

## Loading README.md
with open(file="README.md", mode="r") as readme_handle:

    long_description = readme_handle.read()

setuptools.setup(
    name="g09_cps_relocation",
    author="Anton La Fontaine, Lukas Lehnert",
    author_email="a01351415@unet.univie.ac.at",
    ## <MAJOR_VERSION>, <MINOR_VERSION>, <MAINTENANCE_VERSION>
    version='1.0.0',
    description="A python client library used to get a quick overview between the different libraries of g09_CPS_relocation.",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url='https://gitlab.dke.univie.ac.at/edu-semtech/semtec_ws2020/g09_cps_relocation',
    install_requires=[
        "Flask",
        "paramiko",
        "Owlready2",
        "flaskwebgui",
        "Werkzeug",
        "rdflib",
        "requests"
    ],
    packages=setuptools.find_packages(),
    include_package_data=True,
    python_requires='>=3.7',
)