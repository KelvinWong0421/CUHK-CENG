//g++ -o sparse sparse.cpp -lcnpy
//./sparse
#include <bits/stdc++.h>
#include <vector>
#include <set>
#include <iostream>
#include <sys/time.h>
#include "cnpy.h"

#define row 64
#define col 4096

#define KH 3
#define KW 3

#define OUTC 64 
#define result_w (col - KW + 1)
#define result_h (row - KW + 1)

using namespace std;

typedef pair<int, int> pairs;

typedef struct rulebookEntry
{
    pairs offset;
    vector<pairs> in_out;
} bookE;

double timestamp(){
  struct timeval tv;
  gettimeofday(&tv, 0);
  return tv.tv_sec + 1e-6 * tv.tv_usec;
}

int ***createFilterSample(); // the outer one is n output channel, the second is locY, last is locX (from left to right, top to down)
int ***initResultSpace();     // the outer one is output channel, the second one is the locY, the third is the locX
void clearData(int ***kernal, int ***result);
void displayResult(int ***result);

void initRulebook(vector<bookE> &book)
{
    for (int i = -1; i < 2; i++)
    {
        for (int j = -1; j < 2; j++)
        {
            bookE bkE;
            bkE.offset = make_pair(i, j);
            bkE.in_out = vector<pairs>();
            book.push_back(bkE);
        }
    }
}

int main(){
    vector<pairs> h_in;
    vector<pairs> h_out;

    vector<bookE> rulebook;

    initRulebook(rulebook); // for each offset
    
    /*
    for(int i = 0; i < rulebook.size(); i++){
    pairs y = rulebook[i].offset;
    	cout << y.first << " " << y.second << endl; 
    }*/

    cnpy::NpyArray arr = cnpy::npy_load("pointcloud.npy");
    double *loaded_dataD = arr.data<double>();

    int* loaded_data = (int*)malloc(col*row * sizeof(int));  //convert the data back to int
    for (int i = 0; i < row * col; i++) {
       loaded_data[i] = int(loaded_dataD[i]);
        //if( i % col == 0) cout << endl;
        //cout << loaded_data[i] ;
    }

    // form h_out
    for (int i = 0; i <= (row - KH); i++)
    {
        for (int j = 0; j <= (col - KW); j++)
        {
            if (loaded_data[i * col + j] || loaded_data[i * col + j + 1] || loaded_data[i * col + j + 2] ||
                loaded_data[(i + 1) * col + j] || loaded_data[(i + 1) * col + j + 1] || loaded_data[(i + 1) * col + j + 2] ||
                loaded_data[(i + 2) * col + j] || loaded_data[(i + 2) * col + j + 1] || loaded_data[(i + 2) * col + j + 2])
            {
                pairs x = make_pair(j, i);
                h_out.push_back(x);
                //cout << x.first << " " << x.second << endl;

            }
        }
    }

    //form  h_in and rulebook
    for (int i = 0; i < row; i++){

        // check which offset can be used
        bool top = false, middleH = false, bottom = false;

        if ((i - 2) >= 0)               bottom = true;
        if (i >= 1 && i <= (row - 2))   middleH = true;
        if ((i + 2) < row)              top = true;

        for (int j =0; j < col ; j++ ){

            if(loaded_data[i*col + j] ){ //not zero
                pairs x = make_pair(j, i);
                h_in.push_back(x);
                //cout << x.first << " " << x.second << endl;

                vector<pairs>::iterator it;

                //right 
                if((j-2) >= 0){ 

                    if(bottom){
                        // 1,1
                        it = find(h_out.begin(), h_out.end(), make_pair(j - 2, i - 2));
                        if (it != h_out.end()) {
                            pairs y = make_pair(h_in.size() - 1, it - h_out.begin());
                            rulebook[8].in_out.push_back(y);
                            //cout << "8 " << y.first << " " << y.second<< endl;
                        }
                    }

                    if (middleH){
                        // 1,0
                        it = find(h_out.begin(), h_out.end(), make_pair(j - 2, i - 1));
                        if (it != h_out.end()) {
                            pairs y = make_pair(h_in.size() - 1, it - h_out.begin());
                            rulebook[5].in_out.push_back(y);
                            //cout << "5 " << y.first << " " << y.second<< endl;
                        }
                    }

                    if (top) {
                        // 1, -1
                        it = find(h_out.begin(), h_out.end(), make_pair(j - 2, i));
                        if (it != h_out.end())
                        {
                            pairs y = make_pair(h_in.size() - 1, it - h_out.begin());
                            rulebook[2].in_out.push_back(y);
                            //cout << "2 " << y.first << " " << y.second<< endl;
                        }
                    }

                }

                // middle Col
                if (j >= 1 && j <= (col - 2)){
                    
                    if (bottom) {
                        // 0,1
                        it = find(h_out.begin(), h_out.end(), make_pair(j - 1, i - 2));
                        if (it != h_out.end())
                        {
                            pairs y = make_pair(h_in.size() - 1, it - h_out.begin());
                            rulebook[7].in_out.push_back(y);
                            //cout << "7 " << y.first << " " << y.second<< endl;
                        }
                    }

                    if (middleH) {
                        // 0,0
                        it = find(h_out.begin(), h_out.end(), make_pair(j - 1, i - 1));
                        if (it != h_out.end())
                        {
                            pairs y = make_pair(h_in.size() - 1, it - h_out.begin());
                            rulebook[4].in_out.push_back(y);
                            //cout << "4 " << y.first << " " << y.second<< endl;
                        }
                    }

                    if (top)  {
                        // 0,-1
                        it = find(h_out.begin(), h_out.end(), make_pair(j - 1, i));
                        if (it != h_out.end())
                        {
                            pairs y = make_pair(h_in.size() - 1, it - h_out.begin());
                            rulebook[1].in_out.push_back(y);
                            //cout << "1 " << y.first << " " << y.second<< endl;
                        }
                    }
                }

                //left
                if ((j + 2) < col){

                    if (bottom){
                        //-1,1
                        it = find(h_out.begin(), h_out.end(), make_pair(j, i - 2));
                        if (it != h_out.end())
                        {
                            pairs y = make_pair(h_in.size() - 1, it - h_out.begin());
                            rulebook[6].in_out.push_back(y);
                            //cout << "6 " << y.first << " " << y.second<< endl;
                        }
                    }

                    if (middleH){
                        //-1,0
                        it = find(h_out.begin(), h_out.end(), make_pair(j, i - 1));
                        if (it != h_out.end())
                        {
                            pairs y = make_pair(h_in.size() - 1, it - h_out.begin());
                            rulebook[3].in_out.push_back(y);
                            //cout << "3 " << y.first << " " << y.second << endl;
                        }
                    }

                    if (top) {
                        //-1,-1
                        it = find(h_out.begin(), h_out.end(), make_pair(j, i));
                        if (it != h_out.end())
                        {
                            pairs y = make_pair(h_in.size() - 1, it - h_out.begin());
                            rulebook[0].in_out.push_back(y);
                            //cout << "0 " << y.first << " " << y.second << endl;
                        }
                    }


                }

            }

        }
    }


    //init filter / result space
    int*** filter = createFilterSample();
    int*** result = initResultSpace();

    double time = timestamp();

    //process
    for(int i = 0; i < rulebook.size(); i++){

        int locX = rulebook[i].offset.first + 1, locY = rulebook[i].offset.second + 1;

        for(int j = 0; j < rulebook[i].in_out.size() ; j ++) {
            pairs r = h_out[rulebook[i].in_out[j].second];
            for(int k =0; k <OUTC; k ++){
                result[k][r.second][r.first] += filter[k][locY][locX];
            }
        }
    }
    //displayResult(result);

    cout << timestamp() - time << "s" <<endl; 

    clearData(filter, result);


    return 0;
}

