# szbdt
"""
Created by ： 刘翔
Email to   ： liuxiangxyd@163.com
Started Date：30 May 2018

一、镀锌、喷涂线槽计算公式
1. 槽身成本=[2*(高+折边)+宽]*长*槽厚*槽吨价*密度/1,000,000
2. 槽盖成本=(宽+2*折边)*长*盖厚*盖吨价*密度/1,000,000
3. 喷涂费 = (高+宽)*4*长*每平米喷涂费/1,000
4. 镀锌每条毛利率=（1-每条成本价/每条销售价）*100%
5. 喷涂每条毛利率=（1-每条喷涂成本价/每条喷涂销售价）*100%
6-11: 上述两个公式修改一下，有可能改变运行误差。
4. 镀锌每条毛利率%=（每条销售价-每条成本价）*100/每条销售价
5. 喷涂每条毛利率%=（每条喷涂销售价-每条喷涂成本价）*100/每条喷涂销售价
注意：取小数点后2位。

常用数据，节省输入时间，方便用户选择，避免错误数据输入：
第一排为：
长: [2],宽:[60,80,100,150,200],高:[40,60,80,100],折边:[10,15,20],密度:[7.85],
第二排为：
    吨价（槽,盖）:[5150,5200,5250,5350,5800,6150],
    厚（槽,盖）:[0.35,0.45,0.6,0.7,0.8,0.9,1.0,1.2],
    每平米喷涂费:[0,5.5,6.5,9,10],

后面的上浮率为
    上浮率%:[0,5,6,7,8,9,10,11,12,13,14,15]

二、图形界面采用内部模块 tkinter 设计样式

三、Python源码采用pyInstaller工具进行编译发布

    pyinstaller -F -w -i myicon.ico

    注意：请在32位的Python环境下运行，兼容性比较好，可以在Windows7/10 32bit/64bit OS下运行。
    64位Python环境下发布的执行文件只能在64位操作系统下运行。

四、执行文件 bdt.exe，图标文件 myicon.ico

五、运行方式
1. 直接点击执行文件 bdt.exe
   这时显示的公司名称为缺省公司名称：深圳市八达通线管桥架有限公司
2. 在DOS命令行下，运行 C:\bdt>bdt 《新公司名》
   这时显示的是《新公司名》
3. 建立快捷键，在快捷键的目标（T）中，增加新公司名，如
   C:bdt\bdt.exe XXXX公司
   以后就点击这个快捷键就可以了。
4. 如果希望改变图标按钮，可以修改myicon.ico的图形，与执行文件放在一个目录下。

TODO：
（1）输入数据格式检查，是否为正确的数字格式？
（2）关键数字修改，是否自动计算结果？

"""
