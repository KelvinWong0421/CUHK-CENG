
// g++ strassen.cpp -o strassen -std=c++17 -O3 -Wall && ./strassen

#include <stdio.h>
#include <stdlib.h>
#include <math.h>
#include <iostream>
#include <sys/time.h>

#define SIZE 1024

using namespace std;

double get_time() {
  struct timeval tv;
  gettimeofday(&tv, nullptr);
  return tv.tv_sec + 1e-6 * tv.tv_usec;
}

int** AllocateMatrix(int size);
void FreeMatrix(int** matrix, int size);

void ReadMatrix(int**,int);
void WriteMatrix(int**,int);

void MatrixAdd(int **A, int **B, int **Result, int N);
void MatrixSubtrac(int **A, int **B, int **Result, int N);

void StrassenAlgorithm(int **A, int **B, int **C, int N);




// Function to allocate memory for a matrix
int** AllocateMatrix(int size) {
    int** matrix = new int*[size];
    for (int i = 0; i < size; ++i) {
        matrix[i] = new int[size];
    }
    return matrix;
}

// Function to free the allocated memory for a matrix
void FreeMatrix(int** matrix, int size) {
    for (int i = 0; i < size; ++i) {
        delete[] matrix[i];
    }
    delete[] matrix;
}


/* For taking input from standard input(keyboard)*/
void ReadMatrix(int** A,int N)
{
    int i,j;

    for(i=0; i<N; i++)
    {
        for(j=0; j<N; j++)
        {
            // scanf("%lf", &A[i][j]);
            A[i][j] = rand()% 10;
        }
    }
}

/*For printing the matrix in standard output(console)*/
void WriteMatrix(int** A, int N)
{
    int i, j;

    for(i=0; i<N; i++)
    {
        for(j=0; j<N; j++)
        {
            printf("%d \t", A[i][j]);
        }
        printf("\n");
    }
}

/*This function will add two square matrix*/
void MatrixAdd(int** A, int** B, int** Result, int N)
{
    int i, j;

    for(i=0; i< N; i++)
    {
        for(j=0; j<N; j++)
        {
            Result[i][j] = A[i][j] + B[i][j];
        }
    }

}

/*This function will subtract one  square matrix from another*/
void MatrixSubtrac(int** A, int** B, int** Result, int N)
{
    int i, j;

    for(i=0; i< N; i++)
    {
        for(j=0; j<N; j++)
        {
            Result[i][j] = A[i][j] - B[i][j];
        }
    }
}


