from setuptools import setup

with open("README.md", "r") as fh:
    long_description = fh.read()

setup(
    name='pyhard',
    version='0.3',
    description='Instance hardness package',
    long_description=long_description,
    long_description_content_type="text/markdown",
    packages=['pyhard'],
    url='https://gitlab.com/ita-ml/instance-hardness',
    license='',
    author='Pedro Paiva',
    author_email='paiva@ita.br',
    install_requires=[
        'pandas>=1.0.3',
        'scikit-learn>=0.22.1',
        'numpy>=1.18.4',
        'PyYAML',
        'scipy',
        'gower',
        'panel',
        'bokeh>=2.0.2',
        'ipywidgets',
        'holoviews>=1.13.2',
        'matplotlib>=3.2.1',
        'plotly',
        'plotting',
        'rankaggregation'
    ],
    include_package_data=True,
    # package_data={'data': ['data/'],
    #               'config': ['conf/config.yaml'],
    #               },
    data_files=[('data', ['data/**/*.csv'])],
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
    python_requires='>=3.7'
)
