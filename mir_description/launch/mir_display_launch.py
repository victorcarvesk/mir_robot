#!/usr/bin/env python3

from launch import LaunchDescription
from launch_ros.actions import Node
from launch_ros.substitutions import FindPackageShare
from launch.actions import DeclareLaunchArgument, IncludeLaunchDescription
from launch.conditions import IfCondition, UnlessCondition
from launch.launch_description_sources import PythonLaunchDescriptionSource
from launch.substitutions import LaunchConfiguration, PathJoinSubstitution


def generate_launch_description():

    pkg_mir_description = FindPackageShare('mir_description')

    rviz_config_file = LaunchConfiguration('rviz_config_file')
    hidden_joint_state = LaunchConfiguration('hidden_joint_state')

    return LaunchDescription([

        DeclareLaunchArgument(
            name='hidden_joint_state',
            default_value='false',
            description='Enable to publish joint states using joint state publisher'
        ),
        
        DeclareLaunchArgument(
            name='rviz_config_file',
            default_value=PathJoinSubstitution([
                pkg_mir_description, 'rviz', 'mir_description.rviz'
            ]),
            description='A display config file (.rviz) to load',
        ),

        IncludeLaunchDescription(
            PythonLaunchDescriptionSource([
                PathJoinSubstitution([
                    pkg_mir_description, 'launch', 'mir_launch.py',
                ]),
            ]),
            launch_arguments={
                'use_rviz': 'true',
                'rviz_config_file': rviz_config_file,
            }.items(),
        ),

        Node(
            package='joint_state_publisher',
            executable='joint_state_publisher',
            output='both',
            condition=IfCondition(hidden_joint_state),
        ),

        Node(
            package='joint_state_publisher_gui',
            executable='joint_state_publisher_gui',
            output='both',
            condition=UnlessCondition(hidden_joint_state),
        ),
    ])
