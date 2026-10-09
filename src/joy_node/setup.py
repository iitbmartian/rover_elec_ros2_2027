import glob
from setuptools import find_packages, setup

package_name = 'joy_node'

setup(
    name=package_name,
    version='0.0.0',
    packages=find_packages(exclude=['test']),
    data_files=[
        ('share/ament_index/resource_index/packages',
            ['resource/' + package_name]),
        ('share/' + package_name, ['package.xml']),
        ('share/' + package_name + '/launch', glob.glob('launch/*.launch.py')),
        ('share/' + package_name + '/config', glob.glob('config/*.yaml')),
    ],
    install_requires=['setuptools'],
    zip_safe=True,
    maintainer='ritvik',
    maintainer_email='ritviknainawatee3@gmail.com',
    description='TODO: Package description',
    license='TODO: License declaration',
    extras_require={
        'test': [
            'pytest',
        ],
    },
    entry_points={
        'console_scripts': [
            'joy_node = joy_node.joy_node:main',
            'joy_translator = joy_node.joy_translator:main',
            'joy_velocity = joy_node.joy_velocity:main',
            'dummy_joy = joy_node.dummy_joy:main',
        ],
    },
)