/*This is the strassen algorithm. (Divide and Conqure)*/
void StrassenAlgorithm(int** A, int** B, int** C, int N)
{
    // trivial case: when the matrice is 1 X 1:
    if(N == 1)
    {
        C[0][0] = A[0][0] * B[0][0];
        return;
    }

    // other cases are treated here:
    else
    {
        int Divide  = (int)(N/2);
        int newSize = Divide;


        int **A11 = AllocateMatrix(newSize);
        int **A12 = AllocateMatrix(newSize);
        int **A21 = AllocateMatrix(newSize);
        int **A22 = AllocateMatrix(newSize);
        int **B11 = AllocateMatrix(newSize);
        int **B12 = AllocateMatrix(newSize);
        int **B21 = AllocateMatrix(newSize);
        int **B22 = AllocateMatrix(newSize);
        int **C11 = AllocateMatrix(newSize);
        int **C12 = AllocateMatrix(newSize);
        int **C21 = AllocateMatrix(newSize);
        int **C22 = AllocateMatrix(newSize);
        int **P1 = AllocateMatrix(newSize);
        int **P2 = AllocateMatrix(newSize);
        int **P3 = AllocateMatrix(newSize);
        int **P4 = AllocateMatrix(newSize);
        int **P5 = AllocateMatrix(newSize);
        int **P6 = AllocateMatrix(newSize);
        int **P7 = AllocateMatrix(newSize);
        int **AResult = AllocateMatrix(newSize);
        int **BResult = AllocateMatrix(newSize);


        int i, j;

        //dividing the matrices in 4 sub-matrices:
        for (i = 0; i < Divide; i++)
        {
            for (j = 0; j < Divide; j++)
            {
                A11[i][j] = A[i][j];
                A12[i][j] = A[i][j + Divide];
                A21[i][j] = A[i + Divide][j];
                A22[i][j] = A[i + Divide][j + Divide];

                B11[i][j] = B[i][j];
                B12[i][j] = B[i][j + Divide];
                B21[i][j] = B[i + Divide][j];
                B22[i][j] = B[i + Divide][j + Divide];
            }
        }

        // Calculating p1 to p7:
        /*For details -- Introduction to Algorithms 3rd Edition by CLRS*/

        MatrixAdd(A11, A22, AResult, Divide);   // a11 + a22
        MatrixAdd(B11, B22, BResult, Divide);   // b11 + b22
        StrassenAlgorithm(AResult, BResult, P1, Divide);  // p1 = (a11+a22) * (b11+b22)

        MatrixAdd(A21, A22, AResult, Divide);   // a21 + a22
        StrassenAlgorithm(AResult, B11, P2, Divide); // p2 = (a21+a22) * (b11)

        MatrixSubtrac(B12, B22, BResult, Divide); // b12 - b22
        StrassenAlgorithm(A11, BResult, P3, Divide); // p3 = (a11) * (b12 - b22)

        MatrixSubtrac(B21, B11, BResult, Divide); // b21 - b11
        StrassenAlgorithm(A22, BResult, P4, Divide); // p4 = (a22) * (b21 - b11)

        MatrixAdd(A11, A12, AResult, Divide); // a11 + a12
        StrassenAlgorithm(AResult, B22, P5, Divide); // p5 = (a11+a12) * (b22)

        MatrixSubtrac(A21, A11, AResult, Divide); // a21 - a11
        MatrixAdd(B11, B12, BResult, Divide); // b11 + b12
        StrassenAlgorithm(AResult, BResult, P6, Divide); // p6 = (a21-a11) * (b11+b12)

        MatrixSubtrac(A12, A22, AResult, Divide); // a12 - a22
        MatrixAdd(B21, B22, BResult, Divide); // b21 + b22
        StrassenAlgorithm(AResult, BResult, P7, Divide); // p7 = (a12-a22) * (b21+b22)

        // calculating c21, c21, c11 e c22:

        MatrixAdd(P3, P5, C12, Divide); // c12 = p3 + p5
        MatrixAdd(P2, P4, C21, Divide); // c21 = p2 + p4

        MatrixAdd(P1, P4, AResult, Divide); // p1 + p4
        MatrixAdd(AResult, P7, BResult, Divide); // p1 + p4 + p7
        MatrixSubtrac(BResult, P5, C11, Divide); // c11 = p1 + p4 - p5 + p7

        MatrixAdd(P1, P3, AResult, Divide); // p1 + p3
        MatrixAdd(AResult, P6, BResult, Divide); // p1 + p3 + p6
        MatrixSubtrac(BResult, P2, C22, Divide); // c22 = p1 + p3 - p2 + p6


        // Grouping the results obtained in a single matrice:

        for (i = 0; i < Divide ; i++)
        {
            for (j = 0 ; j < Divide ; j++)
            {
                C[i][j] = C11[i][j];
                C[i][j + Divide] = C12[i][j];
                C[i + Divide][j] = C21[i][j];
                C[i + Divide][j + Divide] = C22[i][j];
            }
        }

        // Free all allocated matrices
        FreeMatrix(A11, newSize);
        FreeMatrix(A12, newSize);
        FreeMatrix(A21, newSize);
        FreeMatrix(A22, newSize);
        FreeMatrix(B11, newSize);
        FreeMatrix(B12, newSize);
        FreeMatrix(B21, newSize);
        FreeMatrix(B22, newSize);
        FreeMatrix(C11, newSize);
        FreeMatrix(C12, newSize);
        FreeMatrix(C21, newSize);
        FreeMatrix(C22, newSize);
        FreeMatrix(P1, newSize);
        FreeMatrix(P2, newSize);
        FreeMatrix(P3, newSize);
        FreeMatrix(P4, newSize);
        FreeMatrix(P5, newSize);
        FreeMatrix(P6, newSize);
        FreeMatrix(P7, newSize);
        FreeMatrix(AResult, newSize);
        FreeMatrix(BResult, newSize);
    }

}

/*The main function*/
int main()
{
    
    
    int i,j;
    int N,M,Count = 0;

    N = SIZE;


    int** A = AllocateMatrix(N);
    int** B = AllocateMatrix(N);
    int** C = AllocateMatrix(N);

    M = N;
    float avg_time = 0.0f;

    // printf("Matrix A:\n");
    ReadMatrix(A,M);
    // printf("Matrix B:\n");
    ReadMatrix(B,M);

    if(M > 1)
    {

        while(M>=2)
        {
            M/=2;
            Count++;
        }

        M = N;

        if(M != (pow(2.0,Count)))
        {
            N = pow(2.0,Count+1);

            for(i=0; i<N; i++)
            {
                for(j=0; j<N; j++)
                {
                    if((i>=M) || (j>=M))
                    {
                        A[i][j] = 0.0;
                        B[i][j] = 0.0;
                    }
                }
            }
        }
    }

    for (int K = 0; K < 32; K++) {
        auto t = get_time();

        StrassenAlgorithm(A,B,C,N); // StrassenAlgorithm called here

        printf("%f\n", get_time() - t);
        avg_time += get_time() - t;
    }
    printf("Avg Time for Calculation: %f\n", avg_time / 32);

    FreeMatrix(A, N); // After you are done using matrix A
    FreeMatrix(B, N); // After you are done using matrix B
    FreeMatrix(C, N); // After you are done using matrix C

    return 0;

}
