import setuptools

setuptools.setup(
    name='caktin',
    version='v0.1.0',
    author='Lionel Gulich',
    author_email='lgulich@ethz.ch',
    url='https://github.com/lgulich/caktin',
    download_url="https://github.com/lgulich/caktin/archive/v0.1.0.tar.gz",
    description='A tool for compiling cakti.',
    install_requires=[],
    classifiers=[
        'Programming Language :: Python :: 3 :: Only',
        'License :: OSI Approved :: GNU General Public License v3 (GPLv3)',
        'Operating System :: POSIX :: Linux',
        'Natural Language :: English',
    ],
    license='Closed',
    scripts=[
        'scripts/caktin',
    ],
    python_requires='>=3.6',
)
