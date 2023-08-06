from setuptools import setup

with open("README.md", "r", encoding="utf-8") as f:
    long_description = f.read()

setup(
    name='coolstuff',
    packages=['coolstuff'],
    version='1.0.0',
    author='Raymond',
    description='ML-analysis',
    long_description=long_description,
    long_description_content_type="text/markdown",
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
        "Development Status :: 3 - Alpha",
    ],
    keywords=['cool', 'stuff'],
    install_requires=[
        'pandas',
        'torchvision',
        'torch',
        'adversarial-robustness-toolbox',
        'sklearn',
        'tensorflow',
        'captum',
        'plotly',
    ]
)
