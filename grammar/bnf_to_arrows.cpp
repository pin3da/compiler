using namespace std;
#include<iostream>
#include<sstream>
#include<string>

int main(){
    string line;
    while(getline(cin,line)){
        stringstream buffer(line);
        string name; buffer>>name;
        string dots; buffer>>dots;
        string prod,t; 
        while(buffer>>t)prod+=" "+t;
        
        cout<<name<<" -> "<<prod<<endl;
        while(getline(cin,line) and line.find(";") == string::npos){
            stringstream buffer(line);
            buffer>>dots;
            prod="";
            while(buffer>>t)prod+=" "+t;
            cout<<name<<" -> "<<prod<<endl;
            
        }
    }

    return 0;
}
