from setuptools import setup

setup(
      name='pySmartKD',
      version = '0.1.6',
      description = 'Functions to analyze and plot geochemical data and to predict distribution coefficients between chemical species and minerals',
      py_modules=[],
      author = 'Jadallah Zouabe',
      author_email ='jzouabe@berkeley.edu',
      license ='MIT',
      packages=[],
      install_requires=[
        'csv',
        'pandas',
        'numpy',
        'seaborn',
        'matplotlib',
        'sklearn',
        'scipy'],
      include_package_Data=True
      )

         

