# (1) Import — นำเข้า Library ที่จำเป็นทั้งหมด
import os
from launch import LaunchDescription
from launch.actions import DeclareLaunchArgument
from launch.substitutions import LaunchConfiguration
from launch_ros.actions import Node
from ament_index_python.packages import get_package_share_directory

# (2) Entry Point — ฟังก์ชันหลักที่ ROS2 จะเรียกเมื่อใช้คำสั่ง ros2 launch
def generate_launch_description():

    # (3) Body — เตรียม path ของ Package และ Config File
    pkg_dir = get_package_share_directory('my_robot_bringup')

    # กำหนด LaunchConfiguration สำหรับ path ของ Config
    # (ช่วยให้สามารถ Override ค่าได้จาก Command Line ได้)
    slam_params_file = LaunchConfiguration('slam_params_file')

    # ประกาศ Argument พร้อม Default Value ที่ชี้ไปยังไฟล์ yaml ใน Package
    declare_slam_params = DeclareLaunchArgument(
        'slam_params_file',
        default_value=os.path.join(
            pkg_dir,
            'config',
            'mapper_params_online_async.yaml'   # ไฟล์ Config ที่สร้างในขั้นตอน 4.2
        ),
        description='Path to slam_toolbox config file',
    )

    # กำหนด SLAM Toolbox Node
    slam_node = Node(
        package='slam_toolbox',                    # Package ของ SLAM Toolbox
        executable='async_slam_toolbox_node',      # โหมด Async (ไม่ Block การทำงานอื่น)
        name='slam_toolbox',                       # ชื่อ Node ใน ROS2 Graph
        output='screen',                           # แสดง Log ออกที่ Terminal
        parameters=[slam_params_file],             # โหลด Config จากไฟล์ yaml
    )

    # (4) Guard — Return LaunchDescription พร้อม Argument และ Node
    return LaunchDescription([
        declare_slam_params,   # ต้องประกาศ Argument ก่อน Node เสมอ
        slam_node,
    ])
