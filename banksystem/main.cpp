#include <iostream>
#include <fstream>

using namespace std;

class BankAccount {
    public: 
    double balance = 0.0;

    BankAccount(){};

    double checkbalance(double& balance){
        return balance;
    }
    void deposit(double& balance, double dpamount){
        balance += dpamount;
    }
    void draft(double& balance, double dfamount){
        balance -= dfamount;
    }
    
};

int main() {
    BankAccount newAcc;

    ifstream inFile("balance.txt");
    if (!inFile.is_open()) {
        cout << "Error: Balance file not opening.\n";
        return 0;
    }

    inFile >> newAcc.balance;
    inFile.close();

    ofstream outFile;
    
    int choice;
    do {
        cout << "************************\n";
        cout << "  Welcome to your ATM\n";
        cout << "************************\n";
        cout << "Please select an action:\n";
        cout << "  1. Check Balance\n";
        cout << "  2. Make a deposit\n";
        cout << "  3. Withdraw currency\n";
        cout << "  4. Exit\n";
        cout << "************************\n";
        
        cin >> choice;

        switch (choice) {
            case 1:
                cout << "**************************\n";
                cout << "Your current balance is $" << newAcc.balance << "\n";
                newAcc.checkbalance(newAcc.balance);
                break;
            case 2:
                double dpamount;
                cout << "************************\n";
                cout << "  Enter the amount\n";
                cout << "************************\n";
                cin >> dpamount;
                if (dpamount < 0) {
                    cout << "  Invalid amount\n";
                    break;
                }
                newAcc.deposit(newAcc.balance, dpamount);

                //add to history
                outFile.open("history.txt", ios::app);
                if(!outFile.is_open()){
                    cout << "History file is not openning\n";
                } 
                outFile << "add $" << dpamount << endl;
                outFile.close();
                cout << "**************************\n";
                cout << "$" << dpamount << " have been deposited\n";
                break;
            case 3:
                double dfamount;
                cout << "************************\n";
                cout << "  Enter the amount\n";
                cout << "************************\n";
                cin >> dfamount;
                if (dfamount < 0) {
                    cout << "Invalid amount\n";
                    break;
                }
                else if (newAcc.balance < dfamount) {
                    cout << "Not enough currency\n";
                    break;
                }
                newAcc.draft(newAcc.balance, dfamount);

                //add to history
                outFile.open("history.txt", ios::app);
                if(!outFile.is_open()){
                    cout << "History file is not openning\n";
                }
                outFile << "Withdraw $" << dfamount << endl;
                outFile.close();
                cout << "***************************\n";
                cout << "$" << dfamount << " have been withdrawn\n";
                break;
            case 4:
                outFile.open("balance.txt");
                if (!outFile.is_open()) {
                    cout << "Error: Balance file not opening.\n";
                    return 0;
                }
                outFile << newAcc.balance << endl;
                outFile.close();
                cout << "************************\n";
                cout << "  Thank you for using our ATM\n";
                cout << "************************\n";
                return 0;
            default:
                cout << "  Invalid choice\n";
                break;
        }
    } while (choice != 4);

    return 0;
}