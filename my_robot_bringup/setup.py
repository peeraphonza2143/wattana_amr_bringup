# (1) Import — นำเข้า Library สำหรับ Package Setup
import os
from glob import glob
from setuptools import find_packages, setup

package_name = 'my_robot_bringup'

# (2) Entry Point — กำหนด Metadata และรายการไฟล์ที่ต้อง Install
setup(
    name=package_name,
    version='0.0.1',
    packages=find_packages(exclude=['test']),
    data_files=[
        # ลงทะเบียน Package กับ ament index (จำเป็นทุก Package)
        ('share/ament_index/resource_index/packages',
            ['resource/' + package_name]),
        ('share/' + package_name, ['package.xml']),

        # ✅ Install ทุกไฟล์ .launch.py ในโฟลเดอร์ launch/
        (os.path.join('share', package_name, 'launch'),
            glob('launch/*.launch.py')),

        # ✅ Install ทุกไฟล์ .yaml ในโฟลเดอร์ config/
        (os.path.join('share', package_name, 'config'),
            glob('config/*.yaml')),

        # ✅ Install ทุกไฟล์ในโฟลเดอร์ map/ (แผนที่จาก Module 19)
        (os.path.join('share', package_name, 'map'),
            glob('map/*')),
    ],
    install_requires=['setuptools'],
    zip_safe=True,
    maintainer='your_name',               # ← เปลี่ยนเป็นชื่อของคุณ
    maintainer_email='your@email.com',    # ← เปลี่ยนเป็น Email ของคุณ
    description='Launch files for bringing up the AMR robot',
    license='Apache-2.0',
    entry_points={
        'console_scripts': [],
    },
)
