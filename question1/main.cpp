#include <iostream>
#include <vector>
#include <cmath>
#include <limits>

using namespace std;

vector<double> gaussSeidel(const vector<vector<double>>& A, const vector<double>& b, vector<double> x, double tol = 1e-3, int maxIter = 1000) {
    int n = A.size();
    vector<double> x_old(n);

    cout << "Iteração inicial: ";
    for (auto xi : x) cout << xi << " ";
    cout << endl;

    for (int iter = 0; iter < maxIter; ++iter) {
        x_old = x;

        for (int i = 0; i < n; ++i) {
            double diag = A[i][i];
            double soma = 0.0;
            for (int j = 0; j < n; ++j) {
                if (j != i)
                    soma += A[i][j] * x[j];
            }

            x[i] = (b[i] - soma) / diag;
        }

        double erro = 0.0;
        for (int i = 0; i < n; ++i)
            erro = max(erro, fabs(x[i] - x_old[i]));

        cout << "Iteração " << iter + 1 << ": ";
        for (auto xi : x) cout << xi << " ";
        cout << "| erro = " << erro << endl;

        if (erro < tol) {
            cout << "\nConvergência atingida após " << iter + 1 << " iterações.\n";
            return x;
        }
    }
    return x;
}

int main() {
    vector<vector<double>> A = {
        {10, 4, -0.5, 1, 0},
        {0, -8.1, -2, 1, -3},
        {2, 4, -7, 0, 0},
        {-1, 2, -3, -10, 2},
        {2, 1, -1, 1, -7},
    };

    vector<double> b = {5, -2, 13, 4, 12};
    vector<double> x0 = {1, 1, 0, 1, 0};
    vector<double> x = gaussSeidel(A, b, x0);

    cout << "\nSolução aproximada:\n";
    for (int i = 0; i < x.size(); ++i)
        cout << "x" << i + 1 << " = " << x[i] << endl;
        
    vector<double> residuo(x.size());
    for (int i = 0; i < A.size(); ++i) {
        double soma = 0.0;
        for (int j = 0; j < A[i].size(); ++j)
            soma += A[i][j] * x[j];
            residuo[i] = b[i] - soma;
    }

    cout << "\nVetor resíduo:\n";
    for (int i = 0; i < residuo.size(); ++i)
        cout << "r" << i + 1 << " = " << residuo[i] << endl;

    return 0;
}
