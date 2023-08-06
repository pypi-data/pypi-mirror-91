from setuptools import setup
import pathlib
here = pathlib.Path('README.md').parent.resolve()

setup(
    name = 'UltimateChemCalc',
    packages = ['UltimateChemCalc'],
    description='A collection of chemistry-related conversion calculators.',
    long_description=(here / 'README.md').read_text(encoding='utf-8'),
    long_description_content_type='text/markdown',
    version = '2.25',
    license='MIT',
    author = 'Harold J. Iwen',
    author_email = 'inventorsniche349@gmail.com',
    url = 'https://www.inventorsniche.com',
    download_url = 'https://github.com/Hiwen-STEM/UltimateChemCalc',
    keywords = ['Chemistry', 'Mole', 'Stoichiometry','Conversion','Chemical','Equation'],
    install_requires=[
        'periodictable',
        'wxPython',
        'sympy',
    ],
    classifiers=[
        'Development Status :: 3 - Alpha',
        'Intended Audience :: Developers',
        'Topic :: Software Development :: Build Tools',
        'License :: OSI Approved :: MIT License',
        'Programming Language :: Python :: 3.6',     
        'Programming Language :: Python :: 3.7',
        'Programming Language :: Python :: 3.8',
    ]
)
