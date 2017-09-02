from setuptools import setup, find_packages

version = '0.0.1'

tests_require=[
    'WebTest >= 1.3.1',  # py3 compat
    'pytest',
    'pytest-cov'
],

setup(name='skyskraper',
      version=version,
      description="SkyTrak golf shot analytics tool",
      long_description=open("README.md").read() + "\n" +
                       open("HISTORY.txt").read(),
      # Get more strings from
      # http://pypi.python.org/pypi?:action=list_classifiers
      classifiers=[
        'Development Status :: 4 - Beta',
        'Environment :: Console',
        'Framework :: Pyramid',
        'Intended Audience :: Developers',
        'License :: Other/Proprietary License',
        'Natural Language :: English',
        "Programming Language :: Python :: 2",
        'Programming Language :: Python :: 2.7',
        'Programming Language :: Python :: 3',
      ],
      author='David Davis',
      author_email='davisd50@gmail.com',
      url='https://github.com/davisd50/skyskraper',
      packages=find_packages(exclude=['ez_setup']),
      include_package_data=True,
      package_data = {
          '': ['*.zcml', '*.xml', '*.yml', '*.yaml']
        },
      zip_safe=False,
      install_requires=[
          'setuptools',
          'zope.interface',
          'zope.location',
          'sqlalchemy',
          'sparc.config'
      ],
      extras_require={
            'testing': tests_require,
      },
      )
