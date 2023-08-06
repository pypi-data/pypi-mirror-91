#include <iostream>
#include <numeric>

int solve(int nums[], int n)
{
    int sum = 0;
    sum = std::accumulate(nums, nums+n, sum);
    return sum;
}

int main()
{
    int n;
    std::cin >> n;
    int nums[n];
    for (size_t i = 0; i < n; ++i)
        std::cin >> nums[i];
    std::cout << solve(nums, n) << "\n";
    return 0;
}