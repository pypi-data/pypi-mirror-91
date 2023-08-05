import setuptools

with open("README.md", "r") as fh:
    long_description = fh.read()


setuptools.setup(
    name="dltkai",
    version="1.1.2",
    author="DLTK",
    author_email="connect@qubitai.tech",
    description="Python Client for DLTK.",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/dltk-ai/dltkai-sdk",
    packages=setuptools.find_packages(),
    install_requires=[
        'Keras',
        'tensorflow==2.2.0',
        'imageai==2.1.5',
        'nltk==3.4.5',
        'spacy==2.2.4',
        'numpy==1.18.1',
        'scikit-learn==0.22.1',
        'scipy==1.4.1',
        'seaborn==0.10.0',
        'matplotlib==3.1.3',
        'gensim==3.8.1',
        'beautifulsoup4==4.8.2',
        'rake-nltk==1.0.4',
        'imutils==0.5.3',
        'opencv-python==4.5.1.48',
        'pandas==1.0.0',
        'streamlit==0.64.0'
    ],
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
)
