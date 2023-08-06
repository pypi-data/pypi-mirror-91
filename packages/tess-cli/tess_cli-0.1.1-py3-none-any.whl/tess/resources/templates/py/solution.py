def solve(nums):
    sum = 0
    #@log print(f'<sum> intialized to: {sum}')
    for num in nums:
        """@log
        print(f'Adding num: <{num}>')
        print(f'{num} + {sum} = {num + sum}')
        """
        sum = sum + num
    return sum


n = int(input())
nums = [int(num) for num in input().split()]

print(solve(nums))
