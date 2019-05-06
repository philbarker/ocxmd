from setuptools import setup

setup(
    name="ocxmd",
    version="0.1",
    py_modules=["ocxmd"],
    install_requires=["markdown>=3.0", "PyYAML>=3.13"],
    author="Phil Barker",
    author_email="phil.barker@pjjk.co.uk",
    url="https://github.com/philbarker/ocxmd",
    description="A python markdown extension to take metadata embedded as YAML in a page of markdown and render it as JSON-LD in the HTML created by MkDocs.",
    license="Apache2",
)
