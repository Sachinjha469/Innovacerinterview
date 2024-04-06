class User:
    def __init__(self, user_id, name):
        self.user_id = user_id
        self.name = name
        self.owed_to = {}
        self.owes = {}

    def add_owed_amount(self, friend_id, amount):
        if friend_id in self.owed_to:
            self.owed_to[friend_id] += amount
        else:
            self.owed_to[friend_id] = amount

    def add_owes_amount(self, friend_id, amount):
        if friend_id in self.owes:
            self.owes[friend_id] += amount
        else:
            self.owes[friend_id] = amount


class Expense:
    def __init__(self, expense_id, payer_id, amount):
        self.expense_id = expense_id
        self.payer_id = payer_id
        self.amount = amount
        self.shares = {}

    def add_share(self, user_id, share_amount):
        self.shares[user_id] = share_amount


class ExpenseManager:
    def __init__(self):
        self.users = {}
        self.expenses = []

    def add_user(self, user_id, name):
        self.users[user_id] = User(user_id, name)

    def add_expense(self, expense_id, payer_id, amount, shares):
        expense = Expense(expense_id, payer_id, amount)
        for user_id, share_amount in shares.items():
            expense.add_share(user_id, share_amount)
            if user_id != payer_id:
                self.users[payer_id].add_owed_amount(user_id, share_amount)
                self.users[user_id].add_owes_amount(payer_id, share_amount)
        self.expenses.append(expense)

    def get_amount_owed_by_user(self, user_id):
        return self.users[user_id].owed_to

    def get_amount_owed_to_user(self, user_id):
        return self.users[user_id].owes


def main():
    manager = ExpenseManager()

    manager.add_user(1, "Ram")
    manager.add_user(2, "Shyam")
    manager.add_user(3, "Gyan")

    manager.add_expense(1, 1, 300, {2: 100, 3: 100})

    print("Amounts owed by each friend:")
    for user_id, amount in manager.get_amount_owed_by_user(1).items():
        user_name = manager.users[user_id].name
        print(f"User {user_id} owes Ram with username {user_name}: Rs.{amount}")

    print("\nAmounts Ram owes to each friend:")
    for user_id, amount in manager.get_amount_owed_to_user(1).items():
        user_name = manager.users[user_id].name
        print(f"Ram owes User {user_id} with username {user_name}: Rs.{amount}")
    if not manager.get_amount_owed_to_user(1).items():
      print(f"Ram doesn't owe any money to his friend.")


if __name__ == "__main__":
    main()
