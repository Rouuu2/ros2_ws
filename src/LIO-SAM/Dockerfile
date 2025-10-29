FROM osrf/ros:humble-desktop-full-jammy

RUN apt-get update \
    && apt-get install -y curl \
    && curl -s https://raw.githubusercontent.com/ros/rosdistro/master/ros.asc | apt-key add - \
    && apt-get update \
    && apt install -y python3-colcon-common-extensions \
    && apt-get install -y ros-humble-navigation2 \
    && apt-get install -y ros-humble-robot-localization \
    && apt-get install -y ros-humble-robot-state-publisher \
    && apt install -y ros-humble-perception-pcl \
  	&& apt install -y ros-humble-pcl-msgs \
  	&& apt install -y ros-humble-vision-opencv \
  	&& apt install -y ros-humble-xacro \
    && rm -rf /var/lib/apt/lists/*

RUN apt-get update \
    && apt install -y software-properties-common \
    && add-apt-repository -y ppa:borglab/gtsam-release-4.1 \
    && apt-get update \
    && apt install -y libgtsam-dev libgtsam-unstable-dev \
    && rm -rf /var/lib/apt/lists/*

SHELL ["/bin/bash", "-c"]

RUN mkdir -p ~/ros2_ws/src \
    && cd ~/ros2_ws/src \
    && git clone --branch ros2 https://github.com/TixiaoShan/LIO-SAM.git \
    && cd .. \
    && source /opt/ros/humble/setup.bash \
    && colcon build

RUN echo "source /opt/ros/humble/setup.bash" >> /root/.bashrc \
    && echo "source /root/ros2_ws/install/setup.bash" >> /root/.bashrc

WORKDIR /root/ros2_ws


cmake_minimum_required(VERSION 3.5)
project(lio_sam)

if(NOT CMAKE_BUILD_TYPE AND NOT CMAKE_CONFIGURATION_TYPES)
  set(CMAKE_BUILD_TYPE Release)
endif()


# find dependencies
find_package(ament_cmake REQUIRED)
find_package(rosidl_default_generators REQUIRED)
find_package(rclcpp REQUIRED)
find_package(rclpy REQUIRED)
find_package(cv_bridge REQUIRED)
find_package(std_msgs REQUIRED)
find_package(sensor_msgs REQUIRED)
find_package(geometry_msgs REQUIRED)
find_package(nav_msgs REQUIRED)
find_package(visualization_msgs REQUIRED)
find_package(pcl_conversions REQUIRED)
find_package(pcl_msgs REQUIRED)
find_package(tf2 REQUIRED)
find_package(tf2_geometry_msgs REQUIRED)
find_package(tf2_sensor_msgs REQUIRED)
find_package(tf2_eigen REQUIRED)
find_package(tf2_ros REQUIRED)
set(OpenCV_STATIC ON)
find_package(OpenCV REQUIRED)
find_package(PCL REQUIRED)
find_package(GTSAM REQUIRED)
#find_package(Eigen REQUIRED)
find_package(Eigen3 REQUIRED) #
include_directories(${EIGEN3_INCLUDE_DIR}) #
find_package(OpenMP REQUIRED)

include_directories(
  include/lio_sam
)

rosidl_generate_interfaces(${PROJECT_NAME} "msg/CloudInfo.msg" "srv/SaveMap.srv" DEPENDENCIES std_msgs sensor_msgs)



add_executable(${PROJECT_NAME}_featureExtraction src/featureExtraction.cpp)
ament_target_dependencies(${PROJECT_NAME}_featureExtraction rclcpp rclpy std_msgs sensor_msgs geometry_msgs nav_msgs pcl_conversions pcl_msgs visualization_msgs tf2 tf2_ros tf2_eigen tf2_sensor_msgs tf2_geometry_msgs OpenCV PCL)
rosidl_get_typesupport_target(cpp_typesupport_target ${PROJECT_NAME} "rosidl_typesupport_cpp")
target_link_libraries(${PROJECT_NAME}_featureExtraction "${cpp_typesupport_target}") 

add_executable(${PROJECT_NAME}_imageProjection src/imageProjection.cpp)
ament_target_dependencies(${PROJECT_NAME}_imageProjection rclcpp rclpy std_msgs sensor_msgs geometry_msgs nav_msgs pcl_conversions pcl_msgs visualization_msgs tf2 tf2_ros tf2_eigen tf2_sensor_msgs tf2_geometry_msgs OpenCV PCL)
target_link_libraries(${PROJECT_NAME}_imageProjection "${cpp_typesupport_target}") 

add_executable(${PROJECT_NAME}_imuPreintegration src/imuPreintegration.cpp)
ament_target_dependencies(${PROJECT_NAME}_imuPreintegration rclcpp rclpy std_msgs sensor_msgs geometry_msgs nav_msgs pcl_conversions pcl_msgs visualization_msgs tf2 tf2_ros tf2_eigen tf2_sensor_msgs tf2_geometry_msgs OpenCV PCL GTSAM Eigen)
target_link_libraries(${PROJECT_NAME}_imuPreintegration gtsam "${cpp_typesupport_target}")

add_executable(${PROJECT_NAME}_mapOptimization src/mapOptmization.cpp)
ament_target_dependencies(${PROJECT_NAME}_mapOptimization rclcpp rclpy std_msgs sensor_msgs geometry_msgs nav_msgs pcl_conversions pcl_msgs visualization_msgs tf2 tf2_ros tf2_eigen tf2_sensor_msgs tf2_geometry_msgs OpenCV PCL GTSAM)
if (OpenMP_CXX_FOUND)
  target_link_libraries(${PROJECT_NAME}_mapOptimization gtsam "${cpp_typesupport_target}" OpenMP::OpenMP_CXX)
else()
  target_link_libraries(${PROJECT_NAME}_mapOptimization gtsam "${cpp_typesupport_target}")
endif()


install(
  DIRECTORY launch
  DESTINATION share/${PROJECT_NAME}/
)

install(
  DIRECTORY config
  DESTINATION share/${PROJECT_NAME}/
)

install(
  TARGETS ${PROJECT_NAME}_imageProjection
  DESTINATION lib/${PROJECT_NAME}
)

install(
  TARGETS ${PROJECT_NAME}_imuPreintegration
  DESTINATION lib/${PROJECT_NAME}
)

install(
  TARGETS ${PROJECT_NAME}_featureExtraction
  DESTINATION lib/${PROJECT_NAME}
)

install(
  TARGETS ${PROJECT_NAME}_mapOptimization
  DESTINATION lib/${PROJECT_NAME}
)

install(
  DIRECTORY "include/"
  DESTINATION include
)

ament_export_include_directories(include)

if(BUILD_TESTING)
  find_package(ament_lint_auto REQUIRED)
  # the following line skips the linter which checks for copyrights
  # uncomment the line when a copyright and license is not present in all source files
  #set(ament_cmake_copyright_FOUND TRUE)
  # the following line skips cpplint (only works in a git repo)
  # uncomment the line when this package is not in a git repo
  #set(ament_cmake_cpplint_FOUND TRUE)
  ament_lint_auto_find_test_dependencies()
endif()

ament_package()


