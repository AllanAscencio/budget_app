class Category:
    def __init__(self, name):
        self.name = name
        print("Init Category:", self.name)
        self.ledger = []
        self.total = 0

    def __repr__(self):
        header = self.name.center(30, "*") + "\n"
        ledger = ""
        for item in self.ledger:
            # format description and amount
            line_description = "{:<23}".format(item["description"])
            line_amount = "{:>7.2f}".format(item["amount"])
            # Truncate ledger description and amount to 23 and 7 characters respectively
            ledger += "{}{}\n".format(line_description[:23], line_amount[:7])
        total = "Total: {:.2f}".format(self.total)
        return header + ledger + total

    def deposit(self, user_deposit: int, deposit_reason=""):
        self.total += user_deposit
        self.ledger.append({'amount': user_deposit, "description": deposit_reason})

    def withdraw(self, amount_withdrawn: float or int, withdrawn_motive=""):
        withdraw_allowed = self.check_funds(amount_withdrawn)

        if withdraw_allowed:
            self.total -= amount_withdrawn
            self.ledger.append({"amount": -amount_withdrawn, "description": withdrawn_motive})

        return withdraw_allowed

    def get_balance(self):
        return self.total

    def transfer(self, transfer_money: int, budget_category):
        transfer_succesful = self.check_funds(transfer_money)

        if transfer_succesful:
            self.withdraw(transfer_money, f"Transfer to {budget_category.name}")
            budget_category.deposit(transfer_money, f"Transfer from {self.name}")

        return transfer_succesful

    def check_funds(self, amount):
        if amount > self.total:
            return False
        return True


def create_spend_chart(categories):
    spent_amounts = []
    # Get total spent in each category
    for category in categories:
        spent = 0
        for item in category.ledger:
            if item["amount"] < 0:
                spent += abs(item["amount"])
        spent_amounts.append(round(spent, 2))

    # Calculate percentage rounded down to the nearest 10
    total = round(sum(spent_amounts), 2)
    spent_percentage = list(map(lambda amount: int((((amount / total) * 10) // 1) * 10), spent_amounts))

    # Create the bar chart substrings
    header = "Percentage spent by category\n"

    chart = ""
    for value in reversed(range(0, 101, 10)):
        chart += str(value).rjust(3) + '|'
        for percent in spent_percentage:
            if percent >= value:
                chart += " o "
            else:
                chart += "   "
        chart += " \n"

    footer = "    " + "-" * ((3 * len(categories)) + 1) + "\n"
    descriptions = list(map(lambda category: category.name, categories))
    max_length = max(map(lambda name: len(name), descriptions))
    descriptions = list(map(lambda name: name.ljust(max_length), descriptions))
    for x in zip(*descriptions):
        footer += "    " + "".join(map(lambda s: s.center(3), x)) + " \n"

    return (header + chart + footer).rstrip("\n")