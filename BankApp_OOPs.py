import cx_Oracle as cx
import sys
con = cx.connect('bank/vishal@127.0.0.1/xe')
cur = con.cursor()
import os
from base64 import b64encode

class Bank: #This class contains all the functions for bank services

    def admin_menu(self):
        os.system('cls')
        validate=False
                                #Admin Menu
        prompt = int(raw_input("1. Print Closed Accounts History\n2. FD Report of a Customer"       
                               "\n3. FD Report of a Customer vis-a-vis another Customer"
                               "\n4. FD Report w.r.t a particular FD amount \n5. Loan Report of a Customer"
                               "\n6. Loan Report of a Customer vis-a-vis another Customer"
                               "\n7. Loan Report w.r.t a particular Loan amount\n"
                               "8. Loan - FD Report of Customers\n9. Report of Customers who are yet to avail a loan\n"
                               "10. Report of Customers who are yet to open a FD account\n"
                               "11. Report of Customers who neither have a loan nor an FD account with the bank"
                               "\n0. Admin Logout\n"))
        ###################################################################################################################

        if prompt==1: #closed account history
            os.system('cls')
            cur.execute("SELECT account_num,date_closed FROM cust_account where account_status='closed'")
            x=cur.fetchall()
            print "\n***********************************************************\n"
            print " ___________________________________"
            print "| Account Number |    Date Closed   |"
            print "|                |    (yy-mm-dd)    |"
            print "|________________|__________________|"
            for i in x:
                date = str(i[1])
                print "| ", repr(i[0]).rjust(12), " | ", repr(date[2:11]).rjust(14), " | "
            print "|________________|__________________|"

            print "\n***********************************************************\n"
            raw_input("\nPress Enter To GO BACK\n")
            self.admin_menu()
        ###################################################################################################################

        elif prompt == 2: #FD report of a customer
            os.system('cls')
            while validate <>True:
                try:
                    cust_id=int(raw_input("Enter Customer ID: "))
                except:
                    print "\nInvalid ID.Please RETRY\n"
                    raw_input("\nPress Enter To GO BACK\n")
                    self.admin_menu()
                cur.execute("SELECT account_num FROM cust_account where cust_id=:1 and account_type='fd'",{'1':cust_id})
                x=cur.fetchall()
                if x is None:
                    print "N/A"
                else:
                    print "\n***********************************************************\n"
                    print " ________________________________________________"
                    print "| Account Number |     Amount       |    Term    |"
                    print "|________________|__________________|____________|"
                    for i in x:
                        cur.execute("SELECT amount,term FROM cust_fd where account_num=:1",{'1':i[0]})
                        y=cur.fetchone()
                        print "| ", repr(i[0]).rjust(12), " | ", repr(y[0]).rjust(14), " | ", repr(y[1]).rjust(8), " | "
                    print "|________________|__________________|____________|"

                    print "\n***********************************************************\n"
                    validate=True
            raw_input("\nPress Enter To GO BACK\n")
            self.admin_menu()

        ###################################################################################################################

        elif prompt==3: #FD report of customer vis-a-vis another customer
            os.system('cls')
            while validate <>True:
                sum=0
                try:
                    cust_id=int(raw_input("Enter Customer ID: "))
                except:
                    print "\nInvalid ID.Please RETRY"
                    raw_input("\nPress Enter To GO BACK!\n")
                    self.admin_menu()
                cur.execute("SELECT account_num FROM cust_account where cust_id=:1 and account_type='fd'",{'1':cust_id})
                x=cur.fetchall()
                for i in x:
                    cur.execute("SELECT amount,term FROM cust_fd where account_num=:1", {'1': i[0]})
                    sum+= cur.fetchone()[0]
                #print sum
                if x is None:
                    print "N/A"
                else:
                    cur.execute(
                        "select  cust_account.cust_id,cust_account.account_num,cust_fd.amount,cust_fd.term FROM cust_fd inner join "
                        "cust_account ON cust_fd.account_num=cust_account.account_num where cust_fd.amount >:1 and "
                        "cust_account.account_type='fd' ", {'1': sum})
                    x = cur.fetchall()
                    print "\n***********************************************************\n"
                    print " _______________________________________________________________"
                    print "| Customer ID    |     A/c Number   |    Amount    |    Term    |"
                    print "|________________|__________________|______________|____________|"
                    for i in x:
                        print "| ", repr(i[0]).rjust(12), " | ", repr(i[1]).rjust(14), " | ", repr(i[2]).rjust(10), " | ",repr(i[3]).rjust(8)
                    print "|________________|__________________|______________|____________|"

                    print "\n***********************************************************\n"
                    validate=True
            raw_input("\nPress Enter To GO BACK\n")
            self.admin_menu()

        ###################################################################################################################

        elif prompt==4: #FD report w.r.t a particular FD amount
            os.system('cls')
            while validate <>True:
                amount=float(raw_input("Enter Amount: "))
                if amount <=0 or amount%1000 <> 0:
                    print "\nEnter valid Amount."
                else:
                    validate=True
            cur.execute("select  cust_account.cust_id,cust_fd.amount FROM cust_fd inner join "
                        "cust_account ON cust_fd.account_num=cust_account.account_num where cust_fd.amount >:1 and "
                        "cust_account.account_type='fd' ",{'1':amount})
            x=cur.fetchall()
            print "\n***********************************************************\n"
            print " _____________________________________________________________________"
            print "| Customer ID    |     First Name   |     Last Name    |     Amount   |"
            print "|________________|__________________|__________________|______________|"
            for i in x:
                cur.execute("SELECT first_name,last_name FROM cust_info where cust_id=:1",{'1':i[0]})
                y=cur.fetchone()
                print "| ", repr(i[0]).rjust(12), " | ", repr(y[0]).rjust(14), " | ", repr(y[1]).rjust(14), " | ", repr(i[1]).rjust(10), " | "
            print "|________________|__________________|__________________|______________|"

            print "\n***********************************************************\n"
            raw_input("\nPress Enter To GO BACK\n")
            self.admin_menu()
        ###################################################################################################################

        elif prompt==5: #Loan report
            os.system('cls')
            while validate <>True:
                try:
                    cust_id=int(raw_input("Enter Customer ID: "))
                except:
                    print "\nInvalid ID.Please RETRY"
                    raw_input("\nPress Enter To GO BACK\n")
                    self.admin_menu()
                cur.execute("SELECT account_num FROM cust_account where cust_id=:1 and account_type='loan'",{'1':cust_id})
                x=cur.fetchall()
                if x is None:
                    print "N/A"
                else:
                    print "\n***********************************************************\n"
                    print " ________________________________________________"
                    print "| Account Number |     Amount       |    Term    |"
                    print "|________________|__________________|____________|"
                    for i in x:
                        cur.execute("SELECT amount,term FROM cust_fd where account_num=:1",{'1':i[0]})
                        y=cur.fetchone()
                        print "| ", repr(i[0]).rjust(12), " | ", repr(y[0]).rjust(14), " | ", repr(y[1]).rjust(8), " | "
                    print "|________________|__________________|____________|"

                    print "\n***********************************************************\n"
                    validate=True
            raw_input("\nPress Enter To GO BACK\n")
            self.admin_menu()
        ###################################################################################################################

        elif prompt==6:
            os.system('cls')
            while validate <>True:
                sum=0
                try:
                    cust_id=int(raw_input("Enter Customer ID: "))
                except:
                    print "\nInvalid ID.Please RETRY"
                    raw_input("\nPress Enter To GO BACK\n")
                    self.admin_menu()
                cur.execute("SELECT account_num FROM cust_account where cust_id=:1 and account_type='loan'",{'1':cust_id})
                x=cur.fetchall()
                for i in x:
                    cur.execute("SELECT amount,term FROM cust_fd where account_num=:1", {'1': i[0]})
                    sum+= cur.fetchone()[0]
                #print sum
                if x is None:
                    print "N/A"
                else:
                    cur.execute(
                        "select  cust_account.cust_id,cust_account.account_num,cust_fd.amount,cust_fd.term FROM cust_fd inner join "
                        "cust_account ON cust_fd.account_num=cust_account.account_num where cust_fd.amount >:1 and "
                        "cust_account.account_type='loan' ", {'1': sum})
                    x = cur.fetchall()
                    print "\n***********************************************************\n"
                    print " _______________________________________________________________"
                    print "| Customer ID    |     A/c Number   |    Amount    |    Term    |"
                    print "|________________|__________________|______________|____________|"
                    for i in x:
                        print "| ", repr(i[0]).rjust(12), " | ", repr(i[1]).rjust(14), " | ", repr(i[2]).rjust(10), " | ",repr(i[3]).rjust(8)
                    print "|________________|__________________|______________|____________|"

                    print "\n***********************************************************\n"
                    validate=True
            raw_input("\nPress Enter To GO BACK\n")
            self.admin_menu()

        ###################################################################################################################

        elif prompt==7:
            os.system('cls')
            while validate <>True:
                amount=float(raw_input("Enter Amount: "))
                if amount <=0 or amount%1000 <> 0:
                    print "\nEnter valid Amount."
                else:
                    validate=True
            cur.execute("select  cust_account.cust_id,cust_fd.amount FROM cust_fd inner join "
                        "cust_account ON cust_fd.account_num=cust_account.account_num where cust_fd.amount >:1 and "
                        "cust_account.account_type='loan' ",{'1':amount})
            x=cur.fetchall()
            print "\n***********************************************************\n"
            print " _______________________________________________________________________"
            print "| Customer ID    |     First Name   |     Last Name    |      Amount    |"
            print "|________________|__________________|__________________|________________|"
            for i in x:
                cur.execute("SELECT first_name,last_name FROM cust_info where cust_id=:1",{'1':i[0]})
                y=cur.fetchone()
                print "| ", repr(i[0]).rjust(12), " | ", repr(y[0]).rjust(14), " | ", repr(y[1]).rjust(14), " | ", repr(i[1]).rjust(12), " | "
            print "|________________|__________________|__________________|________________|"

            print "\n***********************************************************\n"
            raw_input("\nPress Enter To GO BACK\n")
            self.admin_menu()

        ###################################################################################################################

        elif prompt==8:
            os.system('cls')
            loan_sum=0
            fd_sum=0
            cur.execute("SELECT cust_id,first_name,last_name from cust_info")
            x=cur.fetchall()
            for i in x:
                cur.execute("SELECT  account_num,account_type from cust_account where cust_id=:1 and account_type in('fd','loan')",{'1':i[0]})
                y=cur.fetchall()
                if len(y)==0:

                    continue
                else:
                    for j in y:
                        if j[1]=='fd':
                            cur.execute("SELECT amount from cust_fd where account_num=:1",{'1':j[0]})
                            fd_sum+=cur.fetchone()[0]
                        else:
                            cur.execute("SELECT amount from cust_fd where account_num=:1", {'1': j[0]})
                            loan_sum += cur.fetchone()[0]
                    if loan_sum > fd_sum:
                        print "\n***********************************************************\n"
                        print " ________________________________________________________________________________________"
                        print "| Customer ID    |     First Name   |     Last Name    |      FD Sum    |      Loan Sum  |"
                        print "|________________|__________________|__________________|________________|________________|"
                        print "| ", repr(i[0]).rjust(12), " | ", repr(i[1]).rjust(14), " | ", repr(i[2]).rjust(14), " | ", repr(fd_sum).rjust(12), " | ", repr(loan_sum).rjust(12), " | "
                        print "|________________|__________________|__________________|________________|________________|"
                        print "\n***********************************************************\n"

            raw_input("\nPress Enter To GO BACK\n")
            self.admin_menu()

        ###################################################################################################################

        elif prompt==9:
            os.system('cls')
            cur.execute("select i.cust_id,i.first_name,i.last_name FROM cust_info i,cust_account a where i.cust_id=a.cust_id(+) and i.cust_id not in(select cust_id from cust_account where account_type in('loan'))")
            x=cur.fetchall()
            if x is None:
                print "\nNo Such Customer"
                raw_input("\nPress Enter To GO BACK")
                self.admin_menu()
            else:
                print "\n***********************************************************\n"
                print " ______________________________________________________"
                print "| Customer ID    |     First Name   |     Last Name    |"
                print "|________________|__________________|__________________|"
                for i in x:
                    print "| ", repr(i[0]).rjust(12), " | ", repr(i[1]).rjust(14), " | ", repr(i[2]).rjust(14), " | "
                print "|________________|__________________|__________________|"
                print "\n***********************************************************\n"
                raw_input("\nPress Enter To GO BACK")
                self.admin_menu()

        ###################################################################################################################

        elif prompt==10:
            os.system('cls')
            cur.execute("select i.cust_id,i.first_name,i.last_name FROM cust_info i,cust_account a where i.cust_id=a.cust_id(+) and i.cust_id not in(select cust_id from cust_account where account_type in('fd'))")
            x=cur.fetchall()
            if x is None:
                print "\nNo Such Customer"
                raw_input("\nPress Enter To GO BACK")
                self.admin_menu()
            else:
                print "\n***********************************************************\n"
                print " ______________________________________________________"
                print "| Customer ID    |     First Name   |     Last Name    |"
                print "|________________|__________________|__________________|"
                for i in x:
                    print "| ", repr(i[0]).rjust(12), " | ", repr(i[1]).rjust(14), " | ", repr(i[2]).rjust(14), " | "
                print "|________________|__________________|__________________|"
                print "\n***********************************************************\n"
                raw_input("\nPress Enter To GO BACK")
                self.admin_menu()
        ###################################################################################################################

        elif prompt==11:
            os.system('cls')
            cur.execute("select i.cust_id,i.first_name,i.last_name FROM cust_info i,cust_account a where i.cust_id=a.cust_id(+) and i.cust_id not in(select cust_id from cust_account where account_type in('fd','loan'))")
            x=cur.fetchall()
            if x is None:
                print "\nNo Such Customer"
                raw_input("\nPress Enter To GO BACK")
                self.admin_menu()
            else:
                print "\n***********************************************************\n"
                print " ______________________________________________________"
                print "| Customer ID    |     First Name   |     Last Name    |"
                print "|________________|__________________|__________________|"
                for i in x:
                    print "| ", repr(i[0]).rjust(12), " | ", repr(i[1]).rjust(14), " | ", repr(i[2]).rjust(14), " | "
                print "|________________|__________________|__________________|"
                print "\n***********************************************************\n"
                raw_input("\nPress Enter To GO BACK")
                self.admin_menu()

        ###################################################################################################################
        elif prompt==0:
            os.system('cls')
            sys.exit("Thank You")

        ###################################################################################################################

        else:
            os.system('cls')
            print"\nSelect Right Option . Try Again\n"
            raw_input("\nPress Enter To GO BACK\n")
            self.admin_menu()

        ###################################################################################################################



    
    def openac(self,cust_id): #functionality to choose type of account to open
        os.system('cls')
        prompt = int(raw_input("1. Savings\n2. Current\n3. FD\n4. GO BACK\n"))
        amount=0
        deposit=0
        net_amount=0
        validate=False
        if prompt == 1:
            cur.execute("SELECT last_number FROM user_sequences WHERE sequence_name = 'AC'")
            account_num = cur.fetchone()[0]
            cur.execute("SELECT account_num,account_type from cust_account where cust_id=:1 and account_type='savings' and account_status !='closed'",{'1':cust_id})
            x=cur.fetchone()
            if x is not None:
                print "\nYou Already Have a Savings Account with account number: ",x[0]
                raw_input("\nPress Enter To GO BACK")
                self.openac(cust_id)
            cur.execute("INSERT INTO cust_account(account_num,cust_id,account_type) VALUES(ac.nextval,:1,'savings')",{'1':cust_id})
            cur.execute("INSERT INTO cust_bal (trans_id,account_num,account_type,amount,deposit,net_amount,"
                        "transaction_date) VALUES( trans_id.nextval,:1,'savings',:2,:3,:4,sysdate)", (account_num,amount, deposit, net_amount))
            con.commit()
            print "\n***Please Note You Savings Account Number: ",account_num,"***\n"
            raw_input("\nPress Enter To GO BACK\n")
            self.transaction(cust_id)

        elif prompt==2:
            cur.execute("SELECT account_num,account_type from cust_account where cust_id=:1 and account_type='current'",{'1':cust_id})
            x=cur.fetchone()
            if x is not None:
                print "\nYou Already Have a Savings Account with account number: ",x[0]
                raw_input("\nPress Enter To GO BACK")
                self.openac(cust_id)
            print "\nPlease Deposit 5000 minimum to open an current account\n"
            while validate <> True:
                try:
                    deposit = float(raw_input("Amount to deposit:"))
                except:
                    print "\nEnter Integer Value"
                    continue
                net_amount = deposit
                amount = 0
                if deposit < 5000:
                    print "\nPlease Deposit a Minimum Sum of 5000"
                else:
                    validate=True
            cur.execute("SELECT last_number FROM user_sequences WHERE sequence_name = 'AC'")
            account_num = cur.fetchone()[0]
            cur.execute("INSERT INTO cust_account(account_num,cust_id,account_type) VALUES(ac.nextval,:1,'current')",{'1':cust_id})
            cur.execute("INSERT INTO cust_bal (trans_id,account_num,account_type,amount,deposit,net_amount,"
                        "transaction_date) VALUES( trans_id.nextval,:1,'current',:2,:3,:4,sysdate)", (account_num,amount, deposit, net_amount))
            con.commit()
            print "\n***Please Note You Current Account Number: ", account_num, "***\n"
            raw_input("\nPress Enter To GO BACK\n")
            self.transaction(cust_id)

        elif prompt == 3:
            cur.execute("SELECT last_number FROM user_sequences WHERE sequence_name = 'AC'")
            account_num = cur.fetchone()[0]
            while validate <>True:
                amount=float(raw_input("Enter Amount to be Deposited for FD:"))
                if amount <=0 or amount%1000 <> 0:
                    print "\nEnter valid Amount.\n"
                else:
                    validate=True
            while validate <>False:
                term=int(raw_input("Enter term of Deposit(in Months): "))
                if term <12:
                    print "\nEnter Valid Months(>12).\."
                else:
                    validate=False
            cur.execute("INSERT INTO cust_account(account_num,cust_id,account_type) VALUES(ac.nextval,:1,'fd')",{'1':cust_id})
            cur.execute("INSERT INTO cust_fd VALUES(:1,:2,:3)", (account_num,amount,term))
            con.commit()
            print "\n***Please Note You FD Account Number: ",account_num,"***\n"
            raw_input("\nPress Enter To GO BACK\n")
            self.transaction(cust_id)
        elif prompt == 4:
            self.transaction(cust_id)
        else:
            print "\nYou Have Choosen Wrong Option Please Retry\n"
            raw_input("\nPress Enter To GO BACK\n")
            self.openac(cust_id)

    def transaction(self,cust_id):
        os.system('cls')
        validate=False
        prompt = int(raw_input("1. Address Change\n2. Open Account\n3. Deposit money\n4. Withdraw money\n5. Transfer "
                               "Money\n6. Print Statement\n7. Account Closure\n8. Avail Loan\n9. My Accounts\n0. Logout\n"))
        ###################################################################################################################

        if prompt == 1:
            os.system('cls')
            house_no = int(raw_input("House No.: "))
            city = raw_input("City: ")
            state = raw_input("State: ")
            validate=True
            while validate != False:
                pin = int(raw_input("Zip: "))
                if len(list(str(pin))) != 6:
                    print "Enter Valid 6 digit Zip"
                else:
                    validate = False
            cur.execute("UPDATE cust_info set house_no=:1,city=:2,state=:3,zip=:4 where cust_id=:5",( house_no, city, state, pin,cust_id))
            con.commit()
            raw_input("\nPress Enter To GO BACK\n")
            self.transaction(cust_id)
        ###################################################################################################################

        elif prompt == 2:

            self.openac(cust_id)

        ###################################################################################################################

        elif prompt == 3:
            os.system('cls')
            while validate <>True:
                try:
                    account_num=int(raw_input("Enter Account Number To Deposit: "))
                except:
                    print "\nEnter Integer Value\n"
                    raw_input("\nPress Enter To GO BACK\n")
                    self.transaction(cust_id)
                cur.execute("SELECT account_status from cust_account where account_num=:1 and cust_id=:2",{'1':account_num,'2':cust_id})
                x=cur.fetchone()
                if x is None:
                    print "\nEnter Valid A/c No.\n"
                    raw_input("\nPress Enter To GO BACK\n")
                    self.transaction(cust_id)
                if x[0] =="closed":
                    print "\nThis Account is Closed.Please Enter an 'active' A/c No.\n"
                    raw_input("Press Enter To GO BACK\n")
                    self.transaction(cust_id)
                dep=float(raw_input("Enter Ammount To be Deposited:    "))

                cur.execute("SELECT amount,account_type,net_amount from cust_bal where account_num=:1 ORDER BY transaction_date desc",{'1':account_num});
                x = cur.fetchone()
                if x is None:
                    print "\nEnter Valid A/c No.\n"
                else:
                    validate=True
            bal=x[0]
            account_type=x[1]
            if bal==None:
                bal=0
            bal=x[2]
            net_amount=bal+dep
            print "\nBalance After Deposit: ",net_amount
            cur.execute("INSERT INTO cust_bal (trans_id,account_num,account_type,amount,deposit,net_amount,wdraw,transaction_date) "
                        "VALUES(trans_id.nextval,:1,:2,:3,:4,:5,0,sysdate)",(account_num,account_type,bal,dep,net_amount))
            con.commit()
            raw_input("\nPress Enter To GO BACK")
            self.transaction(cust_id)
        ###################################################################################################################

        elif prompt == 4:
            os.system('cls')
            while validate <>True:
                try:
                    account_num = int(raw_input("Enter Account Number To Withdraw: "))
                except:
                    print "\nEnter Integer Value\n"
                    raw_input("Press Enter To GO BACK\n")
                    self.transaction(cust_id)
                cur.execute("SELECT account_status from cust_account where account_num=:1 and cust_id=:2",{'1':account_num,'2':cust_id})
                x=cur.fetchone()
                if x is None:
                    print "\nEnter Valid A/c No.\n"
                    raw_input("Press Enter To GO BACK\n")
                    self.transaction(cust_id)
                if x[0] =="closed":
                    print "\nThis Account is Closed.Please Enter an 'active' A/c No.\n"
                    raw_input("\nPress Enter To GO BACK")
                    self.transaction(cust_id)
                widam=float(raw_input("Enter Ammount To be withdrawn:    "))
                cur.execute("SELECT amount,wdraw_limit,account_type,net_amount from cust_bal where account_num=:1 ORDER BY transaction_date desc",{'1':account_num});
                x= cur.fetchone()
                if x is None:
                    print "\nEnter Valid A/c No.\n"
                else:
                    validate=True
            bal= x[3]
            account_type=x[2]
            wdraw_limit=x[1]
            if widam>bal :
                print "\nInsufficient balance in account\n"
                raw_input("\nPress Enter To GO BACK")
                self.transaction(cust_id)
            elif wdraw_limit>9:
                print "\nYou Have Crossed Maximum Withdrawl Limit\n"
                raw_input("\nPress Enter To GO BACK")
                self.transaction(cust_id)
            else:
                if wdraw_limit==0:
                    cur.execute("UPDATE cust_bal SET start_date=sysdate where account_num=:1", {'1': account_num});
                bal=x[3]
                net_amount=bal-widam
                print "\nYou have withdrawn Rs.",widam," from your account\n"
                cur.execute("INSERT INTO cust_bal (trans_id,account_num,account_type,amount,wdraw,net_amount,deposit,"
                            "transaction_date) VALUES(trans_id.nextval,:1,:2,:3,:4,:5,0,sysdate)",(account_num, account_type, bal, widam, net_amount))

                if x[2]=='savings':
                    cur.execute("UPDATE cust_bal SET wdraw_limit=:1 where account_num=:2", {'1': wdraw_limit + 1, '2': account_num});
                con.commit()
                raw_input("\nPress Enter To GO BACK")
                self.transaction(cust_id)

        ###################################################################################################################

        elif prompt == 5:
            os.system('cls')
            while validate <>True:
                try:
                    account_num1 = int(raw_input("Enter Account Number To Withdraw From: "))
                except:
                    print "\nEnter Integer Value\n"
                    raw_input("Press Enter To GO BACK\n")
                    self.transaction(cust_id)
                cur.execute("SELECT account_status from cust_account where account_num=:1 and cust_id=:2",{'1':account_num1,'2':cust_id})
                x=cur.fetchone()
                if x is None:
                    print "\nEnter Valid A/c No.\n"
                    raw_input("\nPress Enter To GO BACK\n")
                    self.transaction(cust_id)
                if x[0] =="closed":
                    print "\nThis Account is Closed.Please Enter an 'active' A/c No.\n"
                    raw_input("\nPress Enter To GO BACK\n")
                    self.transaction(cust_id)
                try:
                    account_num2 = int(raw_input("Enter Account Number to Transfer To: "))
                except:
                    print "\nEnter Integer Value\n"
                    raw_input("Press Enter To GO BACK\n")
                    self.transaction(cust_id)
                cur.execute("SELECT account_status from cust_account where account_num=:1",{'1':account_num2})
                x=cur.fetchone()
                if x is None:
                    print "\nEnter Valid A/c No.\n"
                    raw_input("\nPress Enter To GO BACK\n")
                    self.transaction(cust_id)
                if x[0] =="closed":
                    print "\nThis Account is Closed.Please Enter an 'active' A/c No.\n"
                    raw_input("\nPress Enter To GO BACK\n")
                    self.transaction(cust_id)
                cur.execute("SELECT amount,wdraw_limit,account_type,net_amount from cust_bal where account_num=:1 ORDER BY transaction_date desc",{'1':account_num1});
                x= cur.fetchone()
                cur.execute("SELECT amount,wdraw_limit,account_type,net_amount from cust_bal where account_num=:1 ORDER BY transaction_date desc",{'1':account_num2})
                y=cur.fetchone()
                if x is None:
                    print "\nEnter Your Valid A/c No.\n"
                elif y is None:
                    print "\nPlease Enter a Valid Transfer A/c No.\n"
                else:
                    validate=True
                    widam=float(raw_input("Enter Ammount To be Transfered:    "))

            bal1= x[3]
            bal2=y[3]
            account_type=x[2]
            wdraw_limit=x[1]
            if widam>bal1 :
                print "\nInsufficient balance in account\n"
                raw_input("Press Enter To GO BACK\n")
                self.transaction(cust_id)
            elif wdraw_limit>9:
                print "\nYou Have Crossed Maximum Withdrawl Limit\n"
                raw_input("\nPress Enter To GO BACK\n")
                self.transaction(cust_id)
            else:
                if wdraw_limit==0:
                    cur.execute("UPDATE cust_bal SET start_date=sysdate where account_num=:1", {'1': account_num1});
                bal1=x[3]
                net_amount1=bal1-widam
                net_amount2=bal2+widam
                print "\nYou have withdrawn Rs.",widam," from your account\n"
                cur.execute("INSERT INTO cust_bal (trans_id,account_num,account_type,amount,wdraw,net_amount,deposit,"
                            "transaction_date) VALUES(trans_id.nextval,:1,:2,:3,:4,:5,0,sysdate)",(account_num1, account_type, bal1, widam, net_amount1))

                cur.execute(
                    "INSERT INTO cust_bal (trans_id,account_num,account_type,amount,deposit,net_amount,wdraw,transaction_date) "
                    "VALUES(trans_id.nextval,:1,:2,:3,:4,:5,0,sysdate)", (account_num2, account_type, bal2, widam, net_amount2))

                if x[2]=='savings':
                    cur.execute("UPDATE cust_bal SET wdraw_limit=:1 where account_num=:2", {'1': wdraw_limit + 1, '2': account_num1});
                con.commit()
                raw_input("\nPress Enter To GO BACK\n")
                self.transaction(cust_id)


        ###################################################################################################################


        elif prompt == 6:
            os.system('cls')
            while validate <>True:
                try:
                    account_num = int(raw_input("\nEnter Account Number: "))
                    start_date=str(raw_input("\nEnter Start date in format:dd/mm/yyyy: "))
                    end_date = str(raw_input("\nEnter End date in format:dd/mm/yyyy: "))
                except:
                    print "\nEnter Proper Value\n"
                    raw_input("Press Enter To GO BACK\n")
                    self.transaction(cust_id)
                cur.execute("SELECT to_date(transaction_date,'dd/mm/yyyy'),wdraw,deposit,net_amount from cust_bal where account_num=:1 and "
                            "transaction_date between to_date(:2,'dd/mm/yyyy') and to_date(:3,'dd/mm/yyyy') ORDER BY "
                            "transaction_date desc",{'1':account_num,'2':start_date,'3':end_date});
                x= cur.fetchall()

                if len(x)==0:
                    print "No Data Retrieved.Check if  A/c No is valid OR date format is As REQUIRED"
                else:
                    validate=True
            print "\n***********************************************************\n"
            print " _________________________________________________________"
            print "| Transaction Date |    Debit   |   Credit   |   Amount   |"
            print "|   (yy-mm-dd)     |            |            |            |"
            print "|__________________|____________|____________|____________|"
            for i in x:
                date=str(i[0])
                print "| ",repr(date[2:11]).rjust(14)," | ",repr(i[1]).rjust(8)," | ",repr(i[2]).rjust(8)," | ",repr(i[3]).rjust(8)," |"
            print "|__________________|____________|____________|____________|"


            print "\n***********************************************************\n"
            raw_input("\nPress Enter To GO BACK\n")
            self.transaction(cust_id)

        ###################################################################################################################

        elif prompt==7:
            os.system('cls')
            try:
                 account_num=int(raw_input("Enter A/c No. To be Closed: "))
            except:
                print "\nEnter Integer Value\n"
                raw_input("Press Enter To GO BACK!!")
                self.transaction(cust_id)
            cur.execute("SELECT account_status,account_type from cust_account where account_num=:1", {'1': account_num})
            x = cur.fetchone()
            if x is None:
                print "\nAccount Does not Exists.Please Enter a Valid A/c No.\n"
                raw_input("\nPress Enter To GO BACK\n")
                self.transaction(cust_id)
            elif x[0] == "closed":
                print "\nThis Account is Already Closed.Please Enter an 'active' A/c No.\n"
                raw_input("\nPress Enter To GO BACK\n")
                self.transaction(cust_id)
            elif x[1] =='loan' or x[1] == 'fd':
                print "\nThis Account Cannot be closed It is LOAN/FD account\n"
                raw_input("\nPress Enter To GO BACK\n")
                self.transaction(cust_id)
            cur.execute("SELECT net_amount from cust_bal where account_num=:1 ORDER BY transaction_date desc",{'1':account_num})
            x=cur.fetchone()[0]
            print "\nAmount :",x," will be sent to Your Address.\n"
            cur.execute("UPDATE cust_account set account_status='closed',date_closed=sysdate where account_num=:1",{'1':account_num})
            con.commit()
            raw_input("\nPress Enter To GO BACK\n")
            self.transaction(cust_id)
        ###################################################################################################################

        elif prompt == 8:
            os.system('cls')
            cur.execute("SELECT account_num FROM cust_account where cust_id=:1 and account_type='loan'", {'1': cust_id})
            x=cur.fetchone()
            if x is not None:
                print "\nYou already Have a LOAN with bank.\n***Your LOAN Account Nuber is: ",x[0],"***\n"
                raw_input("\nPress Enter To GO BACK\n")
                self.transaction(cust_id)

            cur.execute("SELECT account_num FROM cust_account where cust_id=:1 and account_type='savings'",{'1':cust_id})
            x=cur.fetchone()
            if x is None:
                print "\nPlease Open A Savings Account First.\n"
            else:
                cur.execute("SELECT net_amount from cust_bal where account_num=:1 ORDER BY transaction_date desc",{'1':x[0]})
                savings=cur.fetchone()[0]
                cur.execute("SELECT last_number FROM user_sequences WHERE sequence_name = 'AC'")
                account_num = cur.fetchone()[0]
                while validate <>True:
                    amount=float(raw_input("Enter Amount to be Needed For LOAN:"))
                    if amount <=0 or amount%1000 <> 0 or amount>(2*savings):
                        print "\nEnter valid Amount.(Please check that:\nIt is a positive number\nIt is a multiple of " \
                              "1000\nIt Does not exceed (2*Your Saving Account Balance)\nYour Saving Account Balance is:  " \
                              "",savings
                    else:
                        validate=True
                while validate <>False:
                    term=int(raw_input("Enter term of Deposit(in Months): "))
                    if term <=0:
                        print "\nEnter Valid Months.\n"
                    else:
                        validate=False
                cur.execute("INSERT INTO cust_account(account_num,cust_id,account_type) VALUES(ac.nextval,:1,'loan')",{'1':cust_id})
                cur.execute("INSERT INTO cust_fd VALUES(:1,:2,:3)", (account_num,amount,term))
                con.commit()
                print "\n***Please Note You LOAN Account Number: ",account_num,"***\n"
            raw_input("\nPress Enter To GO BACK\n")
            self.transaction(cust_id)
        ###################################################################################################################

        elif prompt == 9:
            os.system('cls')
            cur.execute("SELECT account_num,account_type from cust_account where cust_id=:1 and account_status!='closed'",{'1':cust_id})
            x=cur.fetchall()
            print "\n***********************************************************"

            for i in x:
                print "A/c No.: "+str(i[0])+"  Type:  "+str(i[1])
            print "***********************************************************\n"
            raw_input("\nPress Enter To GO BACK\n")
            self.transaction(cust_id)
        ###################################################################################################################

        elif prompt == 0:
            print "\nThank You\n"
            bankMenu()

        ###################################################################################################################


        else:
            os.system('cls')
            print("\nYou have pressed the wrong key, please try again\n")
            raw_input("\nPress Enter To GO BACK\n")
            self.transaction(cust_id)

        ###################################################################################################################
            
    def login(self):
        os.system('cls')
        try:
            cust_id = int(raw_input("User Id: "))
            passwd = raw_input("Password: ")
        except:
            print "Enter Valid Credentials"
            raw_input("\nPress Enter!")
            self.login()
        passwd=b64encode(passwd)
        cur.execute("SELECT * from cust_info where cust_id=:1 and passwd=:2",(cust_id,passwd))
        x=cur.fetchone()
        if x is not None:
            if x[6]=="closed":
                print "This Account has been closed.Please Contact Branch Administartor"
                sys.exit()
        try:
            cur.execute("SELECT attempts from cust_info where cust_id=:1",{'1':cust_id})
            y=cur.fetchone()
            attempts=y[0]
        except:
            print "No such User Exists.Please Enter a Valid User Id"
            raw_input("\nPress Enter!")
            self.login()
        if x is None:
            print "Login Failure Please Retry "
            if attempts<2 and attempts>=0:
                attempts+=1
                print "\n\nAttempts Remaining",3-attempts
                cur.execute("UPDATE cust_info SET attempts=:1 WHERE cust_id=:2",{'1':attempts,'2':cust_id})
                con.commit()
                raw_input("\nPress Enter!")
                self.login()
            else:
                print "\nAccount Locked Please contact Administrator!!\n"
                return 0;
        else:
            #print x[5]
            if x[5]==2:
                print "\nAccount Locked Please Contact Branch Administrator!!\n"
                return 0;
            print "\nLogin Successful!\n"
            cur.execute("UPDATE cust_info SET attempts=:1 WHERE cust_id=:2", {'1': 0, '2': cust_id})
            con.commit()
            self.transaction(cust_id)

        try:
            con.close()
        except:
            pass

    def create_tables(self):
        try:
            cur.execute("CREATE SEQUENCE id START WITH 1000 INCREMENT BY 1 NOCACHE NOCYCLE")
        except cx.DatabaseError as e:
            pass
        try:
            cur.execute("CREATE SEQUENCE trans_id START WITH 1000 INCREMENT BY 1 NOCACHE NOCYCLE")
        except cx.DatabaseError as e:
            pass
        try:
            cur.execute("CREATE SEQUENCE ac START WITH 1786 INCREMENT BY 1 NOCACHE NOCYCLE")
        except cx.DatabaseError as e:
            pass
        try:
            cur.execute("CREATE TABLE  cust_info ( cust_id int PRIMARY KEY, first_name varchar(50) NOT NULL, last_name "
                        "varchar(50) NOT NULL, passwd varchar(50) NOT NULL,attempts int default 0,house_no int NOT NULL, "
                        "city varchar(50) NOT NULL,state varchar(20) NOT NULL, zip numeric(6) NOT NULL)")
        except:
            #print e
            pass
        try:
            cur.execute("CREATE TABLE  cust_account (account_num int PRIMARY KEY,cust_id int NOT NULL,account_type varchar(8),"
                        "account_status varchar(10) default 'active',date_closed date, CONSTRAINT fk_cust FOREIGN KEY ("
                        "cust_id) REFERENCES cust_info(cust_id))")
        except:
            #print e
            pass
        try:
            cur.execute("CREATE TABLE cust_bal(account_num int NOT NULL,trans_id int PRIMARY KEY,account_type varchar(8) NOT NULL,amount float(8) "
                        "DEFAULT 0.0,wdraw float(8) DEFAULT 0.0,deposit float(8) DEFAULT 0.0,net_amount float(8) DEFAULT "
                        "0.0,wdraw_limit int default 0,start_date date,transaction_date date,constraint fkey1 foreign "
                        "key(account_num) references cust_account(account_num))")
        except cx.DatabaseError as e:
            #print e
            pass
        try:
            cur.execute("CREATE TABLE cust_fd(account_num int NOT NULL,amount float(8) NOT NULL,term int NOT NULL,"
                        "CONSTRAINT fkey2 FOREIGN KEY(account_num) REFERENCES cust_account(account_num))")
        except cx.DatabaseError as e:
            #print e
            pass
        finally:
            pass

    def register(self):
        os.system('cls')
        amount = 0
        deposit=0
        net_amount=0
        flag = 0
        validate=False
        self.create_tables()
        first_name = raw_input("First name: ")
        last_name = raw_input("Last name: ")
        while validate <> True:
            passwd = raw_input("Password: ")
            if len(list(passwd))<8:
                print "Enter 8 characters minimum"
            else:
                passwd = b64encode(passwd)
                validate=True
        house_no = int(raw_input("House No.: "))
        city = raw_input("City: ")
        state = raw_input("State: ")
        while validate!=False:
            pin = int(raw_input("Zip: "))
            if len(list(str(pin))) != 6:
                print "Enter Valid 6 digit Zip"
            else:validate=False
        cur.execute("SELECT cust_id,first_name,last_name,house_no FROM cust_info where first_name=:1 and last_name=:2",{'1':first_name,'2':last_name})
        x = cur.fetchall()
        if len(x) == 0:
            flag = 1
        else:
            for i in x:
                a = i[3]
                if a == house_no:
                    print "User Already Exists"
                    raw_input("\nPress Enter To GO BACK !")
                    flag = 2
                    return flag
            if flag == 0:
                flag = 1
        if flag == 1:
            cur.execute("SELECT last_number FROM user_sequences WHERE sequence_name = 'ID'")
            cust_id = cur.fetchone()[0]
            cur.execute(
                "INSERT INTO cust_info (cust_id,first_name,last_name,passwd,house_no,city,state,zip) VALUES(id.nextval,:1,:2,:3,:4,:5,:6,:7)",
                (first_name, last_name, passwd,house_no, city, state, pin))
            con.commit()
            print "Successful Registration *** Please Note Down Your User Id: " + str(cust_id) + " ***"
            raw_input("\nPress Enter To LOGIN !")
            self.login()



