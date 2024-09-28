
import csv

# Open the CSV file
with open('valid_guesses.csv', 'r') as file:
    reader = csv.reader(file)
    data = [row[0] for row in reader]

print(data)
