import requests


class ApiData:
    response = requests.get('https://my.api.mockaroo.com/user.json?key=f3057d20')
    data = response.json()
    nombre = ''
    apellido = ''
    email = ''
    telefono = ''
    plate = ''
    street = ''
    zip = ''
    city = ''
    country = ''

    def __init__(self, num):
        self.num = num

    def assign_values(self):
        self.nombre = self.data[self.num]['first_name']
        self.apellido = self.data[self.num]['last_name']
        self.email = self.data[self.num]['email']
        self.telefono = self.data[self.num]['phone']
        self.plate = self.data[self.num]['plate']
        self.street = self.data[self.num]['street']
        self.zip = self.data[self.num]['zip']
        self.city = self.data[self.num]['city']
        self.country = self.data[self.num]['country']


# data = ApiData(1)
# data.assign_values()
# print(data.nombre)
# print(data.apellido)
# print(data.email)
# print(data.telefono)
# print(data.plate)
# data2 = ApiData(2)
# data2.assign_values()
# print(data2.nombre)
# print(data2.apellido)
# print(data2.email)
# print(data2.telefono)
# print(data2.plate)

