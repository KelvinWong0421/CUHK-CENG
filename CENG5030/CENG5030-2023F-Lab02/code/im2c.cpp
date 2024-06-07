//g++ -O3 -o im2c im2c.cpp

#include <iostream>
#include <vector>
#include <cassert>
#include <sys/time.h>

using namespace std;

// Assumes input image is a 3D vector with dimensions [channels][height][width]
// Output matrix has dimensions [kernel_height * kernel_width * channels][output_height * output_width]
vector<vector<float>> img2col(const vector<vector<vector<float>>>& input, int kernel_size, int stride, int padding) {
    int channels = input.size();
    int height = input[0].size();
    int width = input[0][0].size();
    
    // Calculate output dimensions
    int output_height = (height - kernel_size + 2 * padding) / stride + 1;
    int output_width = (width - kernel_size + 2 * padding) / stride + 1;
    
    // Initialize the output matrix with zeros
    vector<vector<float>> output((kernel_size * kernel_size * channels), vector<float>(output_height * output_width, 0));

    // Start filling the output matrix
    for (int c = 0; c < channels; ++c) {  // 'c' is the correct variable name for channels in the loop
        for (int kernel_row = 0; kernel_row < kernel_size; ++kernel_row) {
            for (int kernel_col = 0; kernel_col < kernel_size; ++kernel_col) {
                int row_base = c * kernel_size * kernel_size + kernel_row * kernel_size + kernel_col;
                for (int output_row = 0; output_row < output_height; ++output_row) {
                    for (int output_col = 0; output_col < output_width; ++output_col) {
                        int input_row = output_row * stride + kernel_row;
                        int input_col = output_col * stride + kernel_col;
                        if (input_row < height && input_col < width) {
                            output[row_base][output_row * output_width + output_col] =
                                input[c][input_row][input_col];
                        }  // Padding with zeros is implicit due to initialization of 'output'
                    }
                }
            }
        }
    }

    return output;
}


void print_matrix(const vector<vector<float>>& mat) {
    for (const auto& row : mat) {
        for (float val : row) {
            cout << val << " ";
        }
        cout << endl;
    }
}

// int main() {
//     // Create a test input (3 channels, 4x4 image)
//     vector<vector<vector<float>>> test_input = {
//         {
//             {1, 2, 3, 4},
//             {5, 6, 7, 8},
//             {9, 10, 11, 12},
//             {13, 14, 15, 16}
//         },
//         {
//             {17, 18, 19, 20},
//             {21, 22, 23, 24},
//             {25, 26, 27, 28},
//             {29, 30, 31, 32}
//         },
//         {
//             {33, 34, 35, 36},
//             {37, 38, 39, 40},
//             {41, 42, 43, 44},
//             {45, 46, 47, 48}
//         }
//     };

//     // Apply img2col on the test input
//     vector<vector<float>> output_col_matrix = img2col(test_input, 3, 1, 0);

//     // Print output for visual checking
//     cout << "Output (img2col) matrix:" << endl;
//     print_matrix(output_col_matrix);

//     // Expected output dimensions for a 3x3 kernel with stride 1 and no padding on a 4x4 image
//     // should be 3 * 3 * 3 (channels) rows and 2 * 2 (output height * output width) columns
//     // Since the actual logic for generating expected_output isn't provided,
//     // you need to calculate the expected output yourself based on the input dimensions and parameters.
    
//     // Assert to automatically verify the output (after you compute the expected_output)
//     // assert(output_col_matrix == expected_output); // Uncomment this after you fill `expected_output`

//     // The rest of the code...
    
//     return 0;
// }
 

double get_time() {
  struct timeval tv;
  gettimeofday(&tv, nullptr);
  return tv.tv_sec + 1e-6 * tv.tv_usec;
}


void test() {
    // Define your test parameters
    const int height = 56, width = 56, in_channels = 3, kernel_size = 3, stride = 1, padding = 0;
    
    // Create a test input with 1 batch x in_channels x height x width filled with 1.0 for simplicity
    vector<vector<vector<float>>> test_input(in_channels, vector<vector<float>>(height, vector<float>(width, 1.0)));
    
    // Run img2col on the test input
    vector<vector<float>> output_col_matrix = img2col(test_input, kernel_size, stride, padding);
    
    // Normally, you'd check the correctness of the output here or use it for further calculations
    // For timing tests, we're only interested in the performance aspect
}

int main() {

  float avg_time = 0.0f;
  for (int K = 0; K < 32; K++) {
    auto t = get_time();

    test();
    printf("%f\n", get_time() - t);
    avg_time += get_time() - t;
  }
  printf("Avg Time for Calculation: %f\n", avg_time / 32);
  return 0;
}
