#define RED 4
#define GREEN 5
#define BLUE 6
#define YELLOW 7
#define K1 8
#define K2 9
#define Knob A0
#define LDR A2
#define CLK 10
#define DIO 11
#define buzzer 3
#include "RichShieldTM1637.h"  // for displayer
#include "RichShieldPassiveBuzzer.h"
PassiveBuzzer music(buzzer);
TM1637 Bal(CLK,DIO);
//////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////
//Global variables//
double balance, expense, accumulated_expense = 0, Daily_Expense[30], Balance_Progress[30], Accumulated_Expense_Progress[30];
int PreviousInput = -1; //variable used for ReadBalance(), so that digit resets to 0 upon confirmation of input
int Check_if_below_balance = 0; //variable used for checking whether balance is sufficient
int day = 0; //variable used to track days
int lowest_spending=9999,highest_spending=0; //variable used for finding highest and lowest day spending
int z = 1; //variable used for while loop at end of function
int data[4] = {0,0,0,0};
//////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////
//Functions declaration//
void ReadBalance(double &value,double max);
void TrackDaily_Expense(double daily_expense[], double &bal, double &acc);
void EndOfMonthAnalysis(void);
void graph(double bank[], double exp, double acc_exp[], double daily_exp[]);
//////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////
void setup() {
pinMode(K1,INPUT_PULLUP);
pinMode(K2,INPUT_PULLUP);
pinMode(RED,OUTPUT);
pinMode(GREEN,OUTPUT);
pinMode(YELLOW,OUTPUT);
Bal.init();
Serial.begin(9600);
}
///////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////
void loop() 
{
  day=0,Check_if_below_balance=0,accumulated_expense=0,PreviousInput=-1,z=1,highest_spending=0,lowest_spending=9999; //reset these datas to default
  Serial.println("Please enter balance :");
  ReadBalance(balance,9999); //Read balance
  Serial.print("Your balance is ");
  Serial.println(balance);
  Serial.println("Please enter target expense for the month ");
  ReadBalance(expense,balance); //Read total expense
  Serial.print("Your target expense for the month is ");
  Serial.println(expense);
  TrackDaily_Expense(Daily_Expense, balance, accumulated_expense);
  delay(2000);
  EndOfMonthAnalysis();
  delay(1000);
  Serial.println("Press K1 to review graph");
  while(z)
  {
    if(digitalRead(K1) == 0)
    {
    graph(Balance_Progress, expense, Accumulated_Expense_Progress, Daily_Expense);
    z = 0;
    while(digitalRead(K1) == 0)
    delay(100);
    }
  }
}
//////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////  Read values
void ReadBalance(double &value, double max) //reading input from user
{
  int count = 3;
  int confirmation = 0;
  Check_if_below_balance = 0; //variable for checking if balance is sufficient
  while (confirmation == 0)
  {
    if (analogRead(Knob) / 112 != PreviousInput)
    {
      data[count] = analogRead(Knob) / 112; //Knob adjustment for 1-9
      PreviousInput = -1;
    }
    if (digitalRead(K1) == 1 && digitalRead(K2) == 0) //switches inbetween the numbers on displayer
    {
      count--;
      if (count < 0)
      {
        count = 3;
      }
      delay(200);
      for (int i = 0; i < 3; i++) //blink to show user which digit they selected
      {
        Bal.display(count, 16);
        delay(100);
        Bal.display(count, data[count]);
      }
    }
    for (int i = 0; i < 4; i++) //Display each knob values
    {
      Bal.display(i, data[i]);
    }
    if (digitalRead(K1) == 0) //confirmation button
    {
      delay(200);
      value = data[0] * 1000 + data[1] * 100 + data[2] * 10 + data[3]; //calculates the value
      if (value <= max) //if value is in acceptable range, confirms input
      {
        confirmation = 1;
        delay(200);
        digitalWrite(GREEN, HIGH);
        music.playTone(1000, 120); //music to signal user confirms
        for (int j = 0; j < 4; j++) //Blink digits to signal user confirms
        {
          for (int i = 0; i < 4; i++)
          {
            Bal.display(i, 16); // make all digit disappear
          }
          delay(100);
          Bal.display(j, data[j]); // make digit appear
        }
        delay(200);
        digitalWrite(GREEN, LOW); //indicate confirmation
        PreviousInput = analogRead(Knob) / 112;
        for (int i = 0; i < 4; i++) //resets loop back to 0 for next inputs
        {
          data[i] = 0;
        }
        while (digitalRead(K1) == 0) //prevent user from holding K2 which read multiple input
        {
          delay(100);
        }
      }
      else //if value is not acceptable, show error message
      {
        Serial.println(" ");
        Serial.println("Please enter value within balance");
        music.playTone(100, 120); //Signals that value is not accepted
        digitalWrite(RED, HIGH);  //signals that value is not accepted
        delay(1000);
        digitalWrite(RED, LOW);
        Check_if_below_balance = 1;
        PreviousInput = analogRead(Knob) / 112;
        if (day > 0) //check if the function is being used to track daily expense
        {
          value = data[0] * 1000 + data[1] * 100 + data[2] * 10 + data[3]; //assigns the value as the user has spent more than balance
          Serial.println("Exceeded balance...");
          delay(200);
          break;
        }
        for (int i = 0; i < 4; i++) //resets loop back to 0 for next inputs
        {
          data[i] = 0;
          count = 3;
        }
        while (digitalRead(K1) == 0 && digitalRead(K2) == 0)
        {
          delay(100);
        }
      }
    }
  }
}
/////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////// Graph function
void graph(double bank[], double exp, double acc_exp[], double daily_exp[] )
{
  Serial.println("=== GRAPH START ===");
  for(int i = 0;i<day;i++)
  {
    Serial.print(bank[i]);
    Serial.print(",");
    Serial.print(exp);
    Serial.print(",");
    Serial.print(acc_exp[i]);
    Serial.print(",");
    Serial.println(daily_exp[i]);
  }
  Serial.println("=== GRAPH ENDS ===");
}
//////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////// Track daily expense
void TrackDaily_Expense(double daily_expense[], double &bal, double &acc)
{
  for (int q = 0; q < 30; q++)
  {
    day += 1; //counts number of days
    Serial.print("Please enter your expense for day ");
    Serial.print(q + 1);
    Serial.print(": ");
    ReadBalance(daily_expense[q], bal);
    Balance_Progress[q] = bal;
    bal -= daily_expense[q];
    Accumulated_Expense_Progress[q] = acc;
    acc += daily_expense[q];
    if (daily_expense[q] > highest_spending)
    {
      highest_spending = daily_expense[q];
    }
    if (daily_expense[q] < lowest_spending)
    {
      lowest_spending = daily_expense[q];
    }
    Serial.println(daily_expense[q]);
    if (Check_if_below_balance == 1) //check if balance is > 0, if more than 0, breaks and skip to graph and analysis mode
    {
      break;
    }
  }
}
////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////// end of month analysis
void EndOfMonthAnalysis()
{
  double daily_expense = accumulated_expense/day;
  if (accumulated_expense <= expense && balance >= 0) // IF TARGET MET
  {
    long savings = expense - accumulated_expense;
    long YearlySavings = (expense*12)-(daily_expense*365);
    Serial.print("Days lasted: ");
    Serial.println(day);
    Serial.print("Highest spending in a day = ");
    Serial.print(highest_spending);
    Serial.println("!");
    Serial.print("Lowest spending in a day = ");
    Serial.print(lowest_spending);
    Serial.println("!");
    Serial.print("Congratulations! you met your target and exceeded by $");
    Serial.print(savings);
    Serial.println("!");
    Serial.print("your average daily expenses is $");
    Serial.println(daily_expense);
    Serial.print("if you continue this trend, you will save $");
    Serial.print(YearlySavings);
    Serial.println(" in a year!");
    int melody[] = {262, 330, 392, 523, 659, 523, 659, 784};
    int duration = 180;
        if (accumulated_expense >= (expense*0.95)) // IF -5%
    {
      digitalWrite(YELLOW, HIGH);
    }
    else
    {
      digitalWrite(GREEN, HIGH);
    }
    for (int i = 0; i < 8; i++)
    {
      music.playTone(melody[i], duration);
      delay(60);  // shorter pause = more energetic
    }
    delay(2000);
    digitalWrite(GREEN, LOW);
    digitalWrite(YELLOW, LOW);
  }

  else
  {
    long overspend = accumulated_expense - expense;
    long YearlySpendings = (daily_expense*365) - (expense*12);
    Serial.print("Days lasted: ");
    Serial.println(day);
    Serial.print("Highest spending in a day = ");
    Serial.print(highest_spending);
    Serial.println("!");
    Serial.print("Lowest spending in a day = ");
    Serial.print(lowest_spending);
    Serial.println("!");
    Serial.print("Nice try! You can do better. Exceeded target by $"); //if failed.
    Serial.println(overspend);
    Serial.print("Your average daily expenses is $");
    Serial.print(accumulated_expense / day);
    Serial.println("!");
    Serial.print("If you continue this trend, you will spend an extra $");
    Serial.print(YearlySpendings);
    Serial.println(" in a year!");
    int sadMelody[] = {440, 392, 349, 330, 294, 222, 200, 190};
    int durations[] = {400, 400, 500, 500, 600, 600, 800, 1200};
    digitalWrite(RED, HIGH);
    for (int i = 0; i < 8; i++)
    {
      music.playTone(sadMelody[i], durations[i]);
      delay(50);  // short pause between notes
    }
    delay(2000);
    digitalWrite(RED, LOW);
  }

}
