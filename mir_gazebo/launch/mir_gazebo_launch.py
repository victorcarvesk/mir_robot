#!/usr/bin/env python3

from launch import LaunchDescription
from launch_ros.substitutions import FindPackageShare
from launch.actions import DeclareLaunchArgument, IncludeLaunchDescription
from launch.conditions import UnlessCondition
from launch.launch_description_sources import PythonLaunchDescriptionSource
from launch.substitutions import LaunchConfiguration, PathJoinSubstitution


def generate_launch_description():

    pkg_mir_gazebo = FindPackageShare("mir_gazebo")
    pkg_ros_gz_sim = FindPackageShare('ros_gz_sim')

    headless_mode = LaunchConfiguration('headless_mode')
    gazebo_config_file = LaunchConfiguration('gazebo_config_file')
    gazebo_verbose_level = LaunchConfiguration('gazebo_verbose_level')
    world_file = LaunchConfiguration('world_file')

    return LaunchDescription([

        DeclareLaunchArgument(
            name='world_file',
            default_value=PathJoinSubstitution([
                pkg_mir_gazebo, 'worlds', 'empty.world',
            ]),
            description='SDF world file',
        ),

        DeclareLaunchArgument(
            name='gazebo_config_file',
            default_value=PathJoinSubstitution([
                pkg_mir_gazebo, 'config', 'full_view.config'
            ]),
            description='Gazebo GUI config file',
        ),

        DeclareLaunchArgument(
            name='rviz_config_file',
            default_value=PathJoinSubstitution([
                pkg_mir_gazebo, 'rviz', 'mir_visu_full.rviz'
            ]),
            description='A display config file (.rviz) to load',
        ),

        DeclareLaunchArgument(
            name='headless_mode',
            default_value='false',
            choices=['true', 'false'],
            description='Run Gazebo without GUI',
        ),

        DeclareLaunchArgument(
            name='gazebo_verbose_level',
            default_value='1',
            choices=['0', '1', '2', '3', '4'],
            description='Adjust the level of console output (0~4).',
        ),

        #

        IncludeLaunchDescription(
            PythonLaunchDescriptionSource(
                PathJoinSubstitution([
                    pkg_ros_gz_sim, 'launch', 'gz_sim.launch.py'
                ]),
            ),
            launch_arguments={
                'gz_args': [
                    world_file,
                    ' -s -r ',
                    ' --gui-config ', gazebo_config_file,
                    ' -v ', gazebo_verbose_level,
                ],
                'on_exit_shutdown': 'true'
            }.items(),
        ),

        IncludeLaunchDescription(
            PythonLaunchDescriptionSource(
                PathJoinSubstitution([
                    pkg_ros_gz_sim, 'launch', 'gz_sim.launch.py'
                ]),
            ),
            launch_arguments={
                'gz_args': [
                    ' -g ',
                    ' -v ', gazebo_verbose_level,
                ],
                'on_exit_shutdown': 'true'
            }.items(),
            condition=UnlessCondition(headless_mode),
        ),

        IncludeLaunchDescription(
            PythonLaunchDescriptionSource([
                PathJoinSubstitution([pkg_mir_gazebo, 'launch', 'mir_spawner_launch.py']),
            ]),
        ),

    ])
