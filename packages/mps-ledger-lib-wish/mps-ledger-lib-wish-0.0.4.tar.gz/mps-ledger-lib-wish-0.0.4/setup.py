import setuptools

with open("README.md", "r") as fh:
    long_description = fh.read()

setuptools.setup(
    name="mps-ledger-lib-wish",
    version="0.0.4",
    author_email="merchant_payments_eng@contextlogic.com",
    description="A library for Ledger system in Wish",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/ContextLogic/mps-ledger-lib",
    packages=setuptools.find_packages(),
    classifiers=[
        "Programming Language :: Python :: 2",
        "Programming Language :: Python :: 3",
        "Operating System :: OS Independent",
    ],
    python_requires='>=2.7',
)