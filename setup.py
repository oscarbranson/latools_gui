from setuptools import setup, find_packages

setup(name='latools_gui',
      version='0.0.1',
      description='A GUI for LAtools',
      url='https://github.com/oscarbranson/latools_gui',
      author='TechLauncher Project - Team XXXXX',
      author_email='oscarbranson@gmail.com',
      license='MIT',
      packages=find_packages(),
      classifiers=['Development Status :: 4 - Beta',
                   'Intended Audience :: Science/Research',
                   'Topic :: Scientific/Engineering',
                   'Programming Language :: Python :: 2',
                   'Programming Language :: Python :: 3',
                   ],
      install_requires=['latools',
                        'PyQt5',
                        'pyqtgraph'],
      # package_data={
      # },
      zip_safe=False)