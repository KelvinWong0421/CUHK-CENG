//g++ -O3 -o winograd winograd.cpp -larmadillo -lblas -llapack
//./
#include <iostream>
#include <fstream>
#include <armadillo>
#include <math.h>
#include <sys/time.h>

using namespace std;
using namespace arma;

double timestamp();
void report_winograd_statistics(int K, int C, int P, double time);

mat** create_fourd_array(int d1, int d2, int d3, int d4) {
  mat** array = new mat*[d1]();
  for (int i = 0; i < d1; i++) {
    array[i] = new mat[d2]();
    for (int j = 0; j < d2; j++) {
      array[i][j] = mat(d3, d4);
    }
  }
  return array;
}

void free_fourd_array(mat** array, int d1) {
  for (int i = 0; i < d1; i++) {
    delete[] array[i];
  }
  delete[] array;
}

// input: K filters, C channels, H height, W width, array of filters, image reference,
// result reference. Modifies result.
void convolute(int K, int C, int H, int W, cube* filters, cube& image, cube& result) {
  // defining constants and values that follow directly from
  // https://arxiv.org/abs/1509.09308
  int m = 2;
  int r = 3;
  int alpha = m + r - 1;
  int out_H = H - r + 1;
  int out_W = W - r + 1;
  int num_h_tiles = ceil(out_H/m);
  int num_w_tiles = ceil(out_W/m);
  int P = num_h_tiles * num_w_tiles;
  mat G = { {1.0, 0.0, 0.0},
            {0.5, 0.5, 0.5},
            {0.5, -0.5, 0.5},
            {0.0, 0.0, 1.0} };
  mat B = { {1, 0, 0, 0},
            {0, 1, -1, 1},
            {-1, 1, 1, 0},
            {0, 0, 0, -1} };
  mat A = { {1, 0},
            {1, 1},
            {1, -1},
            {0, -1}};

  // a helper lambda function that generates b, the tile index,
  // from the y and x tile coordinates.
  auto gen_b = [num_h_tiles, num_w_tiles](int y, int x) -> int {
    return y * num_w_tiles + x;
  };

  // factoring out malloc'ing before measuring runtime
  mat **U = create_fourd_array(alpha, alpha, K, C);
  mat **V = create_fourd_array(alpha, alpha, C, P);
  mat**M = new mat*[alpha]();
  for (int xi = 0; xi < alpha; xi++) {
    M[xi] = new mat[alpha];
  }
  

  double time = timestamp();

  // Generates U, an alpha x alpha x K x C transformation of the filters.
  for (int k = 0; k < K; k++) {
    for (int c = 0; c < C; c++) {
      // flop: K * C * (4 * 3 * 5) * 2 
      mat u = G * filters[k].slice(c) * G.t();
      for (int xi = 0; xi < alpha; xi++) {
        for (int nu = 0; nu < alpha; nu++) {
          U[xi][nu](k, c) = u(xi, nu);
        }
      }
    }
  }

  // Generates V, an alpha x alpha x C x P transformation of the image.
  for (int c = 0; c < C; c++) {
    mat channel = image.slice(c);
    for (int y = 0; y < num_h_tiles; y++) {
      for (int x = 0; x < num_w_tiles; x++) {
        mat d = channel(span(y * m, y * m + alpha - 1), span(x * m, x * m + alpha - 1));
        // flop: C * P * (4 * 4 * 7) * 2
        mat v = B.t() * d * B;
        int b = gen_b(y, x);
        for (int xi = 0; xi < alpha; xi++) {
          for (int nu = 0; nu < alpha; nu++) {
            V[xi][nu](c, b) = v(xi, nu);
          }
        }
      }
    }
  }
  
  // computes M, an alpha x alpha x K x P matrix
  for (int xi = 0; xi < alpha; xi++) {
    for (int nu = 0; nu < alpha; nu++) {
      // flop: 16 * K * P * (2C - 1) 
      M[xi][nu] = U[xi][nu] * V[xi][nu];
    }
  }

  // computes the final convolution.
  mat m_hold = zeros<mat>(alpha, alpha);
  for (int k = 0; k < K; k++) {
    for (int y = 0; y < num_h_tiles; y++) {
      for (int x = 0; x < num_w_tiles; x++) {
        int b = gen_b(y, x);
        for (int xi = 0; xi < alpha; xi++) {
          for (int nu = 0; nu < alpha; nu++) {
            m_hold(xi, nu) = M[xi][nu](k, b);
          }
        }
        // flop: K * P * (2 * 4 * 7) * 2
        result.slice(k)(span(y*m, (y+1)*m-1), span(x*m, (x+1)*m-1)) = A.t() * m_hold * A;
      }
    }
  }

  time = timestamp() - time;
  report_winograd_statistics(K, C, P, time);

  free_fourd_array(U, alpha);
  free_fourd_array(V, alpha);
  free_fourd_array(M, alpha);
}

double timestamp()
{
  struct timeval tv;
  gettimeofday (&tv, 0);
  return tv.tv_sec + 1e-6*tv.tv_usec;
}

void report_winograd_statistics(int K, int C, int P, double time) {
  int flop = (K * C * (4 * 3 * 5) * 2 +
              C * P * (4 * 4 * 7) * 2 + 
              16 * K * P * (2 * C - 1) + 
              K * P * (2 * 4 * 7) * 2);
  double mflops = flop / (1024.0 * 1024.0 * time);
  // cout << "Floating point operations: " << flop << "\n";
  // cout << "Time Elapsed: " << time << "\n";
  // cout << "MFlop/s: " << mflops << "\n";
}


void test(int K, int C, int H, int W) {
    // Create filters and image with random values for testing purposes
    cube* filters = new cube[K];
    for (int i = 0; i < K; ++i) {
        filters[i] = cube(3, 3, C, fill::randu); // Random initialization
    }
    cube image(H, W, C, fill::randu); // Random initialization
    cube result(H - 2, W - 2, K); // Adjust the size for the output of the convolution

    // Perform the Winograd convolution
    convolute(K, C, H, W, filters, image, result);

    // Clean up dynamic memory
    delete[] filters;
}

int main(int argc, char *argv[]) {
    // Basic error handling for command-line arguments
    if (argc != 5) {
        cerr << "Usage: " << argv[0] << " K C H W" << endl;
        return 1;
    }

    // Parsing command line arguments
    int K = atoi(argv[1]); // Number of filters
    int C = atoi(argv[2]); // Number of channels
    int H = atoi(argv[3]); // Height of the input image
    int W = atoi(argv[4]); // Width of the input image

    // Variables for average time calculation
    double avg_time = 0.0;
    int num_runs = 10; // Number of runs to average over

    for (int i = 0; i < num_runs; ++i) {
        double t = timestamp();

        // Perform the Winograd convolution
        cube* filters = new cube[K];
        test(K, C, H, W);

        double elapsed_time = timestamp() - t;
        avg_time += elapsed_time;
        cout << "Run " << i + 1 << ": Time = " << elapsed_time << " seconds" << endl;
    }

    avg_time /= num_runs;
    cout << "Average Time for " << num_runs << " Calculations: " << avg_time << " seconds" << endl;
    return 0;
}