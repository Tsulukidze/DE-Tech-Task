import logging
import logging.config
import yaml
import pandas as pd

from genereta import (
    safe_json_parse,
    drop_missing_values,
    calculate_claims_for_last_180,
    calculate_day_sinlastloan,
    calculate_disb_bank_loan_wo_tbc,
    total_contracts,
    count_by_bank,
    select_columns,
    total_loan_summa
)

# Load logging configuration from the YAML file
with open('config/logging_config.yaml', 'r') as f:
    logging_config = yaml.safe_load(f)

logging.config.dictConfig(logging_config)
logger = logging.getLogger(__name__)


def run():
    df = pd.read_csv('data/data.csv')

    # Apply the function to the 'contracts' column to handle invalid JSON
    df['contracts'] = df['contracts'].apply(safe_json_parse)


    df = drop_missing_values(df=df)


    df['tot_claim_cnt_l180d'] = df.apply(calculate_claims_for_last_180, axis=1)

    df['disb_bank_loan_wo_tbc'] = df['contracts'].apply(calculate_disb_bank_loan_wo_tbc)

    df['day_sinlastloan'] = df.apply(calculate_day_sinlastloan, axis=1)

    # additional calculations

    df['num_contracts'] = df['contracts'].apply(total_contracts)

    df['bank_counts'] = df['contracts'].apply(count_by_bank)

    df['total_loan_summa'] = df['contracts'].apply(total_loan_summa)


    df = select_columns(df=df)

    df.to_csv('reports/contract_features.csv', index=False)


if __name__ == "__main__":
    run()