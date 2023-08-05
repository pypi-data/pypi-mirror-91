from setuptools import setup


def parse_requirements_file(filename):
    with open(filename, encoding="utf-8") as fid:
        requires = [l.strip() for l in fid.readlines() if l]
    return requires


setup(
    name='GPJax',
    version='0.1.5',
    author='Thomas Pinder',
    author_email='t.pinder2@lancaster.ac.uk',
    packages=['gpjax'],  #, 'package_name.test'],
    # scripts=['bin/script1', 'bin/script2'],
    # url='http://pypi.python.org/pypi/PackageName/',
    license='LICENSE',
    description=
    'Didactic Gaussian processes in Jax and ObJax.',
    long_description="GPJax aims to provide a low-level interface to Gaussian process models. Code is written entirely in Jax and Objax to enhance readability, and structured so as to allow researchers to easily extend the code to suit their own needs. When defining GP prior in GPJax, the user need only specify a mean and kernel function. A GP posterior can then be realised by computing the product of our prior with a likelihood function. The idea behind this is that the code should be as close as possible to the maths that we would write on paper when working with GP models.",
    install_requires=parse_requirements_file("requirements.txt"),
    # entry_points={
    #     "console_scripts": [
    #         "gpjax=gpjax.__main__:main",
    #     ]
    # },
)   
