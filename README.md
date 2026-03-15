# Currency Converter for Alfred

Simple Alfred workflow to convert currencies. It displays the quote amounts for all tracked currencies relative to a given base and amount.

Exchange rates update every 15 minutes. 

## Features

- Add tracked currencies: `ccy add CODE`

- Convert: `ccy BASE_CODE [BASE_AMT] [QUOTE_CODE]`
  - `ccy CHF` → tracked currencies relative to CHF 1
  - `ccy JPY 5000` → tracked currencies relative to JPY 5000
  - `ccy HKD 78 USD` → USD relative to HKD 78

- Remove tracked currencies: `ccy CODE` (hold option to remove)

- Clear cache: `ccy clear`

- Reset workflow: `ccy reset`

## Notes

- Currency codes are case-insensitive.

- The AMOUNT parameter accepts shorthand and formatted inputs: k (thousand), m (million), b (billion), or comma-separated numbers (e.g., 1.5k, 2m, 3,000).

- Behavior for BASE:
  - If BASE is tracked, the workflow treats it as the base.
  - If BASE is not tracked, the workflow searches all supported currencies for BASE.
