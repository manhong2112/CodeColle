# coding: utf-8
import pickle
import os


class Account:
    def __init__(self, user_id=""):
        self.account = {}
        self.count = 0
        self.user_id = user_id
        if not os.path.isfile('account.db'):
            with open('account.db', 'wb') as db:
                pickle.dump(self.user_id, db)
                pickle.dump(self.account, db)
                pickle.dump(self.count, db)
        with open('account.db', 'rb') as db:
            try:
                self.user_id = pickle.load(db)
                self.account = pickle.load(db)
                self.count = pickle.load(db)
            except EOFError:
                pass

    def add_account(self, item, money):
        int(money)
        self.count += 1
        self.account[self.count] = str(now.date()) + "|" + money + "|" + item

    def check_money(self):
        total = 0
        for record_id in range(1, len(self.account) + 1):
            total += int(self.account[record_id].split("|")[1])

        print("== You have", total, "==")

    def list_account(self):
        print("Date\t\t$\t\tItem")
        for record_id in range(1, len(self.account) + 1):
            print(self.account[record_id].replace('|', "\t\t"))

    def close_account(self):
        with open('account.db', 'wb') as db:
            pickle.dump(self.user_id, db)
            pickle.dump(self.account, db)
            pickle.dump(self.count, db)
        print("Good Bye!")


def main():
    account = Account()
    account_func = {
        "1": lambda: account.add_account(input("Item > "), input("Money > ")),
        "2": account.check_money,
        "3": account.list_account
    }

    while True:
        print(">> # # # # # # # # # # # # # # #")
        print(">> Add record to account, input 1")
        print(">> Check your money, input 2")
        print(">> List the log of your account, input 3")
        print(">> If you want to exit, input 0")
        print(">> # # # # # # # # # # # # # # #")
        try:
            val = input("> ")
            account_func[val]()
        except KeyError:
            if val == "0":
                account.close_account()
                break
            print("E> Wrong Input")
        except ValueError:
            print("E> Wrong Value")


main()
