from setuptools import setup, find_packages

version = '0.46.01'

if __name__ == "__main__":
    with open('requirements.txt') as f:
        requirements = f.read().splitlines()

    setup(name='ttlab',
          version=version,
          description='Physics lab equipment analysis software',
          # long_description_content_type='text/markdown',
          long_description=open("README.rst").read(),
          url='',
          author='Christopher Tiburski and Johan Tenghamn',
          author_email='info@ttlab.se',
          license='MIT',
          packages=find_packages(),
          install_requires=requirements,
          keywords='XPS Cary5000 MassSpec Mass spectrometer Light spectrometer Insplorion Physics Analysis Pfeiffer Multipak Plasmonics Activation energy X0Reactor Plasmons',
          classifiers=['Development Status :: 4 - Beta', 'Programming Language :: Python :: 3.6', 'Intended Audience :: Science/Research',
                       'Topic :: Scientific/Engineering :: Physics'],
          zip_safe=False)
