#include <iostream>
#include <vector>
#include <map>
#include <set>
#include <sstream>
// rukkkkk
using namespace std;

int main() {
    vector<pair<int, int>> links;
    set<int> s;

    // cout << "Enter source and destination pairs separated by space (e.g., '1 2 3 4'): " << endl;

    // string line;
    // getline(cin, line); // Read the entire line

    // istringstream iss(line);
    // int src, dst;

    // // Read pairs from the line until no more pairs are available
    // while (iss >> src >> dst) {
    //     // cout<<"The input is "<<endl;
    //     // cout<<src<<endl;
    //     // cout<<dst<<endl;
    //     links.push_back({src, dst});
    //     s.insert(src);
    //     s.insert(dst);
    // }
    while (true) {
        int src, dst;
        cin >> src >> dst;
        links.push_back({src, dst});
        s.insert(src);
        s.insert(dst);
    }
   
    long double n = s.size();

    // Compute the number of links pointing to each page
    map<int, long double> m;
    for (auto link : links) {
        m[link.first]++;
    }

    // Initialize the hyperlink matrix H
    vector<vector<long double>> H(n, vector<long double>(n, 0));
    for (auto link : links) {
        H[link.second][link.first] = 1.0 / m[link.first];
    }

    // Identify dangling nodes and compute A matrix
    vector<vector<long double>> A(n, vector<long double>(n, 0));
    vector<int> dangling_nodes;
    for (int i = 0; i < n; i++) {
        if (m[i] == 0) {
            dangling_nodes.push_back(i);
            for (int j = 0; j < n; j++) {
                A[j][i] = 1.0 / n;
            }
        }
    }

    // Initialize PageRank vector
    vector<long double> I(n, 1.0 / n);

    // Iteratively compute PageRank
    for (int iter = 0; iter < 100; iter++) {
        vector<long double> I_next(n, 0);

        // Compute the next PageRank vector
        for (int i = 0; i < n; i++) {
            long double a = 0.15 / n;
            for (int j = 0; j < n; j++) {
                a += 0.85 * H[i][j] * I[j];
            }
            for (auto dangling : dangling_nodes) {
                a += 0.85 * A[i][dangling] * I[dangling];
            }
            I_next[i] = a;
        }

        // Update the PageRank vector
        I = I_next;
    }

    // Output PageRank values
    long double ans = 0;
    for (int i = 0; i < n; i++) {
        cout << i << " = " << I[i] << endl;
        ans += I[i];
    }
    cout << "s = " << ans << endl;

    return 0;
}
