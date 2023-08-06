"""
krapplet: A password manager written as a gnome-keyring applet
setup.py is the PyPI packaging script
(c) 2020-2021 Johannes Willem Fernhout, BSD 3-Clause License applies
"""

import setuptools
import pathlib

# Obtain long_description from README.md"
with open("README.md", "r", encoding="utf-8") as fh:
    long_description = fh.read()

# Obtain install_requires from requirements.txt file
requirements_path = pathlib.Path(__file__).parent
install_requires = (requirements_path / "requirements.txt").read_text().splitlines()

#
setuptools.setup(
    name="krapplet", 
    version="0.2.0",
    author="Johannes Willem Fernhout",
    author_email="hfern@fernhout.info",
    description="A password manager written as a gnome-keyring applet",
    long_description=long_description,
    long_description_content_type="text/markdown",
    license="BSD-3-clause",
    keywords=["password manager", "gnome-keyring"],
    url="https://gitlab.com/hfernh/krapplet",
    packages=setuptools.find_packages(),
    install_requires=install_requires,
    data_files=[
        ('share/applications', ['share/applications/krapplet.desktop']),
        ('share/icons/hicolor/48x48/apps', ['share/icons/hicolor/48x48/apps/krapplet.png']),
        ('share/icons/hicolor/96x96/apps', ['share/icons/hicolor/96x96/apps/krapplet.png']),
    ],
    entry_points={
        'console_scripts': [
            'krapplet = krapplet.krapplet:main',
        ],
    },
    classifiers=[
        "Development Status :: 4 - Beta",
        "Environment :: X11 Applications :: GTK",
        "Intended Audience :: End Users/Desktop",
        "License :: OSI Approved :: BSD License",
        "Operating System :: POSIX :: Linux", 
        "Programming Language :: Python :: 3.7",
        "Programming Language :: Python :: 3.8",
        "Programming Language :: Python :: 3.9",
        "Topic :: Security",
        "Topic :: Utilities",
    ],
    python_requires='>=3.7',
)

