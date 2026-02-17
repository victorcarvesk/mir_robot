#!/usr/bin/env python3

from launch import LaunchDescription
from launch_ros.actions import Node, PushRosNamespace
from launch_ros.descriptions import ParameterValue
from launch_ros.substitutions import FindPackageShare
from launch.actions import DeclareLaunchArgument, TimerAction
from launch.conditions import IfCondition
from launch.substitutions import LaunchConfiguration, Command, PathJoinSubstitution


def generate_launch_description():

    pkg_mir_description = FindPackageShare('mir_description')

    namespace = LaunchConfiguration('namespace')
    rviz_config_file = LaunchConfiguration('rviz_config_file')
    use_rviz = LaunchConfiguration('use_rviz')
    use_sim_time = LaunchConfiguration('use_sim_time')
    xacro_file = LaunchConfiguration('xacro_file')
    debug_mode = LaunchConfiguration('debug_mode')

    robot_description = ParameterValue(
        Command([
            'xacro ', xacro_file,
        ]),
        value_type=str,
    )

    return LaunchDescription([

        DeclareLaunchArgument(
            name='xacro_file',
            default_value=PathJoinSubstitution([
                pkg_mir_description, 'urdf', 'mir100_description.urdf.xacro',
            ]),
            description='xacro file to load',
        ),

        DeclareLaunchArgument(
            name='namespace',
            default_value='',
            description='Namespace to push all topics to'
        ),

        DeclareLaunchArgument(
            name='use_sim_time',
            default_value='false',
            choices=['true', 'false'],
            description='Use simulator clock',
        ),

        DeclareLaunchArgument(
            name='use_rviz',
            description='Use RViz if true',
            choices=['true', 'false'],
            default_value='false',
        ),

        DeclareLaunchArgument(
            name='rviz_config_file',
            default_value=PathJoinSubstitution([
                pkg_mir_description, 'rviz', 'mir_description.rviz',
            ]),
            description='A display config file (.rviz) to load',
        ),

        DeclareLaunchArgument(
            name='debug_mode',
            choices=['true', 'false'],
            default_value='false',
            description='If true, launch rqt_graph and rqt_tf_tree',
        ),

        PushRosNamespace(namespace),

        Node(
            package='robot_state_publisher',
            executable='robot_state_publisher',
            name='robot_state_publisher',
            output='both',
            parameters=[{
                'robot_description': robot_description,
                'use_sim_time': use_sim_time,
            }],
            remappings=[
                ('/tf', 'tf'),
                ('/tf_static', 'tf_static'),
            ],
        ),

        Node(
            package='rqt_tf_tree',
            executable='rqt_tf_tree',
            output='both',
            remappings=[
                ('/tf', 'tf'),
                ('/tf_static', 'tf_static')
            ],
            condition=IfCondition(debug_mode),
        ),

        Node(
            package='rqt_graph',
            executable='rqt_graph',
            output='both',
            condition=IfCondition(debug_mode),
        ),

        TimerAction(
            period=2.0,
            actions=[
                Node(
                    package='rviz2',
                    executable='rviz2',
                    output={'both': 'log'},
                    parameters=[{
                        'use_sim_time': use_sim_time,
                    }],
                    arguments=['-d', rviz_config_file],
                    remappings=[
                        ('/robot_description', 'robot_description'),
                        ('/clicked_point', 'clicked_point'),
                        ('/goal_pose', 'goal_pose'),
                        ('/initialpose', 'initialpose'),
                        ('/tf', 'tf'),
                        ('/tf_static', 'tf_static'),
                    ],
                    condition=IfCondition(use_rviz),
                ),
            ],
        ),

    ])
