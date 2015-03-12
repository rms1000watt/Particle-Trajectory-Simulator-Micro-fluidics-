from setuptools import setup,find_packages

with open('README.rst') as f:
    readme = f.read()
    
setup(name='ptspy',
      version='1.2.0b1',
      author='Ryan Matthew Smith',
      author_email='rms1000watt@gmail.com',
      url='https://github.com/pypa/sampleproject',
      license='MIT',
      description='Particle trajectory simulator for Python.',
      long_description=readme,
      packages=find_packages(),
      classifiers=[
            'Development Status :: 4 - Beta',            
            'Intended Audience :: Scientists/Biomedical Engineers',
            'Topic :: Simulation :: Particle Trajectory',
            'License :: OSI Approved :: MIT License',
            'Programming Language :: Python :: 2.7',
        ],
      install_requires = ['numpy']
      )