#This function will be called at the starting of program and displays Bank Menu
def bankMenu():
    os.system('cls')
    bk = Bank() #Creating an Object of class Bank , bk is reference which points to that object
    try: #Start_Menu
        prompt = int(raw_input("""1. Sign Up (New Customer)\n""" +
                               """2. Sign In (Existing Customer)\n""" +
                               """3. Admin Sign In\n""" +
                               """4. Quit\n"""))
    except:
        os.system('cls')
        print "\nEnter Valid Input"
        raw_input("\nPress Enter to GO Back")
        bankMenu()
    if prompt == 1:
        # Creates a new customer profile using register() function
        x = bk.register()
        if x == 2:
            bankMenu()
        bankMenu()
    elif prompt == 2:
        x = bk.login() #Customer login point , Calls the login() function
        if x == 0:
            bankMenu()
    elif prompt == 3:
        os.system('cls')
        try:
            username=raw_input("\nUsername: ")
            password=raw_input("Password: ")
        except:
            print "\nEnter Valid Credentials"
            bankMenu()
        if username=='bank' and password=='vishal':
            bk.admin_menu() #strict access for admin
        else:
            print "\nInvalid Credentials.Please Retry"
            raw_input("\nPress Enter to go to Main Menu")
            bankMenu()
    elif prompt == 4:
        sys.exit("Thank You")
    else:
        print "\nYou have pressed the wrong key, please try again\n"
        bankMenu()


bankMenu() #starting point of program
