
## 由来
并行运行Appium docker是一种并行执行移动自动化测试的方式，为了简化环境的搭建，本人采用了Vagrant + virtualbox + ubuntu + docker 的方式一键式构建并行运行Appium脚本的基础环境
## 环境准备
Mac 或 Windows, 安装对应版本的一下软件：
-  [virtualBox](https://www.virtualbox.org/) (5.2.2)
-  [virtualBox Enxtension Pack](https://www.virtualbox.org/wiki/Downloads) (5.2.2)
-  [vagrant](https://www.vagrantup.com/downloads.html) (2.0.1)

## 安装
clone 脚本
`git clone https://github.com/shane51/vagrantfile-template.git`

进入 appiumParallel 目录
`cd vagrantfile-template/appiumParallel`

执行 vagrant up
`vagrant up`

等待vagrant下载ubuntu 16.0.4 LTS 版本，并安装相应的docker。

## 进入ubuntu
在 appiumParallel 目录下执行
`vagrant ssh`
系统会弹出输入Password提示,输入密码 `ubuntu`，即可进入ubuntu。

