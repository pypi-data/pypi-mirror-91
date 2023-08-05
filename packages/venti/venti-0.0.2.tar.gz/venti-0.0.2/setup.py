from setuptools import setup, find_packages
import os
import subprocess


setup(
    name="venti",
    author="Daniel Suo",
    author_email="danielsuo@gmail.com",
    description="",
    keywords="ventilator,ventilation",
    url="https://github.com/MinRegret/venti",
    version="0.0.2",
    packages=find_packages(),
    install_requires=[
        "numpy",
        "tqdm",
        "torch",
        "scipy",
        "sklearn",
        "matplotlib",
        "jupyter",
        "ipython",
        "pathos",
        "pigpio"
    ],
    python_requires=">=3.7.*"
)
