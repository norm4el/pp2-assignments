from functools import reduce

nums = [1, 2, 3, 4, 5]
squares = list(map(lambda x: x * x, nums))
print("map:", squares)

even_nums = list(filter(lambda x: x % 2 == 0, nums))
print("filter:", even_nums)

total = reduce(lambda x, y: x + y, nums)
print("reduce:", total)