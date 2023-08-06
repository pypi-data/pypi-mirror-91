import pathlib
from setuptools import find_packages, setup

HERE = pathlib.Path(__file__).parent
README = (HERE / "README.md").read_text()

REQUIRED_PACKAGES = [
    "torch>=1.7",
    "torchvision>=0.8",
    "torchaudio",
    "tensorflow>=2.4",
    "Matplotlib",
    "Cython",
]

setup(
    name="rodan",
    version="0.0.1",
    description="Advanced Deep Learning Library",
    url="https://github.com/hoangtnm/rodan",
    author="Hoang N.M. Tran",
    author_email="",
    license="Apache License, Version 2.0",
    classifiers=[
        "Intended Audience :: Developers",
        "Intended Audience :: Education",
        "Topic :: Scientific/Engineering",
        "Topic :: Scientific/Engineering :: Mathematics",
        "Topic :: Scientific/Engineering :: Artificial Intelligence",
        "Topic :: Software Development",
        "Topic :: Software Development :: Libraries",
        "Topic :: Software Development :: Libraries :: Python Modules",
        "Programming Language :: Python :: 3",
    ],
    install_requires=REQUIRED_PACKAGES,
    include_package_data=True,
    packages=[p for p in find_packages() if p.endswith("rodan")],
)
