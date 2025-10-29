cmake_minimum_required(VERSION 3.5)
project(lio_sam)

# ------------------------------------------------------------------------------
# --- Build type ---
# ------------------------------------------------------------------------------
if(NOT CMAKE_BUILD_TYPE AND NOT CMAKE_CONFIGURATION_TYPES)
  set(CMAKE_BUILD_TYPE Release)
endif()

# ------------------------------------------------------------------------------
# --- Dependencies ---
# ------------------------------------------------------------------------------
find_package(ament_cmake REQUIRED)
find_package(rosidl_default_generators REQUIRED)

# ROS 2 core
find_package(rclcpp REQUIRED)
find_package(rclpy REQUIRED)

# Messages
find_package(std_msgs REQUIRED)
find_package(sensor_msgs REQUIRED)
find_package(geometry_msgs REQUIRED)
find_package(nav_msgs REQUIRED)
find_package(visualization_msgs REQUIRED)

# TF / Conversions
find_package(tf2 REQUIRED)
find_package(tf2_geometry_msgs REQUIRED)
find_package(tf2_sensor_msgs REQUIRED)
find_package(tf2_eigen REQUIRED)
find_package(tf2_ros REQUIRED)

# Vision / Point Cloud
find_package(cv_bridge REQUIRED)
set(OpenCV_STATIC ON)
find_package(OpenCV REQUIRED)
find_package(PCL REQUIRED)
find_package(pcl_conversions REQUIRED)
find_package(pcl_msgs REQUIRED)

# SLAM libraries
find_package(GTSAM REQUIRED)
find_package(Eigen3 REQUIRED)
include_directories(${EIGEN3_INCLUDE_DIR})

# Parallelization
find_package(OpenMP REQUIRED)

# ------------------------------------------------------------------------------
# --- Include directories ---
# ------------------------------------------------------------------------------
include_directories(
  include/lio_sam
)

# ------------------------------------------------------------------------------
# --- ROS interfaces ---
# ------------------------------------------------------------------------------
rosidl_generate_interfaces(${PROJECT_NAME}
  "msg/CloudInfo.msg"
  "srv/SaveMap.srv"
  DEPENDENCIES std_msgs sensor_msgs
)

# ------------------------------------------------------------------------------
# --- Executables ---
# ------------------------------------------------------------------------------
add_executable(${PROJECT_NAME}_featureExtraction src/featureExtraction.cpp)
ament_target_dependencies(${PROJECT_NAME}_featureExtraction
  rclcpp rclpy std_msgs sensor_msgs geometry_msgs nav_msgs
  pcl_conversions pcl_msgs visualization_msgs tf2 tf2_ros
  tf2_eigen tf2_sensor_msgs tf2_geometry_msgs OpenCV PCL
)
rosidl_get_typesupport_target(cpp_typesupport_target ${PROJECT_NAME} "rosidl_typesupport_cpp")
target_link_libraries(${PROJECT_NAME}_featureExtraction "${cpp_typesupport_target}")

add_executable(${PROJECT_NAME}_imageProjection src/imageProjection.cpp)
ament_target_dependencies(${PROJECT_NAME}_imageProjection
  rclcpp rclpy std_msgs sensor_msgs geometry_msgs nav_msgs
  pcl_conversions pcl_msgs visualization_msgs tf2 tf2_ros
  tf2_eigen tf2_sensor_msgs tf2_geometry_msgs OpenCV PCL
)
target_link_libraries(${PROJECT_NAME}_imageProjection "${cpp_typesupport_target}")

add_executable(${PROJECT_NAME}_imuPreintegration src/imuPreintegration.cpp)
ament_target_dependencies(${PROJECT_NAME}_imuPreintegration
  rclcpp rclpy std_msgs sensor_msgs geometry_msgs nav_msgs
  pcl_conversions pcl_msgs visualization_msgs tf2 tf2_ros
  tf2_eigen tf2_sensor_msgs tf2_geometry_msgs OpenCV PCL GTSAM Eigen3
)
target_link_libraries(${PROJECT_NAME}_imuPreintegration gtsam "${cpp_typesupport_target}")

add_executable(${PROJECT_NAME}_mapOptimization src/mapOptmization.cpp)
ament_target_dependencies(${PROJECT_NAME}_mapOptimization
  rclcpp rclpy std_msgs sensor_msgs geometry_msgs nav_msgs
  pcl_conversions pcl_msgs visualization_msgs tf2 tf2_ros
  tf2_eigen tf2_sensor_msgs tf2_geometry_msgs OpenCV PCL GTSAM Eigen3
)
if(OpenMP_CXX_FOUND)
  target_link_libraries(${PROJECT_NAME}_mapOptimization gtsam "${cpp_typesupport_target}" OpenMP::OpenMP_CXX)
else()
  target_link_libraries(${PROJECT_NAME}_mapOptimization gtsam "${cpp_typesupport_target}")
endif()

# ------------------------------------------------------------------------------
# --- Installation ---
# ------------------------------------------------------------------------------
# Install launch and config files (so .yaml, .rviz, .launch.py are discoverable)
install(
  DIRECTORY launch config
  DESTINATION share/${PROJECT_NAME}
)

# Install binaries
install(TARGETS
  ${PROJECT_NAME}_featureExtraction
  ${PROJECT_NAME}_imageProjection
  ${PROJECT_NAME}_imuPreintegration
  ${PROJECT_NAME}_mapOptimization
  DESTINATION lib/${PROJECT_NAME}
)

# Install headers
install(DIRECTORY include/ DESTINATION include)
ament_export_include_directories(include)

# ------------------------------------------------------------------------------
# --- Tests ---
# ------------------------------------------------------------------------------
if(BUILD_TESTING)
  find_package(ament_lint_auto REQUIRED)
  ament_lint_auto_find_test_dependencies()
endif()

ament_package()
