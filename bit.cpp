// Challenge in codeforece, the web is down at this date 5-24-26 (solution not complete)
#include <iostream>
#include <string>
using namespace std;
int main()
{
    
    int x = 0;
    string a;
    
    cin >> a;
    
    string op;
    
    for (int i = 0; i < stoi(a); i++){
        cin >> op;
        if (op == "++x" || op == "x++"){
            ++x;
            
        }
        
        else if (op == "--x" || op == "x--"){
            --x;
        }
        
    }
    
    cout << x << endl;
    
    

    return 0;
}
