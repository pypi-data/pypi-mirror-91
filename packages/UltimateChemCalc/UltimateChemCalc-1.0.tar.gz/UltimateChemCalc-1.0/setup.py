from distutils.core import setup
setup(
  name = 'UltimateChemCalc',         # How you named your package folder (MyLib)
  packages = ['UltimateChemCalc'],   # Chose the same as "name"
  version = '1.0',      # Start with a small number and increase it with every change you make
  license='MIT',        # Chose a license from here: https://help.github.com/articles/licensing-a-repository
  description = 'This package comes with an entire collection of chemistry calculators. Topics\ninclude basic mole conversions, stoichiometry, molarity, and balancing problems. Furthermore,\nthe second file represents a graphical program containing all calculators that will run upon\nbeing imported; this program can be included via #import FILE# within the local\nscope of a function (this way users can choose when to launch the program). Examples\nare covered below...',   # Give a short description about your library
  author = 'Harold J. Iwen',                   # Type in your name
  author_email = 'inventorsniche349@gmail.com',      # Type in your E-Mail
  url = 'www.inventorsniche.com',   # Provide either the link to your github or to your website
  download_url = 'https://github.com/Hiwen-STEM/UltimateChemCalc',
  keywords = ['Chemistry', 'Mole', 'Stoichiometry','Conversion','Chemical','Equation','Balancing','Chemical_Equation_Balancing'],   # Keywords that define your package best
  install_requires=[            # I get to this in a second
          'periodictable',
          'wxPython',
          'sympy',
      ],
  classifiers=[
    'Development Status :: 3 - Alpha',      # Chose either "3 - Alpha", "4 - Beta" or "5 - Production/Stable" as the current state of your package
    'Intended Audience :: Developers',      # Define that your audience are developers
    'Topic :: Software Development :: Build Tools',
    'License :: OSI Approved :: MIT License',   # Again, pick a license     
    'Programming Language :: Python :: 3.6',    #Specify which pyhton versions that you want to support
    'Programming Language :: Python :: 3.7',
    'Programming Language :: Python :: 3.8',
  ],
)
