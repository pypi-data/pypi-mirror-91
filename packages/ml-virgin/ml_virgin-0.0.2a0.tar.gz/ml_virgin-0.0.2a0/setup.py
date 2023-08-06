import setuptools

with open('README.md', 'r', encoding='utf-8') as fh:
    long_description = fh.read()

setuptools.setup(
    name='ml_virgin',
    version='0.0.2a',
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
        'scikit-learn==0.24.0',
        'pandas==1.1.4',
        'numpy==1.19.4'
    ],
    python_requires='>=3.6',
)
