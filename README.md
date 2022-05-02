# Currency Converter for Alfred
This is a currency converter for alfred workflow. Exchange rate is updated every 15 mins.

## Commands available for this workflow:

1. ```currency add [currency]```
- Please use this command to add currencies you want to track.

2. ```cur [base cur] [base cur amount (optional)] [quote cur (optional)]```

- Case 1: ```cur CHF```
--> value of tracked currencies relative to CHF 1

- Case 2: ```cur JPY 5000```
--> value of tracked currencies relative to JPY 5000

- Case 3: ```cur HKD 78 USD```
--> value of USD relative to HKD 78

- Case 4: ```holding opt```
--> remove this tracked currency

3. ```currency clear```
- Clear cached data

4. ```currency reset```
- Reset this workflow

## TODO Bug Fix

- currency value does not round off to 2 d.p. when copied to clipboard
- autocomplete does not work as intended for case 3 (cur HKD 78 USD)
