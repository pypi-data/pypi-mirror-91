from setuptools import setup, find_packages

VERSION = '0.0.4' 
DESCRIPTION = 'Package for infoblox bloxone users'
LONG_DESCRIPTION = 'Initial package for infoblox bloxone'

# Setting up
setup(
       # the name must match the folder name 'verysimplemodule'
        name="blox1module", 
        version=VERSION,
        author="Amit Mishra",
        author_email="amithrh@gmail.com",
        description=DESCRIPTION,
        long_description=LONG_DESCRIPTION,
        packages=find_packages(),
        install_requires=[], # add any additional packages that 
        # needs to be installed along with your package. Eg: 'caer'
        
        keywords=['python', 'first package'],
        classifiers= [
            "Development Status :: 1 - Planning",
            "Intended Audience :: Education",
            "Programming Language :: Python :: 2",
            "Operating System :: MacOS :: MacOS X",
        ]
)
