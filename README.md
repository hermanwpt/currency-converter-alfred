# Currency Converter for Alfred

Simple Alfred workflow to convert currencies. Exchange rates update every 15 minutes.

Quick summary
- Add tracked currencies: ccy add CODE
- Convert: ccy BASE [AMOUNT] [QUOTE]
  - ccy CHF → tracked currencies relative to CHF 1
  - ccy JPY 5000 → tracked currencies relative to JPY 5000
  - ccy HKD 78 USD → USD relative to HKD 78
- Clear cache: ccy clear
- Reset workflow: ccy reset

Notes
- Currency codes are case-insensitive.
- Workflow prefers tracked (saved) currencies when matching; if matched, the matched saved currency is shown first.
- Amounts are shown with two decimal places and comma separators.
