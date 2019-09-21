from setuptools import setup


def readme():
    with open('README.md') as f:
        return f.read()


setup(name='essentials',
      version='1.0.9',
      description='Core classes and functions, reusable in any kind of Python application',
      long_description=readme(),
      long_description_content_type='text/markdown',
      classifiers=[
          'Development Status :: 5 - Production/Stable',
          'License :: OSI Approved :: MIT License',
          'Programming Language :: Python :: 3',
          'Operating System :: OS Independent'
      ],
      url='https://github.com/RobertoPrevato/essentials',
      author='RobertoPrevato',
      author_email='roberto.prevato@gmail.com',
      keywords='core utilities',
      license='MIT',
      packages=['essentials',
                'essentials.typesutils',
                'essentials.decorators'],
      install_requires=[],
      include_package_data=True,
      zip_safe=False)
