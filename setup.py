import pkg_resources
import gazetteer_access
from setuptools import setup
from setuptools.command.develop import develop
from setuptools.command.install import install

class PostDevelopCommand(develop):
    """Post-installation for development mode."""
    def run(self):
        develop.run(self)
        db = pkg_resources.resource_filename(__name__, 'gazetteer.db')
        gazetteer_access.create_database(db)

class PostInstallCommand(install):
    """Post-installation for installation mode."""
    def run(self):
        install.run(self)
        db = pkg_resources.resource_filename(__name__, 'gazetteer.db')
        gazetteer_access.create_database(db)        

setup(
    name='gazetteer_access',
    version='0.1.0',    
    description="Simple Python library supporting the access to the who's on first gazetteer data.",
    url='https://github.com/bgmartins/gazetteer-access',
    author='Bruno Martins',
    author_email='bgmartins@gmail.com',
    license='BSD 2-clause',
    packages=['gazetteer_access'],
    install_requires=['rasterio', 'rasterstats', 'spatialite', 'geojson', ],
    include_package_data=True,
    package_data={'': ['*.db']},
    cmdclass={
        'develop': PostDevelopCommand,
        'install': PostInstallCommand,
    },

    classifiers=[
        'Development Status :: 1 - Planning',
        'Intended Audience :: Science/Research',
        'License :: OSI Approved :: BSD License',  
        'Operating System :: POSIX :: Linux',        
        'Programming Language :: Python :: 3',
        'Programming Language :: Python :: 3.4',
        'Programming Language :: Python :: 3.5',
    ],
)