int ***createFilterSample()
{
  int i, j, k;
  // init kernal
  int ***kernal = new int **[OUTC];
  // cout << "kernel" << endl  << "-------" << endl;

    for (i = 0; i < OUTC; i++) {
        kernal[i] = new int *[KH];
        for (j = 0; j < KH; j++) {
            kernal[i][j] = new int [KW];
            for (k = 0; k < KW; k++) {
                kernal[i][j][k] = rand() % 10;
            //    cout << kernal[i][j][k] << " ";
            }
        //    cout << endl;
        }
    //   cout << endl;
    }
  //  cout << "###" << endl;
  
  return kernal;
}

int ***initResultSpace(){
    int i, j, k;
    int ***result = new int **[OUTC];
    for (i = 0; i < OUTC; i++){
        result[i] = new int *[result_h];
        for (j = 0; j < result_h; j++){
            result[i][j] = new int[result_w];
            for (k = 0; k < result_w; k++){
                result[i][j][k] = 0;
            }
        }
    }
    return result;
}

void clearData( int ***kernal, int ***result)
{
  int i, j;


  for (i = 0; i < OUTC; i++)
  {
      for (j = 0; j < KH; j++)
      {
        delete[] kernal[i][j];
      }
      delete[] kernal[i];
    }
    delete[] kernal;
  

  for (i = 0; i < OUTC; i++)
  {
    for (j = 0; j < result_h; j++)
    {
      delete[] result[i][j];
    }
    delete[] result[i];
  }
  delete[] result;
}

void displayResult(int ***result)
{
  int i, j, k;
  // display result
  cout << "result for output \n --------" << endl;

  for (i = 0; i < OUTC; i++)
  {
    for (j = 0; j < result_h; j++)
    {
      for (k = 0; k < result_w; k++)
      {
        cout << result[i][j][k] << " ";
      }
      cout << endl;
    }
    cout << endl;
  }
}