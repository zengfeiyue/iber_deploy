1、base_interface_bulid_path是所有interface代码的父目录地址
2、admin_web_bulid_path是管理平台的代码路径
3、kill_bulid是否跳过maven编译
4、dubbo_service是所有interface项目，和项目对应在服务器上对应的路径
5、admin_app key和value是管理平台在服务器上的Tomcat文件夹
6、deploy_test ["iber-sms-service-provider-1.0.0.jar","iber-service-dsdb-1.0.0.jar"] 
	deploy_test代表测试服务器，对应的列表是dubbo_service的key,代表这台服务器需要部署的服务