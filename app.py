
import csv

import requests
from flask import Flask, render_template, request, redirect

app = Flask(__name__)

response = requests.get("http://api.nbp.pl/api/exchangerates/tables/C?format=json")
data=response.json()
rates = data[0].get('rates')
rate_map = {}
for item in rates:
    print(item["code"])
    rate_map[item["code"]] = item



def get_codes():
    codes = []
    for data in rates:
        codes.append(data.get('code'))
    return sorted(codes)

codes = get_codes()

columns=['currency','code','bid','ask']

with open('rates.csv', 'w') as csvfile:
    fieldnames = columns
    writer = csv.DictWriter(csvfile, delimiter=';', fieldnames=fieldnames)
    writer.writeheader()
    writer.writerows(rates)

with open ("rates.csv") as filecsv:
    writer = csv.reader(filecsv,delimiter=';')
    for i in writer:
        pass


@app.route('/', methods=['GET'])
def index():
    return render_template("index.html")

@app.route('/calculator', methods=['GET'])
def calculator():
    return render_template("calculator.html", rates=rates)


@app.route('/calculator', methods=['POST'])
def calc():
    form = request.form
    code = form.get('rates', type=float)
    amount = form.get('amount', type=float)
    price = code*amount
    print(f"Koszt wymiany to : {price} złotych")
    print('\n')
    print("Dzięki za skorzystanie z kalkulatora, daj suba, okejke :)")
    return render_template("/response.html", price = price)


if __name__ == "__main__":
    app.run(debug=True)
