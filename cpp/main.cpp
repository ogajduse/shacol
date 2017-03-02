//#include "stdafx.h"
#include "iostream"
//#include <array> //for std::array
//#include <vector>  //for std::vector
#include <string>  //for std::string
#include <algorithm>
#include "limits.h"
#include "sha256.h"
//#include "stdio.h"

using namespace std;

int main(int argc, char* argv[])
{
    string vstup1 = "4c07a78b"; //32 bits
    string vstup2 = "4c07a78baec4b63"; //60 bits

    cout << endl << "Vstupní hash: " << vstup1 << endl;

    cout << INT_MAX << endl;
    //string* pole = new string[INT_MAX];
    string newHashPart = "";
    string* hashPartArray = new string[100000000];
    cout << "100 millions allocated... " << endl;

    int count = 0;
    bool test = 1;


    while (test)
    {
        hashPartArray[0] = "Ahoj";
        count++;

        for (int i = 0; i <= count; i++)
        {
            if (hashPartArray[i] == newHashPart)
            {
                test = 0;
            }
        }
        //string* hashCollision = find(hashPartArray, hashPartArray + 10, "Ahoj");
        string newHash = "Test";

        string input = "grape";
        string output1 = sha256(input);

        cout << "sha256('"<< input << "'):" << output1 << endl;

        hashPartArray[count] == newHashPart;

        //test = 0;
    }

    //string *hashCollision = find(pole, pole + delka_pole, 3);
/*
            #print count,' : ',newHashPart
            #count += 1
            newHash = hashlib.sha256(newHashPart).hexdigest()
            newHashPart = newHash[0:hashPartLength] #Special ID as input parameter for threading
            #In case of threding is needed the solution for number of position every thread!!!

        print 'Count of the cycles:', len(hashPartDeque)
        print 'Collision hash:', newHashPart
*/

    cout << "Collision found process succeeded! " << endl;
    cout << "Collision hash: " << newHashPart << endl;

    return 0;

}