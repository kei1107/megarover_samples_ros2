import os

from ament_index_python.packages import get_package_share_directory
from launch import LaunchDescription
from launch.actions import DeclareLaunchArgument
from launch.actions import IncludeLaunchDescription
from launch_ros.actions import Node
from launch.launch_description_sources import PythonLaunchDescriptionSource
from launch.substitutions import LaunchConfiguration

def generate_launch_description():
    use_sim_time = LaunchConfiguration('use_sim_time', default='true')
    config_dir = os.path.join(get_package_share_directory('megarover_samples_ros2'), 'config')
    config_file = os.path.join(config_dir, 'mapper_params_online_sync.yaml')

    slam_toolbox_launch_file_dir = os.path.join(
        get_package_share_directory('slam_toolbox'), 'launch')
    rviz_config_dir = os.path.join(get_package_share_directory('megarover_samples_ros2'), 'rviz')
    rviz_config_file = os.path.join(rviz_config_dir, 'mapping.rviz')

    return LaunchDescription([
        DeclareLaunchArgument(
            'use_sim_time',
            default_value='false',
            description='Use simulation (Gazebo) clock if true'),

        IncludeLaunchDescription(
            PythonLaunchDescriptionSource(
                [slam_toolbox_launch_file_dir, '/online_sync_launch.py']),
            launch_arguments={
                'use_sim_time': use_sim_time,
                'slam_params_file': config_file}.items()
        ),

        Node(
            package='rviz2',
            executable='rviz2',
            name='rviz2',
            output='screen',
            arguments=['-d', rviz_config_file],
            parameters=[{'use_sim_time': use_sim_time}]),
    ])

