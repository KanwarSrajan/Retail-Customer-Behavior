from pathlib import Path
import sys
import pandas as pd
import numpy as np


def load_data(file_path):
    return pd.read_csv(file_path)


def normalize_columns(df):
    df.columns = df.columns.str.lower().str.replace(' ', '_', regex=False)
    # optional: remove parentheses characters in column names
    df.columns = df.columns.str.replace('(', '', regex=False).str.replace(')', '', regex=False)
    return df


def fill_review_rating_median(df):
    if 'review_rating' in df.columns and 'category' in df.columns:
        # ensure numeric
        df['review_rating'] = pd.to_numeric(df['review_rating'], errors='coerce')
        df['review_rating'] = df.groupby('category')['review_rating'].transform(lambda x: x.fillna(x.median()))
    return df


def main():
    repo_root = Path(__file__).resolve().parents[1]
    csv_path = repo_root / 'Data' / 'customer_shopping_behavior.csv'
    if not csv_path.exists():
        print(f"CSV not found at {csv_path}")
        sys.exit(1)

    df = load_data(csv_path)
    df = normalize_columns(df)

    # rename purchase amount column if present
    if 'purchase_amount_usd' in df.columns:
        df.rename(columns={'purchase_amount_usd': 'purchase_amount'}, inplace=True)
    if 'purchase_amount_(usd)' in df.columns:
        df.rename(columns={'purchase_amount_(usd)': 'purchase_amount'}, inplace=True)

    df = fill_review_rating_median(df)

    # create age_group column with three labels: young adults, middle aged, senior
    if 'age' in df.columns:
        df['age'] = pd.to_numeric(df['age'], errors='coerce')
        bins = [0, 34, 64, 200]
        labels = ['young adults', 'middle aged', 'senior']
        df['age_group'] = pd.cut(df['age'], bins=bins, labels=labels, right=True, include_lowest=True)
        df['age_group'] = df['age_group'].astype(object)
        df.loc[df['age'].isna(), 'age_group'] = 'unknown'

    # create purchase_frequency_days from frequency_of_purchases
    if 'frequency_of_purchases' in df.columns:
        freq = df['frequency_of_purchases'].astype(str).str.strip().str.lower()
        def freq_to_days(s):
            if pd.isna(s):
                return np.nan
            if 'daily' in s:
                return 1
            if 'weekly' in s:
                return 7
            if 'fortnight' in s or 'biweekly' in s or 'fortnightly' in s:
                return 14
            if 'monthly' in s or 'month' in s:
                return 30
            if 'quarter' in s:
                return 90
            if 'annual' in s or 'year' in s or 'annually' in s or 'yearly' in s:
                return 365
            # try to parse numbers like '2 per month' or '3/month'
            import re
            m = re.search(r"(\d+)\s*(per|/|per\s)\s*(month|year|week|day|quarter)", s) #regex (regular expression) to match patterns
            if m:
                n = int(m.group(1))
                unit = m.group(3)
                if 'day' in unit:
                    return max(1, round(1 / n))
                if 'week' in unit:
                    return round(7 / n)
                if 'month' in unit:
                    return round(30 / n)
                if 'year' in unit:
                    return round(365 / n)
            return np.nan

        df['purchase_frequency_days'] = freq.apply(freq_to_days)
    else:
        df['purchase_frequency_days'] = np.nan

    # write cleaned DataFrame into repository 'output_data' folder
    output_dir = repo_root / 'output_data'
    output_dir.mkdir(parents=True, exist_ok=True)
    out_file = output_dir / 'customer_shopping_behavior_cleaned.csv'
    df.to_csv(out_file, index=False, encoding='utf-8')


    # print('Shape:', df.shape)
    # print('\nInfo:')
    # df.info()
    # print('\nHead:')
    # print(df.head())


if __name__ == '__main__':
    main()
