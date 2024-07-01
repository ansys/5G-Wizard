
from setuptools import setup
  
setup(
    name='5G_wizard',
    version='0.3.2',
    description='The Ansys 5G Wizard can be used to calculate Power Density or Cumulative Distribution Function. These calculations use a codebook to define the mag/phase value on ports for each beam ID. The codebook definition will be imported into your HFSS design, where you can now control the mag/phase on all ports by simply changing the post processing variable “BeamID.”',
    author='Arien Sligar',
    author_email='arien.sligar@ansys.com',
    packages=['my_package'],
    install_requires=[
        'numpy',
        'pandas',
    ],
)