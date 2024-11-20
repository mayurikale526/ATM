class ATM:
    def __init__(self, balance=0):
        self.balance = balance

    def check_balance(self):
        print(f"Your current balance is: ₹{self.balance}\n")

    def deposit(self, amount):
        if amount > 0:
            self.balance += amount
            print(f"₹{amount} deposited successfully.\n")
        else:
            print("Invalid deposit amount.\n")

    def withdraw(self, amount):
        if 0 < amount <= self.balance:
            self.balance -= amount
            print(f"₹{amount} withdrawn successfully.\n")
        elif amount > self.balance:
            print("Insufficient balance.\n")
        else:
            print("Invalid withdrawal amount.\n")

    def run(self):
        while True:
            print("ATM Menu:")
            print("1. Check Balance")
            print("2. Deposit Money")
            print("3. Withdraw Money")
            print("4. Exit")
            try:
                choice = int(input("\nEnter your choice: "))
                if choice == 1:
                    self.check_balance()
                elif choice == 2:
                    amount = float(input("Enter the amount to deposit: ₹"))
                    self.deposit(amount)
                elif choice == 3:
                    amount = float(input("Enter the amount to withdraw: ₹"))
                    self.withdraw(amount)
                elif choice == 4:
                    print("Thank you for using the ATM. Goodbye!")
                    break
                else:
                    print("Invalid choice, please try again.\n")
            except ValueError:
                print("Invalid input. Please enter a number.\n")

atm = ATM(balance=50000)  
atm.run()