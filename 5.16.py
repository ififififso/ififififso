#for循环、while循环
numbers = [1, 2, 3, 4, 5, 6, 7, 8, 9, 10]

sum_of_evens = 0

for number in numbers:
    if number % 2 == 0:
        print(f"{number} 是偶数")
        sum_of_evens += number  # 如果是偶数，则将其加到累加器中
    else:
        print(f"{number} 是奇数")

print(f"所有偶数的和为: {sum_of_evens}")

counter = 0

while counter < 5:
    print(f"计数器的值为: {counter}")
    counter += 1
