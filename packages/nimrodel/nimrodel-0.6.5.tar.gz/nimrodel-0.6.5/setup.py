import setuptools
import importlib

module = importlib.import_module(setuptools.find_packages()[0])

with open("README.md", "r") as fh:
    long_description = fh.read()

setuptools.setup(
    name=module.name,
    version=".".join(str(n) for n in module.version),
    author=module.author["name"],
    author_email=module.author["email"],
    description=module.desc,
	license="GPLv3",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/" + module.author["github"] + "/" + module.name,
    packages=setuptools.find_packages(),
	include_package_data=True,
	package_data={module.name:module.resources},
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: GNU General Public License v3 (GPLv3)",
        "Operating System :: OS Independent",
    ],
	python_requires=">=3.5",
	install_requires=module.requires,
)
