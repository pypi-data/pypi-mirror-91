import java.util.Arrays;
import java.util.Scanner;

public class Model {
    private static int solve(int[] nums) {
        return Arrays.stream(nums).sum();
    }

    public static void main(String[] args) {
        Scanner scanner = new Scanner(System.in);
        int n = scanner.nextInt();
        int nums[] = new int[n];
        for (int i = 0; i < n; ++i)
            nums[i] = scanner.nextInt();
        System.out.println(solve(nums));
    }
}