import os

from ament_index_python.packages import get_package_share_directory
from launch import LaunchDescription
from launch.actions import IncludeLaunchDescription
from launch_ros.actions import Node
from launch.launch_description_sources import PythonLaunchDescriptionSource
from launch.substitutions import LaunchConfiguration

def generate_launch_description():
    use_sim_time = LaunchConfiguration('use_sim_time', default='true')

    sdf_dir = os.path.join(get_package_share_directory(
        'megarover_samples_ros2'), 'models/vmegarover')
    sdf_file = os.path.join(sdf_dir, 'vmegarover.sdf')
    launch_file_dir = os.path.join(get_package_share_directory('megarover_samples_ros2'), 'launch')
    pkg_gazebo_ros = get_package_share_directory('gazebo_ros')

    gazebo = IncludeLaunchDescription(
        PythonLaunchDescriptionSource(
            os.path.join(pkg_gazebo_ros, 'launch', 'gazebo.launch.py')
        ),
    )

    spawn_entiry = Node(
        package='gazebo_ros',
        executable='spawn_entity.py',
        name='spawn_entity',
        output='screen',
        arguments=[
                '-entity', 'vmegarover',
                '-x', '0',
                '-y', '0',
                '-z', '1',
                '-file', sdf_file,
        ]
    )

    robot_state_publisher_launch = IncludeLaunchDescription(
        PythonLaunchDescriptionSource(
            [launch_file_dir, '/robot_state_publisher.launch.py']),
        launch_arguments={'use_sim_time': use_sim_time}.items(),
    )

    cmd_vel_and_odom_relay = IncludeLaunchDescription(
        PythonLaunchDescriptionSource([launch_file_dir, '/cmd_vel_and_odom_relay.launch.py']))

    return LaunchDescription([
        gazebo,
        spawn_entiry,
        robot_state_publisher_launch,
        cmd_vel_and_odom_relay
    ])
