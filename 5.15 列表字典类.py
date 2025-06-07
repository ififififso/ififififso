#列表
my_list = [1, 2, 3, 4, 5]

my_list.extend([6, 7, 8])

my_list.insert(0, 0)  # 在索引0处插入0

# my_list.clear()

last_element = my_list.pop()
third_element = my_list.pop(2)

index_of_3 = my_list.index(3)

count_of_3 = my_list.count(3)

my_list.sort()

my_list.reverse()

my_list_copy = my_list.copy()

print(f"扩展后的列表: {my_list}")
print(f"初始列表的副本: {my_list_copy}")
print(f"移除的最后一个元素: {last_element}, 移除的第三个元素: {third_element}")
print(f"数字3首次出现的位置: {index_of_3}")
print(f"数字3出现的次数: {count_of_3}")



#字典
empty_dict = {}
person = {
    "name": "张三",
    "age": 30,
    "is_student": False
}

person_name = person["name"]
print(person_name)

person["email"] = "zhangsan@example.com"
person["age"] = 31

del person["is_student"]

for key, value in person.items():
    print(f"{key}: {value}")


keys = person.keys()
values = person.values()

print("Keys:", list(keys))
print("Values:", list(values))


#类
class Person:
    def __init__(self, name, age):
        self.name = name
        self.age = age
    def greet(self):
        print(f"你好，我的名字是{self.name}，我今年{self.age}岁了。")
person1 = Person("赵欣茹", 23)
person2 = Person("袁玮泽", 20)

person1.greet()
person2.greet()

print(f"{person1.name}的年龄是{person1.age}岁。")
print(f"{person2.name}的年龄是{person2.age}岁。")

person1.age = 26
print(f"{person1.name}修改后的年龄是{person1.age}岁。")
