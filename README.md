# Retail Customer Behavior

Short description

- **Project:** Retail-Customer-Behavior
- **Purpose:** Clean and transform customer shopping behavior data for analysis.

Data

- **Source file:** Data/customer_shopping_behavior.csv
- **Output:** output_data/customer_shopping_behavior_cleaned.csv

Requirements

- Python 3.8+
- pandas
- numpy

Install dependencies:

```
python -m pip install pandas numpy
```

Run

From the repository root:

```
python Script/Script.py
```

Notes

- The script normalizes column names, fills missing `review_rating` by category median, derives `age_group`, and converts purchase frequency to days.
- The script now creates the `output_data` folder if it doesn't exist and writes the cleaned CSV to `output_data/customer_shopping_behavior_cleaned.csv`.
- If you encounter a permissions error writing to `output_data`, either run the script with elevated privileges or fix folder ownership/ACLs. Example (run in elevated PowerShell): 

```
takeown /F "C:\Users\sraja\Documents\GitHub\Retail-Customer-Behavior\output_data" /R /D Y
icacls "C:\Users\sraja\Documents\GitHub\Retail-Customer-Behavior\output_data" /grant "%USERNAME%:F" /T
```

Contact

- Open an issue or edit this README with improvements or additional usage notes.
