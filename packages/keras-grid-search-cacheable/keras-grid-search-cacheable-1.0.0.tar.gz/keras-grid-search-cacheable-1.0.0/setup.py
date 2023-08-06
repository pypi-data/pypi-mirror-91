import setuptools

with open("README.md", "r", encoding="utf-8") as fh:
    long_description = fh.read()

setuptools.setup(
    name="keras-grid-search-cacheable",
    version="1.0.0",
    author="Daniel Espinosa",
    author_email="daespinosag@unal.edu.co",
    description="Reducción de tiempo de ejecución de los algoritmos de Machine Learning con búsqueda de parámetros en GridSearch.",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/machine-learning-tools/keras-grid-search-cacheable",
    packages=setuptools.find_packages(),
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
    python_requires='>=3.6.9',
    install_requires=[
        'tensorflow>=1.15.0'
    ]
)
