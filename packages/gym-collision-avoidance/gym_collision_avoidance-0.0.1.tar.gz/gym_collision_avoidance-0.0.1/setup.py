from setuptools import setup, find_packages

with open("README.md", "r", encoding="utf-8") as fh:
    long_description = fh.read()

setup(
    name='gym_collision_avoidance',
    version='0.0.1',
    description='Simulation environment for collision avoidance',
    long_description=long_description,
    long_description_content_type="text/markdown",
    url='https://github.com/mit-acl/gym-collision-avoidance',
    author='Michael Everett, Yu Fan Chen, Jonathan P. How, MIT',  # Optional
    keywords='robotics planning gym rl',  # Optional
    python_requires='>=3.6, <3.8',
    install_requires=[
        'tensorflow==1.15.2',
        'Pillow',
        'PyOpenGL',
        'pyyaml',
        'matplotlib>=3.0.0',
        'shapely',
        'pytz',
        'imageio==2.4.1',
        'gym',
        'moviepy',
        'pandas',
        'stable_baselines',
    ],
    packages=find_packages(),
    include_package_data=True,
)