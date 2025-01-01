import pandas as pd
import csv
from datetime import datetime
from data_entry import get_amount,get_category,get_date,get_description
import matplotlib.pyplot as plt

class CSV:
    CSV_FILE = "finance_data.csv"
    columns = ["date", "amount", "category", "description"]
    FORMAT= "%d-%m-%Y"
    @classmethod
    def initialize_csv(cls):
        try:
            pd.read_csv(cls.CSV_FILE)
        except FileNotFoundError:
            # Create a new file with the required columns if it doesn't exist
            df = pd.DataFrame(columns=cls.columns)
            df.to_csv(cls.CSV_FILE, index=False)

    @classmethod
    def add_entry(cls, date, amount, category, description):
        new_entry = {
            "date": date,
            "amount": amount,
            "category": category,
            "description": description,
        }
        # Append the new entry to the CSV file
        with open(cls.CSV_FILE, "a", newline="") as csvfile:
            writer = csv.DictWriter(csvfile, fieldnames=cls.columns)
            # Write the header if the file is empty
            writer.writerow(new_entry)
        print("Entry added successfully")
    @classmethod
    #it gives us all the transcations with in a daterange   
    def get_transactions(cls,start_date,end_date):
        df=pd.read_csv(cls.CSV_FILE)
      #convert all of the dates inside of the date column to a datetime object
      #to use them to filter by different transactions
      #when working with a date frame of pand we have the ability not just to access the individual rows
       #but to access all the columns
       #this line shows that date is in perfext format
        df["date"]=pd.to_datetime(df["date"],format=CSV.FORMAT)  
        start_date=datetime.strptime(start_date,CSV.FORMAT)
        end_date=datetime.strptime(end_date,CSV.FORMAT)
        #creating some things know as mask
        #mask is something that we apply to the different rows inside
        # a datafram to see if w should select that row or not
        mask=(df["date"] >= start_date) & (df["date"] <= end_date)
        filtered_df=df.loc[mask]

        if filtered_df.empty:
            print("no transcation found")
        else:
           
            print(f"Transaction from {start_date.strftime, (CSV.FORMAT)} to {end_date.strftime, (CSV.FORMAT)}")
            #one line anonymous function knons as lambda function taht we passthe paramenter
            print(
                filtered_df.to_string(
                    index=False,formatters={"date": lambda x: x.strftime(CSV.FORMAT)}
                )
            )
            total_income=filtered_df[filtered_df["category"]=="income"]["amount"].sum()
            total_expense=filtered_df[filtered_df["category"]=="expense"]["amount"].sum()
            print("\nsummary: ")
            #2f means 2 decimal
            print(f"total income: ${total_income :.2f}")
            print(f"total expense: ${total_expense :.2f}")
            print(f"Net Saving: ${total_income-total_expense:.2f}")
            return filtered_df
            #for fromatter we pass key and put a function we want to apply to every
            #single element inside a column if we wnt to format it differently

#write a function that will call these functions in the order that we want in order to collect our data
def add():
    CSV.initialize_csv()
    date=get_date("enter the date of thetranscation(dd-mm-yyyy) or enter for todays date:", allow_default=True)
    amount=get_amount()
    category=get_category()
    description=get_description()
    CSV.add_entry(date,amount,category,description)
    #plot graph
def plot_transaction(df):
    df.set_index('date',inplace=True)
    income_df=(df[df["category"]=="income"].resample("D").sum().reindex(df.index,fill_value=0))
    Expense_df=(df[df["category"]=="Expense"].resample("D").sum().reindex(df.index,fill_value=0))
    plt.figure(figsize=(10,5))
    plt.plot(income_df.index,income_df["amount"],label="income",color ="g")
    plt.plot(Expense_df.index,Expense_df["amount"],label="expense",color ="r")
    plt.xlabel("date")
    plt.ylabel("amount")
    plt.title('income and expenses over time')
    plt.legend()
    plt.grid(True)
    plt.show()

def main():
    while True:
        print("\n1. dd a new transaction")
        print("2. view transactions and summary with in a date range")
        print ("3.Exit")
        choice=input("enter your choicr(1-3): ")

        if choice=="1":
            add()
        elif choice=="2":
          start_date=get_date("enter the start date(dd-mm-yyyy):")
          end_date=get_date("enter the end date(dd-mm-yyyy):")
          df=CSV.get_transactions(start_date, end_date)
          if input("do you want to see a plot? [y/n]").lower()=="y":
              plot_transaction(df)
        elif  choice=="3":
            print("Existing...")
            break
        else:
            print("invalid choice. enter 1,2,3")
#we do not wanna run a main func unless it called
if __name__=="__main__":
    main()


         













