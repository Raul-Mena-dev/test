import datetime
from time import strftime
from funciones.function import xpath_dispenser

# x = datetime.date.today()
# y = x + datetime.timedelta(days=10)
# x = x.strftime("%m %d %Y")

x = xpath_dispenser('dispenser')


print(x)
