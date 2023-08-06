import setuptools

setuptools.setup(
    name="pybungie",
    version="0.5.4",
    author="Hayden Cole",
    author_email="cole.haydenj@gmail.com",
    description="For interacting with the Bungie.net API",
    url="https://github.com/Hayden-J-C/pybungie.git",
    packages=['pybungie'],
    package_data={'pybungie': ['config/*', ]},
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
    install_requires=['requests', 'pyOpenSSL', 'python-dotenv'],
    python_requires='>=3.6',
)
