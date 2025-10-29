#!/usr/bin/env python3
"""
mapping_livox_sim.launch.py
---------------------------------
Launches LIO-SAM for Livox-based Gazebo simulation
compatible with your slam_ws PX4-Gazebo pipeline.
"""

import os
from ament_index_python.packages import get_package_share_directory
from launch import LaunchDescription
from launch.actions import DeclareLaunchArgument
from launch.substitutions import LaunchConfiguration
from launch_ros.actions import Node


def generate_launch_description():
    # --- Paths ---
    share_dir = get_package_share_directory('lio_sam')
    params_path = os.path.join(share_dir, 'config', 'params_livox_sim.yaml')
    rviz_config = os.path.join(share_dir, 'config', 'rviz2.rviz')


    # --- Launch arguments ---
    declare_params = DeclareLaunchArgument(
        'params_file',
        default_value=params_path,
        description='Parameter file for Livox-simulation setup.'
    )

    # --- Nodes ---
    nodes = [

        # ---- Core LIO-SAM pipeline ----
        Node(
            package='lio_sam',
            executable='lio_sam_imuPreintegration',
            name='lio_sam_imuPreintegration',
            parameters=[LaunchConfiguration('params_file')],
            output='screen'
        ),
        Node(
            package='lio_sam',
            executable='lio_sam_imageProjection',
            name='lio_sam_imageProjection',
            parameters=[LaunchConfiguration('params_file')],
            output='screen'
        ),
        Node(
            package='lio_sam',
            executable='lio_sam_featureExtraction',
            name='lio_sam_featureExtraction',
            parameters=[LaunchConfiguration('params_file')],
            output='screen'
        ),
        Node(
            package='lio_sam',
            executable='lio_sam_mapOptimization',
            name='lio_sam_mapOptimization',
            parameters=[LaunchConfiguration('params_file')],
            output='screen'
        ),

        # ---- Static transforms ----
        Node(
            package='tf2_ros',
            executable='static_transform_publisher',
            name='map_to_camera_init',
            arguments=['0', '0', '0', '0', '0', '0', 'map', 'camera_init'],
            parameters=[{'use_sim_time': True}],
            output='screen'
        ),
        Node(
            package='tf2_ros',
            executable='static_transform_publisher',
            name='map_to_odom',
            arguments=['0', '0', '0', '0', '0', '0', 'map', 'odom'],
            parameters=[{'use_sim_time': True}],
            output='screen'
        ),

        # ---- RViz visualization ----
        Node(
            package='rviz2',
            executable='rviz2',
            name='rviz2',
            arguments=['-d', rviz_config],
            parameters=[{'use_sim_time': True}],
            output='screen'
        ),
    ]

    return LaunchDescription([declare_params] + nodes)
