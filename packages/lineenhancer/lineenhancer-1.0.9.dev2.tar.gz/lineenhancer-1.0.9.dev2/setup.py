from setuptools import setup
# Create new package with python setup.py sdist
setup(
    name='lineenhancer',
    version='1.0.9.dev2',

    packages=['lineenhancer'],
    license='MIT',
    author='Thorsten Wagner',
    url='https://github.com/MPI-Dortmund/LineEnhancer',
    download_url='https://github.com/MPI-Dortmund/LineEnhancer/releases/download/1.0.3/lineenhancer-1.0.3.tar.gz',
    install_requires=[
        "numpy",
        "mrcfile",
        "scipy",
        "cryolo"
    ],
    author_email='thorsten.wagner@mpi-dortmund.mpg.de',
    description='Enhancing line images',
    entry_points={
        'console_scripts': [
            'line_enhancer.py = lineenhancer.line_enhancer:_main_',
            'line_enhancer_test.py = lineenhancer.line_enhancer_test:_main_']},
)