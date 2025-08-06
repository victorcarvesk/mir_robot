#!/usr/bin/env python3

from launch import LaunchDescription
from launch_ros.actions import Node
from launch_ros.substitutions import FindPackageShare
from launch.actions import IncludeLaunchDescription, DeclareLaunchArgument
from launch.conditions import IfCondition
from launch.launch_description_sources import PythonLaunchDescriptionSource
from launch.substitutions import LaunchConfiguration, PathJoinSubstitution


def generate_launch_description():
    
    pkg_mir_description = FindPackageShare("mir_description")
    pkg_mir_control = FindPackageShare("mir_control")
    pkg_mir_gazebo = FindPackageShare("mir_gazebo")
    
    use_bridge = LaunchConfiguration('use_bridge')
    bridge_config_file = LaunchConfiguration('bridge_config_file')
    use_sim_time = LaunchConfiguration('use_sim_time')

    initial_pos_x = LaunchConfiguration('initial_pos_x')
    initial_pos_y = LaunchConfiguration('initial_pos_y')
    initial_pos_z = LaunchConfiguration('initial_pos_z')
    initial_pos_roll = LaunchConfiguration('initial_pos_roll')
    initial_pos_pitch = LaunchConfiguration('initial_pos_pitch')
    initial_pos_yaw = LaunchConfiguration('initial_pos_yaw')
    
    return LaunchDescription([

        DeclareLaunchArgument(
            name='xacro_file',
            default_value=PathJoinSubstitution([
                pkg_mir_gazebo, 'urdf', 'mir100_gazebo.urdf.xacro'
            ]),
            description='load xacro file',
        ),

        DeclareLaunchArgument(
            name='rviz_config_file',
            default_value=PathJoinSubstitution([
                pkg_mir_gazebo, 'rviz', 'mir_visu_full.rviz'
            ]),
            description='A display config file (.rviz) to load',
        ),

        DeclareLaunchArgument(
            name='use_bridge',
            default_value='true',
            choices=['true', 'false'],
            description='Use gazebo bridge if true',
        ),

        DeclareLaunchArgument(
            name='bridge_config_file',
            default_value=PathJoinSubstitution([
                pkg_mir_gazebo, 'config', 'mir_bridge.yaml'
            ]),
            description='load bridge yaml file',
        ),

        DeclareLaunchArgument(
            name='use_sim_time',
            default_value='true',
            choices=['true', 'false'],
            description='Enable simulation mode if true',
        ),

        DeclareLaunchArgument(
            name='initial_pos_x',
            default_value='-2.0',
            description='Initial pose on axis X (in meters)',
        ),

        DeclareLaunchArgument(
            name='initial_pos_y',
            default_value='-0.5',
            description='Initial pose on axis Y (in meters)',
        ),

        DeclareLaunchArgument(
            name='initial_pos_z',
            default_value='0.0',
            description='Initial pose on axis Z (in meters)',
        ),

        DeclareLaunchArgument(
            name='initial_pos_roll',
            default_value='0.0',
            description='Initial pose roll (in radians)',
        ),

        DeclareLaunchArgument(
            name='initial_pos_pitch',
            default_value='0.0',
            description='Initial pose pitch (in radians)',
        ),

        DeclareLaunchArgument(
            name='initial_pos_yaw',
            default_value='0.0',
            description='Initial pose yaw (in radians)',
        ),

        IncludeLaunchDescription(
            PythonLaunchDescriptionSource([
                PathJoinSubstitution([pkg_mir_description, 'launch', 'mir_launch.py']),
            ]),
        ),

        IncludeLaunchDescription(
            PythonLaunchDescriptionSource([
                PathJoinSubstitution([pkg_mir_control, 'launch', 'mir_controllers_launch.py']),
            ]),
        ),

        Node(
            package='ros_gz_bridge',
            executable='parameter_bridge',
            parameters=[{
                'config_file': bridge_config_file,
                # 'qos_overrides./tf_static.publisher.durability': 'transient_local',
            }],
            output='both',
            condition=IfCondition(use_bridge), # [NOTE] maybe not necessary
        ),

        Node(
            package='ira_laser_tools',
            name='mir_laser_scan_merger',
            executable='laserscan_multi_merger',
            parameters=[{
                'laserscan_topics': "b_scan f_scan",
                'destination_frame': "virtual_laser_link",
                'scan_destination_topic': "scan",
                'cloud_destination_topic': "scan_cloud",
                'min_height': -0.25,
                'max_completion_time': 0.05,
                'max_merge_time_diff': 0.005,
                'use_sim_time': use_sim_time,
                'best_effort': False
            }],
            output='screen',
        ),

        Node(
            package='ros_gz_sim',
            executable='create',
            output='screen',
            arguments=[
                '-topic', 'robot_description',
                '-x', initial_pos_x,
                '-y', initial_pos_y,
                '-z', initial_pos_z,
                '-R', initial_pos_roll,
                '-P', initial_pos_pitch,
                '-Y', initial_pos_yaw,
            ],
        ),
    ])

