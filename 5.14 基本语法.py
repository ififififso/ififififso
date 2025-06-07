
if __name__ == '__main__':
    print(type(3+4j)) #type类型判断；j是虚数单位，不能随意改变。

    a=123
    print(type(a))



    b=1.25
    print(type(b))


    print(type(True))

    name = 'tjzd'
    name = "tjzd"
    name =""" tjzd
        hahaha"""
    print(name)

    age=18
    name='zhaoxinru'
    print("我的名字：%s,年龄：%d" % (name,age))

    a=123
    print("%010d" %a) #不足的用0补全，超过的还是当前位数

    a=1.23456789 #默认后六位小数，遵循四舍五入原则
    print("%f" %a)

    b=2.123456 #加.之后的小数位就是几位
    print("%.3f" %b)

    name='袁玮泽'
    name2='小狗'
    print(f"我的名字是{name},我是{name2}")

    a=1/1 #注意：使用算术运算符/，商一定是浮点数，且除数不能为0
    print(type(a))

    a=5
    b=2
    print (a//b)
    print(a%b)

    print(7.0//2)
    print(3**2+5/2)

    print(3+2)

    print(1/1)

    a=5
    b=2
    print(a//b)
    print(a%b)

    print(7.0//2)

    num1=2
    num2=3
    num3=num1
    print(num3)
    num4=num2
    total=num3+num4
    print(total)