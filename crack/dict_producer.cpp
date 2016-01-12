#include<iostream>
#include<fstream>
#include<iomanip>
using namespace std;
int main() {
    ofstream out("dict2.txt");
    for (int i = 280000; i < 290000; i++) {
        out << setw(6) << setfill('0') << i << endl;
    }
}
