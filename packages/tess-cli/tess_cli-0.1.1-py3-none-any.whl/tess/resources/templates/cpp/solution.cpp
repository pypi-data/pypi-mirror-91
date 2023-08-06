#include <iostream>

int solve(int nums[], int n)
{
    int sum = 0;
    //@log std::cout << "<sum> initialized to: " << sum << "\n";
    for (size_t i = 0; i < n; ++i) {
        /*@log
        std::cout << "Adding num: <" << nums[i] << ">\n";
        std::cout << nums[i] << " + " << sum << " = " << nums[i] + sum << "\n";
        */
        sum += nums[i];
    }
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