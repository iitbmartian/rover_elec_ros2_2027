import glob

from setuptools import find_packages, setup

package_name = 'arm_control'

setup(
    name=package_name,
    version='0.0.0',
    packages=find_packages(exclude=['test']),
    data_files=[
        ('share/ament_index/resource_index/packages',
            ['resource/' + package_name]),
        ('share/' + package_name, ['package.xml']),
        ('share/' + package_name + '/launch', glob.glob('launch/*.launch.py')),
        ('share/' + package_name + '/rviz', glob.glob('rviz/*.rviz')),
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
            'odrive_testing = arm_control.odrive_testing:main',
            'arm_brakes = arm_control.arm_brakes:main',
            'arm_ik = arm_control.arm_ik:main',
            'joint_state_bridge = arm_control.joint_state_bridge:main',
            'wrist_controller = arm_control.wrist_controller:main',
        ],
    },
)
