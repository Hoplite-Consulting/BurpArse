from setuptools import setup, find_packages

setup(
    name="BurpArse",
    version="0.1.2",
    description="Burp XML Parser",
    author="Oliver Scotten",
    author_email="oliver@hopliteconsulting.com",
    packages=find_packages(),
    install_requires=[
        "alive_progress==3.1.5",
        "pyfiglet==1.0.2",
        "setuptools==72.0.0"
    ],
    entry_points={
        "console_scripts": [
            "burparse = burparse.burparse:setup",
        ],
    },
    package_data={"burparse": ["config/*"]}
)
