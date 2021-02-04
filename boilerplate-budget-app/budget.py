class Category:

  def __init__(self,name):
    self.name = name
    self.ledger = []
      
  def get_balance(self):
    balance = 0
    for transaction in self.ledger:
      balance += transaction['amount']
    return balance  
        
  def deposit(self,amount,description=""):
    self.ledger.append({"amount":amount, "description":description})
        
  def withdraw(self,amount,description=""):
    if self.check_funds(amount) == True:
      self.ledger.append({"amount":-amount, "description":description})
      return True
    else:
      return False
        
  def transfer(self,amount,to_category):
    if self.check_funds(amount) == True:
      self.withdraw(amount,f'Transfer to {to_category.name}')
      to_category.deposit(amount,f'Transfer from {self.name}')
      return True
    else:
      return False

  def check_funds(self,amount):
    if self.get_balance() >= amount:
      return True
    else:
      return False  

  def __str__(self):  
    table = self.name.center(30,'*')
    
    for transaction in self.ledger:
      description = transaction['description'][:23].ljust(23)
      amount = ("{:.2f}".format(transaction['amount'])).rjust(7)
      table += f'\n{description}{amount}'

    table += f'\nTotal: {self.get_balance()}'
    return table

def create_spend_chart(categories):
  chart = 'Percentage spent by category'

  totals = [0 for budget in categories]
  category_names = [budget.name for budget in categories]
  
  i = 0
  for budget in categories:
    for transaction in budget.ledger:
      if transaction['amount'] < 0:
        totals[i] += transaction['amount']
    i += 1

  percentages = [((total/sum(totals))*100) for total in totals]
  percentages_zipped = zip(category_names,percentages)
  percentages_categorised = {k:v for (k,v) in percentages_zipped}

  vert_axis = [num for num in range(100,-1,-10)]

  i = 0

  for line in range(12 + len(max(percentages_categorised.keys(), key=len)) + 1):
    if line < 11:
      chart += '\n' + (str(vert_axis[line])).rjust(3) + '|'
      
      for category in percentages_categorised.keys():
        if float(percentages_categorised[category]) > vert_axis[line]:
          chart += ' o '
        else:
          chart += '   '
      chart += ' '    

    if line == 12:
      chart += '\n    ' + ('-' * ((3 * len(percentages_categorised.keys())) + 1))

    if line > 12:
      chart += '\n    '
      for category in percentages_categorised.keys():
        if i < len(category):
          chart += ' ' + category[i] + ' '
        else:
          chart += '   ' 
      chart += ' ' 
      i += 1    
  
  return chart         