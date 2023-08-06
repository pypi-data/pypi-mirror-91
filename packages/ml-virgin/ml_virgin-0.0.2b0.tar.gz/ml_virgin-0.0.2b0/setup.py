import setuptools

with open('README.md', 'r', encoding='utf-8') as fh:
    long_description = fh.read()

setuptools.setup(
    name='ml_virgin',
    version='0.0.2b',
    author='Dan Zimerman',
    author_email='solemnda@gmail.com',
    description='Simple and customizable machine learning pipelines.',
    long_description=long_description,
    long_description_content_type='text/markdown',
    url='https://github.com/solemn-leader/ml_virgin',
    packages=setuptools.find_packages(),
    classifiers=[
        'Programming Language :: Python :: 3',
        'Operating System :: OS Independent',
    ],
    install_requires=[
        'scikit-learn',
        'pandas',
        'numpy'
    ],
    python_requires='>=3.6',
)
