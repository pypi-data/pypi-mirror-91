from setuptools import setup

long_description = """
# Diffraction Simulations - Angular Spectrum Method
Implementation of the Angular Spectrum method in Python to simulate Diffraction Patterns with arbitrary apertures. You can use it for simulating both monochromatic and polychromatic light also with arbitrary spectrums.

How the method and the simulator work is described in this [Article](https://rafael-fuente.github.io/simulating-diffraction-patterns-with-the-angular-spectrum-method-and-python.html). Take a look to the [Youtube video](https://youtu.be/Ft8CMEooBAE) to see the animated simulations!
"""


setup(
    name='diffractsim',
    version='1.1.1',
    description='Implementation of the Angular Spectrum method in Python to simulate Diffraction Patterns',
    long_description=long_description,
    long_description_content_type="text/markdown",
    url='https://github.com/rafael-fuente/Diffraction-Simulations--Angular-Spectrum-Method',
    download_url='https://github.com/rafael-fuente/Diffraction-Simulations--Angular-Spectrum-Method/archive/main.zip',
    keywords = ['diffraction', 'angular spectrum method', 'optics', 'physics simulation'],
    author='Rafael de la Fuente',
    author_email='rafael.fuente.herrezuelo@gmail.com',
    license='MIT',
    packages=['diffractsim'],
    install_requires=['numpy', 'scipy', 'Pillow', 'matplotlib', 'progressbar'],
    classifiers=[
        # How mature is this project? Common values are
        #   3 - Alpha
        #   4 - Beta
        #   5 - Production/Stable
        'Development Status :: 5 - Production/Stable',

        # Indicate who your project is intended for
        'Intended Audience :: Science/Research',
        'Topic :: Scientific/Engineering',

        # Pick your license as you wish (should match "license" above)
        'License :: OSI Approved :: MIT License',
        'Operating System :: OS Independent',

    ],
    include_package_data = True,
    python_requires ='>=3.6',
)