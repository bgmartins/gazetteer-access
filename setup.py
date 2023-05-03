from setuptools import setup

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