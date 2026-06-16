# (1) Import — นำเข้า Library ที่จำเป็นทั้งหมด
import os
from launch import LaunchDescription
from launch.actions import DeclareLaunchArgument
from launch.substitutions import LaunchConfiguration
from launch_ros.actions import Node
from ament_index_python.packages import get_package_share_directory

# (2) Entry Point — ฟังก์ชันหลักที่ ROS2 เรียกเมื่อใช้ ros2 launch
def generate_launch_description():

    # (3) Body — เตรียม path ของ Package
    pkg_dir = get_package_share_directory('my_robot_bringup')

    # LaunchConfiguration — รับค่าจาก Argument หรือใช้ Default
    nav2_params = LaunchConfiguration('nav2_params')
    map_file    = LaunchConfiguration('map_file')

    # ประกาศ Arguments พร้อม Default Value
    declare_nav2_params = DeclareLaunchArgument(
        'nav2_params',
        default_value=os.path.join(pkg_dir, 'config', 'nav2_params.yaml'),
        description='Path to nav2 params file',
    )

    declare_map_file = DeclareLaunchArgument(
        'map_file',
        default_value=os.path.join(pkg_dir, 'map', 'my_map1.yaml'),
        description='Path to map yaml file',  # ชี้ไปยังแผนที่จาก Module 19
    )

    # ── Nav2 Nodes ────────────────────────────────────────────────────

    # โหลดแผนที่จากไฟล์ .yaml และ publish /map
    map_server = Node(
        package='nav2_map_server',
        executable='map_server',
        name='map_server',
        output='screen',
        parameters=[nav2_params, {'yaml_filename': map_file}],
    )

    # ระบุตำแหน่งหุ่นยนต์บนแผนที่ด้วย Particle Filter
    amcl = Node(
        package='nav2_amcl',
        executable='amcl',
        name='amcl',
        output='screen',
        parameters=[nav2_params],
    )

    # Local Planner — คำนวณ /cmd_vel แบบ Real-time
    controller_server = Node(
        package='nav2_controller',
        executable='controller_server',
        name='controller_server',
        output='screen',
        parameters=[nav2_params],
        remappings=[('cmd_vel', '/cmd_vel')],  # ส่งคำสั่งไปยัง Motor Driver
    )

    # Global Planner — วางเส้นทางหลักจากต้นถึงปลาย
    planner_server = Node(
        package='nav2_planner',
        executable='planner_server',
        name='planner_server',
        output='screen',
        parameters=[nav2_params],
    )

    # Behavior Server — จัดการพฤติกรรมเมื่อติดขัด (Spin, Backup)
    behavior_server = Node(
        package='nav2_behaviors',
        executable='behavior_server',
        name='behavior_server',
        output='screen',
        parameters=[nav2_params],
    )

    # BT Navigator — ควบคุม Flow ด้วย Behavior Tree
    bt_navigator = Node(
        package='nav2_bt_navigator',
        executable='bt_navigator',
        name='bt_navigator',
        output='screen',
        parameters=[nav2_params],
    )

    # Waypoint Follower — รับ Waypoint หลายจุดและเดินทางตามลำดับ
    waypoint_follower = Node(
        package='nav2_waypoint_follower',
        executable='waypoint_follower',
        name='waypoint_follower',
        output='screen',
        parameters=[nav2_params],
    )

    # Lifecycle Manager — จัดการ State ของ Nav2 Nodes ทั้งหมด
    # autostart: True = เปิดทุก Node อัตโนมัติเมื่อ Launch
    lifecycle_manager = Node(
        package='nav2_lifecycle_manager',
        executable='lifecycle_manager',
        name='lifecycle_manager_navigation',
        output='screen',
        parameters=[{
            'use_sim_time': False,
            'autostart': True,          # เปิด Node ทั้งหมดอัตโนมัติ
            'node_names': [             # รายชื่อ Node ที่ Lifecycle Manager จัดการ
                'map_server',
                'amcl',
                'controller_server',
                'planner_server',
                'behavior_server',
                'bt_navigator',
                'waypoint_follower',
            ],
        }],
    )

    # (4) Guard — Return LaunchDescription พร้อม Argument และ Node ทั้งหมด
    return LaunchDescription([
        declare_nav2_params,    # ต้องประกาศ Arguments ก่อน Nodes เสมอ
        declare_map_file,
        map_server,
        amcl,
        controller_server,
        planner_server,
        behavior_server,
        bt_navigator,
        waypoint_follower,
        lifecycle_manager,
    ])
