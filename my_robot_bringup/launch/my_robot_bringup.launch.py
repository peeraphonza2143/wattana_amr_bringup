# (1) Import — นำเข้า Library ที่จำเป็น
import os
from launch import LaunchDescription
from launch_ros.actions import Node
from ament_index_python.packages import get_package_share_directory

# (2) Entry Point — ฟังก์ชันหลักที่ ROS2 จะเรียกเมื่อใช้คำสั่ง ros2 launch
def generate_launch_description():

    # (3) Body — เตรียม path ไปยังไฟล์ Config ของ Laser Filter
    laser_filter_config_path = os.path.join(
        get_package_share_directory('my_robot_bringup'),  # ชื่อ Package
        'config',                                          # โฟลเดอร์ย่อย
        'laser_filter.yaml'                                # ชื่อไฟล์ Config
    )

    return LaunchDescription([

        # --- Node ที่ 1: TF Static Transform (base_link → laser) ---
        # ทำหน้าที่: บอกตำแหน่งติดตั้ง LiDAR เทียบกับฐานหุ่นยนต์
        # (Node นี้มีอยู่แล้วจาก Module 16 — ไม่ต้องแก้ไข)
        Node(
            package='tf2_ros',
            executable='static_transform_publisher',
            name='static_tf_pub_laser',
            output='screen',
            # arguments: x      y    z     yaw    pitch roll  parent      child
            arguments=['0.27', '0', '0.38', '3.14', '0', '0', 'base_link', 'laser'],
        ),

        # --- Node ที่ 2: Laser Filter Node (เพิ่มใหม่ใน Module 17) ---
        # ทำหน้าที่: รับ /scan -> กรองตาม laser_filter.yaml -> ส่งออก /scan_filtered
        Node(
            package='laser_filters',                       # Package ที่ให้บริการ Filter
            executable='scan_to_scan_filter_chain',        # โปรแกรม Filter สำหรับ LaserScan
            name='laser_filter',                           # ชื่อ Node ใน ROS2 Graph
            parameters=[laser_filter_config_path],         # โหลดกฎการกรองจาก yaml
            remappings=[
                ('/scan', '/scan'),                        # Input: รับข้อมูลดิบจาก LiDAR
                ('/scan_filtered', '/scan_filtered'),      # Output: ส่งข้อมูลที่กรองแล้ว
            ],
            output='screen',
        ),

    # (4) Guard — ปิด LaunchDescription (จบ return)
    ])
