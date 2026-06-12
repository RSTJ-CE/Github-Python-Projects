#include <iostream> //A-Z(65-90) , a-z(97-122) , () is 40-41, + is 43
#include <cstring>
using namespace std;
// A+AC = A + C ---- A+AB+AC
void Ft(char a[], int count);
void EnterExpression(void);
int length(char len[]);
char expression[50];
int main()
{
	EnterExpression();
	Ft(expression, length(expression));
}

void EnterExpression(void)
{
	cout << "Enter expression (No space) : ";
	cin >> expression;
}
int length(char len[])
{
	return strlen(len);
}
void Ft(char a[], int count)
{
	char term1[50];
	int term1_count = 0; // counts number of char in term 1

	for (int i = 0; i<count;i++) //Finding 1st term
	{
		if (a[i] != 43)
		{
			term1[i] = a[i];
			term1_count += 1;
		}
		else
			break;
	}
	term1[term1_count] = '\0'; //makes it a string
	cout << "First term is : " << term1;

	char term2[50]; 
	int term2_count = 0; // counts no. of char in term 2
	int t2index = 0; // index of term 2
	for (int i = term1_count+1; i<count; i++) // starts i from 2nd term
	{
		if (a[i] != 43)
		{
			
			term2[t2index] = a[i];
			t2index += 1;
			term2_count += 1;
		}
	}
	term2[term2_count] = '\0'; //makes term2 a string
	cout << "\nSecond term is : " << term2 << "\n";

	char factor[50]; //factorising starts
	int factor_count = 0;
	for (int i = 0; i < strlen(term1); i++) //scans entire term 1
	{
		for (int j = 0; j < strlen(term2); j++) // loop scans entire term 2 after e
		{
			if (term1[i] == term2[j]) //checks for factor
			{
					factor[factor_count] = term2[j];
					factor_count += 1;
					cout << "Expression can be factorised by " << term2[j] << "\n";
					term2[j] = '`';
					j = strlen(term2);
			}
		}
	}
	factor[factor_count] = '\0';
	cout << "factor is " << factor;
	cout << "\n";
}