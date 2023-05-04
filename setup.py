from setuptools import setup

setup(
    name='movie-manager',
    version='1.0',
    packages=['movie_manager', 'pages', 'models'],
    package_dir={'': 'src'},
    url='http://www.example.com',
    license='',
    author='KonradFeher',
    author_email='konradfeher@outlook.com',
    description='Python gyak project',
    install_requires=[
        'pathlib~=1.0.1',
        'customtkinter~=5.1.2',
        'Pillow~=9.5.0',
        'requests~=2.28.2',
        'urllib3~=1.26.15',
        'bcrypt~=4.0.1'
    ],
    entry_points={
        'console_scripts': [
            'movie-manager=movie_manager.main:main'
        ]
    },

    include_package_data=True,
)
# Kipróbáltam az összes kombinációt, az asseteket sehogy sem comagolja be.
# MANIFEST.in - nel sem, package_data-val sem.
# Bekerülnek a tarballba de installálás során nem csomagolódnak ki sehova.
# "Majd PyCharm legenerálja"
# A PyCharm kb semmit nem generál le, még a dependencyket se másolja át.
# 4 órát szenvedtem, aztán rollbackeltem mindent.

# Futtatni lehet PyCharmból.
