# coding=utf-8
import json
from fabric.api import *
import os
import sys
import time

env.user = 'root'
env.passwords = {
    'root@ip': 'pwd'
}

env.roledefs = {
    'iber_test': ['root@ip:22']
}
# 生成配置
try:
    with open("param.json", 'r') as load_f:
        param = json.load(load_f)
    deploy_admin_path = param['admin_app']
except Exception as e:
    print(e,'json 读取错误')
    os.system("pause")


@roles('iber_test')
def deploy_test():
    deploy_list = param['deploy_test']
    if not param["kill_bulid"]:
        bulid_project(deploy_list)
    deploy_test_kill_service_pid(deploy_list)
    deploy_test_upload_file(deploy_list)
    deploy_test_run_jar(deploy_list)


def bulid_project(bulidProject):
    pwd = os.getcwd()
    for project in bulidProject:
        if project in param["dubbo_service"]:
            if '.jar' in project:
                # maven package
                os.chdir(param["base_interface_bulid_path"] + project[:-10])
                bulid_result = os.popen("mvn package -Dmaven.test.skip=true")
                if 'BUILD FAILED' in bulid_result.read():
                    print("项目构建失败！！")
                    sys.exit(0)
                os.chdir("target")
                os.system("copy " + project + " " + pwd)
            else:
                # maven interface war
                os.chdir(param["base_interface_bulid_path"] + "iber-service-interface")
                bulid_result = os.popen("mvn package -Dmaven.test.skip=true")
                if 'BUILD FAILED' in bulid_result.read():
                    print("项目构建失败！！")
                    sys.exit(0)
                os.chdir("target")
                os.system("copy iber-service-interface-1.0.0.war " + pwd)
        else:
            os.chdir(param["admin_web_bulid_path"])
            bulid_result = os.popen("mvn package -Dmaven.test.skip=true")
            if 'BUILD FAILED' in bulid_result.read():
                print("项目构建失败！！")
                sys.exit(0)
            os.chdir("target")
            os.system("copy iber-portal.war " + pwd)
    os.chdir(pwd)


# kill servic进程
def deploy_test_kill_service_pid(deploy_list):
    for project in deploy_list:
        pids = run("ps -ef|grep " + project + " | grep -v grep | awk '{print $2}'")
        pid_list = pids.split('\r\n')
        for i in pid_list:
            run('kill -9 %s' % i)  # 杀掉运行服务进程


# 上传文件
def deploy_test_upload_file(deploy_list):
    deploy_path = param['dubbo_service']
    for project in deploy_list:
        if project in param["dubbo_service"]:
            if '.jar' in project:
                # upload dubbo jar
                put(project, deploy_path[project])
            else:
                # upload interface war
                put('iber-service-interface-1.0.0.war', deploy_path[project] + "/webapps/ROOT.war")
                run("rm -rf " + deploy_path[project] + "/webapps/ROOT")

        else:
            # web-app admin upload to service
            put('iber-portal.war', deploy_admin_path[project] + "/webapps/ROOT.war")
            run("rm -rf " + deploy_admin_path[project] + "/webapps/ROOT")


# 启动线程
def deploy_test_run_jar(deploy_list):
    deploy_path = param['dubbo_service']
    for project in deploy_list:
        if project in param["dubbo_service"]:
            if '.jar' in project:
                # start dubbo service
                run("set -m;sh " + deploy_path[project][:-4] + "/bin/start.sh")
            else:
                # upload interface war
                run("set -m;sh " + deploy_path[project] + "/bin/startup.sh")
        else:
            # web-app admin upload to service
            run("set -m;sh " + deploy_admin_path[project] + "/bin/startup.sh")


if __name__ == '__main__':
    try:
        execute(deploy_test)
        os.system("pause")
    except Exception as e:
        print(e)
        os.system("pause")
