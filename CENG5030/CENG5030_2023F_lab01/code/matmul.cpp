// g++ matmul.cpp -o matmul -std=c++17 -O3 -Wall && ./matmul

#include <sys/time.h>
#include <iostream>
#include <cstring>
#include <cassert>
#include <immintrin.h>


double get_time() {
  struct timeval tv;
  gettimeofday(&tv, nullptr);
  return tv.tv_sec + 1e-6 * tv.tv_usec;
}

constexpr int n = 2048;
int A[n][n];
int B[n][n];
int BT[n][n];
int AT[n][n];
int C[n][n];
int C_groundtruth[n][n];

void init() {
  for (int i = 0; i < n; i++) {
    for (int j = 0; j < n; j++) {
      A[i][j] = rand(); 
      B[i][j] = rand(); 
    } 
  }
  for (int i = 0; i < n; i++) {
    for (int j = 0; j < n; j++) {
      for (int k = 0; k < n; k++) {
        C_groundtruth[i][j] += A[i][k] * B[k][j];
      }
    }
  }
}

void test() {
  for (int i = 0; i < n; i++) {
    for (int j = 0; j < n; j++) {
      assert(C[i][j] == C_groundtruth[i][j]);
    }
  }
}

void matmul() {
  memset(C, 0, sizeof(C));
  for (int i = 0; i < n; i++) {
    for (int j = 0; j < n; j++) {
      for (int k = 0; k < n; k++) {
        C[i][j] += A[i][k] * B[k][j];    
      }   
    }
  }
}

void matmul_tiling() {
  memset(C, 0, sizeof(C));
  int block_size = 64;
  for (int ii = 0; ii < n; ii += block_size) {
    for (int jj = 0; jj < n; jj += block_size) {
      for (int kk = 0; kk < n; kk += block_size) {
        for (int i = ii; i < ii + block_size; ++i) {
          for (int j = jj; j < jj + block_size; ++j) {
            for (int k = kk; k < kk + block_size; ++k) {
              C[i][j] += A[i][k] * B[k][j];
            }
          }
        }
      }
    }
  }
}

void matmul_unrolling() {
  memset(C, 0, sizeof(C));
  for (int i = 0; i < n; ++i) {
    for (int j = 0; j < n; ++j) {
      for (int k = 0; k < n; k += 4) { // Unrolling factor of 4
        C[i][j] += A[i][k] * B[k][j];
        C[i][j] += A[i][k + 1] * B[k + 1][j];
        C[i][j] += A[i][k + 2] * B[k + 2][j];
        C[i][j] += A[i][k + 3] * B[k + 3][j];
      }
    }
  }
}

void matmul_write_caching() {
  memset(C, 0, sizeof(C));
  for (int i = 0; i < n; i++) {
    for (int j = 0; j < n; j++) {
      int temp = 0;
      for (int k = 0; k < n; k++) {
        temp += A[i][k] * B[k][j];
      }
      C[i][j] = temp;
    }
  }
}

void matmul_ikj() {
  memset(C, 0, sizeof(C));
  for (int i = 0; i < n; i++) {
    for (int k = 0; k < n; k++) {
      for (int j = 0; j < n; j++) {
        C[i][j] += A[i][k] * B[k][j];    
      }   
    }
  }
}

void matmul_AT() {
  memset(C, 0, sizeof(C));
  for (int i = 0; i < n; i++) {
    for (int j = 0; j < n; j++) {
      AT[i][j] = A[j][i];
    }
  }
  for (int i = 0; i < n; i++) {
    for (int j = 0; j < n; j++) {
      for (int k = 0; k < n; k++) {
        C[i][j] += AT[k][i] * B[k][j];    
      }   
    }
  }
}

void matmul_BT() {
  memset(C, 0, sizeof(C));
  for (int i = 0; i < n; i++) {
    for (int j = 0; j < n; j++) {
      BT[i][j] = B[j][i];
    }
  }
  for (int i = 0; i < n; i++) {
    for (int j = 0; j < n; j++) {
      for (int k = 0; k < n; k++) {
        C[i][j] += A[i][k] * BT[j][k];    
      }   
    }
  }
}

void matmul_ikj_unrolling() {
  memset(C, 0, sizeof(C));
  for (int i = 0; i < n; ++i) {
    for (int k = 0; k < n; ++k) {
      for (int j = 0; j < n; j += 4) { // Unrolling factor of 4
        C[i][j] += A[i][k] * B[k][j];
        C[i][j + 1] += A[i][k] * B[k][j + 1];
        C[i][j + 2] += A[i][k] * B[k][j + 2];
        C[i][j + 3] += A[i][k] * B[k][j + 3];
      }
    }
  }
}


int main() {
  init();
  float avg_time = 0.0f;
  for (int K = 0; K < 32; K++) {
    auto t = get_time();
    // matmul(); 
    matmul_ikj();
    // matmul_AT();
    // matmul_BT();
    // matmul_tiling();
    // matmul_unrolling();
    
    // matmul_ikj_unrolling();
    // matmul_write_caching();
    // matmul_simd();
    test();
    printf("%f\n", get_time() - t);
    avg_time += get_time() - t;
  }
  printf("Avg Time for Calculation: %f\n", avg_time / 32);
  return 0;
}

