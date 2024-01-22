import os

from ament_index_python.packages import get_package_share_directory
from launch import LaunchDescription
from launch.actions import DeclareLaunchArgument, IncludeLaunchDescription, RegisterEventHandler, ExecuteProcess
from launch.event_handlers import OnProcessExit
from launch_ros.actions import Node
from launch.launch_description_sources import PythonLaunchDescriptionSource
from launch.substitutions import LaunchConfiguration, FindExecutable


def generate_launch_description():
    world_file_name = 'vmegarover_sample.world'
    world = os.path.join(get_package_share_directory(
        'megarover_samples_ros2'), 'worlds', world_file_name)

    declare_use_ros2_control = DeclareLaunchArgument(
        'use_ros2_control', default_value='false', description='Use ros2_control(Gazebo) if true , Use gazebo_plugin if false. gazebo_ros2_control is under development and deprecated')
    declare_world_fname = DeclareLaunchArgument(
        'world_fname', default_value=world, description='absolute path of gazebo world file')
    declare_gui = DeclareLaunchArgument(
        'gui', default_value='true', description='Set to "false" to run headless.')

    world_fname = LaunchConfiguration('world_fname')
    use_sim_time = LaunchConfiguration('use_sim_time', default='true')
    use_ros2_control = LaunchConfiguration('use_ros2_control', default='false')
    gui = LaunchConfiguration('gui', default='true')

    pkg_megarover_samples_ros2 = get_package_share_directory(
        'megarover_samples_ros2')
    launch_file_dir = os.path.join(pkg_megarover_samples_ros2, 'launch')

    pkg_gazebo_ros = get_package_share_directory('gazebo_ros')

    gazebo = IncludeLaunchDescription(
        PythonLaunchDescriptionSource(
            os.path.join(pkg_gazebo_ros, 'launch', 'gazebo.launch.py')
        ),
        launch_arguments={
            'world': world_fname,
            'gui': gui
        }.items(),
    )

    spawn_entity = Node(
        package='gazebo_ros',
        executable='spawn_entity.py',
        name='spawn_entity',
        output='screen',
        arguments=[
                '-entity', 'vmegarover',
                '-x', '0',
                '-y', '0',
                '-z', '1',
                '-topic', 'robot_description',
        ]
    )

    # use diff_drive_controller on ros2_control
    robot_state_publisher_on_ros2_control_launch = IncludeLaunchDescription(
        PythonLaunchDescriptionSource(
            [launch_file_dir, '/robot_state_publisher.launch.py']),
        launch_arguments={'use_sim_time': use_sim_time,
                          'use_ros2_control': use_ros2_control}.items(),
    )

    return LaunchDescription([
        declare_use_ros2_control,
        declare_world_fname,
        declare_gui,
        gazebo,
        spawn_entity,
        robot_state_publisher_on_ros2_control_launch,
    ])
