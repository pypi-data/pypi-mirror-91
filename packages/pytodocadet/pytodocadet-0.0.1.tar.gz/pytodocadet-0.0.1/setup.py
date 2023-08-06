from setuptools import setup, find_packages

def readme():
    with open('README.md') as f:
        return f.read()

setup(
    name='pytodocadet',
    version='0.0.1',
    description='Simple and robust "ToDo Application" with Drag-Drop functionality.',
    long_description=readme(),
    long_description_content_type="text/markdown",
    author='Halil Emre Cadet',
    author_email='halilemrecadet@gmail.com',
    url='https://github.com/emrex32/pytodo-cadet',
    install_requires=['PyQt5'],
    py_modules=["pytodocadet"],
    package_dir={'': 'src'},
    license='MIT',
    classifiers=[
        'Development Status :: 5 - Production/Stable',
        'License :: OSI Approved :: MIT License',
        'Programming Language :: Python :: 3',
        'Operating System :: OS Independent'
    ],
    keywords='core package',
    include_package_data=True,
    zip_safe=False)
    
