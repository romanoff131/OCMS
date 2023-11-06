#include <stdio.h>
#include <math.h>

#define N 8

void correlation(int a[], int b[], int c[]) {
    int sum_a = 0, sum_b = 0, sum_c = 0;
    int sum_ab = 0, sum_ac = 0, sum_bc = 0;
    int sum_a_squared = 0, sum_b_squared = 0, sum_c_squared = 0;

    // Вычисление сумм элементов массивов a, b и c
    for (int i = 0; i < N; i++) {
        sum_a += a[i];
        sum_b += b[i];
        sum_c += c[i];
    }

    // Вычисление сумм произведений элементов массивов a и b, a и c, b и c
    for (int i = 0; i < N; i++) {
        sum_ab += a[i] * b[i];
        sum_ac += a[i] * c[i];
        sum_bc += b[i] * c[i];
    }

    // Вычисление сумм квадратов элементов массивов a, b и c
    for (int i = 0; i < N; i++) {
        sum_a_squared += a[i] * a[i];
        sum_b_squared += b[i] * b[i];
        sum_c_squared += c[i] * c[i];
    }

    // Вычисление корреляции
    double correlation_ab = (N * sum_ab - sum_a * sum_b) / sqrtf((N * sum_a_squared - sum_a * sum_a) * (N * sum_b_squared - sum_b * sum_b));
    double correlation_ac = (N * sum_ac - sum_a * sum_c) / sqrtf((N * sum_a_squared - sum_a * sum_a) * (N * sum_c_squared - sum_c * sum_c));
    double correlation_bc = (N * sum_bc - sum_b * sum_c) / sqrtf((N * sum_b_squared - sum_b * sum_b) * (N * sum_c_squared - sum_c * sum_c));

    // Вывод результатов
    printf("Correlation between a and b: %.3f\n", correlation_ab);
    printf("Correlation between a and c: %.3f\n", correlation_ac);
    printf("Correlation between b and c: %.3f\n", correlation_bc);

    printf("Корреляция между a, b и с\n");
    printf("  | a | b | c |\n");
    printf(" a| - |%f |%f |\n",correlation_ab, correlation_ac);
    printf(" b|%f | - |%f|\n",correlation_ab,correlation_bc);
    printf(" c|%f |%f| - |\n",correlation_ac,correlation_bc);
}

double mean(int arr[], int length) {
    int sum = 0;
    for (int i = 0; i < length; i++) {
        sum += arr[i];
    }
    return (double)sum / length;
}

double var(int arr[], int length) {
    double arr_mean = mean(arr, length);
    double sum = 0;
    for (int i = 0; i < length; i++) {
        sum += pow(arr[i] - arr_mean, 2);
    }
    return sum / length;
}

double norm_corr(int a[], int b[], int c[], int length) {
    double a_mean = mean(a, length);
    double b_mean = mean(b, length);
    double c_mean = mean(c, length);

    double a_var = var(a, length);
    double b_var = var(b, length);
    double c_var = var(c, length);

    double numerator = 0;
    double denominator_1 = 0;
    double denominator_2 = 0;

    for (int i = 0; i < length; i++) {
        numerator += (a[i] - a_mean) * (b[i] - b_mean) * (c[i] - c_mean);
        denominator_1 += pow(a[i] - a_mean, 2) * pow(b[i] - b_mean, 2);
        denominator_2 += pow(a[i] - a_mean, 2) * pow(c[i] - c_mean, 2);
    }

    return numerator / (sqrt(denominator_1 * denominator_2));
}


int main() {

    int a[] ={5,2,8,-2,-4,-4,1,3};
    int b[] = {4,1,7,0,-6,-5,2,5};
    int c[] = {-6,-1,-3,-9,2,-8,4,1};
    int length = sizeof(a) / sizeof(a[0]);
    correlation(a, b, c);
    double correlation = norm_corr(a, b, c, length);
    printf("Normalized correlation: %f\n", correlation);


}
