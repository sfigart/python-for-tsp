import gspread
from oauth2client.service_account import ServiceAccountCredentials
import pprint

print("hello rom sharePrices.py")
# Simple script using GSpread to write the trading day of month
# for all the TSP share price history
# Reference article:
# https://medium.com/daily-python/python-script-to-edit-google-sheets-daily-python-7-aadce27846c0
# AWS Cloud 9 instance PIP commands
# pip3 install gspread --user
# pip3 install oauth2client --user
# pip3 install pandas --user

#Authorize the API
scope = [
    'https://www.googleapis.com/auth/drive',
    'https://www.googleapis.com/auth/drive.file'
    ]
file_name = 'client_key.json'
creds = ServiceAccountCredentials.from_json_keyfile_name(file_name,scope)
client = gspread.authorize(creds)

print("got creds")

pp = pprint.PrettyPrinter()

#sheet_name = "Sheet2"
sheet_name = "SharePrices"

#Fetch the sheet
sheet = client.open('TSP SharePrices').worksheet(sheet_name)
data = sheet.get_all_values()

# Initialize variables 
prior_month = ""
trading_day = 0
updates = []

# for each year / month / increment trading day of month counter
for row in range(len(data)):
    
    # skip header row
    if row == 0:
        continue
        
    year, month = data[row][1], data[row][2]
    
    if month != prior_month:
        trading_day = 1
        prior_month = month
        
    print("%2d %s/%s %2d" % (row, year, month, trading_day))
    
    # Save trading_day
    updates.append([trading_day])
    
    trading_day += 1

# Find the range
cell_ref = "D2:D" + str(len(data))

# Do the update en masse to avoid Google 420 Resource Exhausted limit
sheet.update(cell_ref, updates)
