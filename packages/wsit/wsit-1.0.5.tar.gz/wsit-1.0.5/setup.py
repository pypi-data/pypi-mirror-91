from setuptools import setup, find_packages

with open("README.md", "r") as fh:
    long_description = fh.read()

with open('requirements.txt') as fp:
    requires = fp.read()

setup(name='wsit',
      version='1.0.5',
      author='VMS Software, Inc.',
      description='Web Services Integration Toolkit',
      long_description=long_description,
      url="https://vmssoftware.com/products/web-services-integration-toolkit/",
      license='MIT',
      long_description_content_type="text/markdown",
      packages=find_packages(),
      install_requires=requires,
      include_package_data=False,
      zip_safe=False)

