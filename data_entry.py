#user_data_entry
from datetime import datetime
date_format="%d-%m-%Y"
CATEGORIES={"I":"income", "E":"Expense"}

#we use prompt to ask user to input before they gave us the data
#forexamplewe mmay ask dares for different reasons
#allow_default tell us if we should have a default value 0
#reason is that whehn user hit enter and by default it will just select the current date
def get_date(prompt, allow_default=False):
   date_str=input(prompt)
   if allow_default and not date_str:
      return datetime.today().strftime(date_format)
   
#validation check
   try:
       valid_date=datetime.strptime(date_str,date_format)
       #clean the date user type in and give us in the format we wanted
       return valid_date.strftime(date_format)
   except ValueError:
       print("invalid date format, please enter the day in dd-mm-yyyy format")
       return get_date(prompt, allow_default)
   #we call it a recursive function means we calling this fuction again and again until we get a format we want



def get_amount():
   try:
       amount=float(input("enter the amount: "))
       if amount <=0:
           raise ValueError("amount must be non-negative value")
       return amount
   except ValueError as e:
       print(e)
       return amount()
           

def get_category():
    category=input("Enter the category('I' for income or 'E' for expense): ").upper()
    if category in CATEGORIES:
       return  CATEGORIES[category]
    #its means rather than returning i and e it return income and expense
    #we can add multiple category
   
    print("invalid category,please enter 'I' for income and 'E' for Expense.")
    return get_category()
def get_description():
  return input(" enter a description(optional): ")
