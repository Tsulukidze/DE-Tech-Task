import json
import logging
import pandas as pd


from datetime import datetime, timedelta


logger = logging.getLogger(__name__)



# Function to safely parse the JSON column
def safe_json_parse(json_str):
    try:
        # If the value is None, return None
        if pd.isna(json_str):
            return None
        
        # load the JSON
        return json.loads(json_str)
    
    except (json.JSONDecodeError, TypeError) as e:
        # If JSON parsing fails, log the error and return None
        # Log the first 100 characters of the invalid JSON
        logger.error(f"Invalid JSON encountered: {json_str[:100]}...") 
        return None


def clean_application_date(application_date):

    # Convert the application_date to datetime
    application_date = pd.to_datetime(application_date, errors='coerce')
    
    # Normalize the datetime (strip time and timezone info)
    application_date = application_date.normalize().strftime("%d.%m.%Y")
    
    application_date = datetime.strptime(application_date, "%d.%m.%Y")

    return application_date


def drop_missing_values(df):
    df = df.dropna()
    return df

    
# Function to calculate claims for the last 180 days
def calculate_claims_for_last_180(row):
    contracts=row['contracts']
    application_date = row['application_date']
    application_date = clean_application_date(application_date=application_date)

    if isinstance(contracts, dict):  # Case: Single contract (not a list)
        contracts = [contracts]  # Convert to list for processing
    
    cutoff_date = application_date - timedelta(days=180)
    claim_count = 0
    
    # Loop through the contracts and check each claim's date
    for contract in contracts:
        # make sure that , contract is a dictionary and has the claim_date key
        if isinstance(contract, dict):
            claim_date_str = contract.get('claim_date', None)
            if claim_date_str:
                try:
                    # Convert claim_date to a datetime object using format dd.mm.yyyy
                    claim_date = datetime.strptime(claim_date_str, '%d.%m.%Y')
                    if claim_date >= cutoff_date:
                        claim_count += 1
                except ValueError:
                    # In case of an invalid date format, log it and continue
                    logging.error(f"Invalid claim date format: {claim_date_str}")
                    continue

    # If no valid claims, return -3
    if claim_count == 0:
        return -3
    
    return claim_count


# Function to calculate the sum of disbursed bank loans excluding TBC loans
def calculate_disb_bank_loan_wo_tbc(contracts):    
    # If contracts is a single dictionary, convert it to a list for processing
    if not isinstance(contracts, list):
        contracts = [contracts]
        
    excluded_banks = ['LIZ', 'LOM', 'MKO', 'SUG', None]
    total_loan_exposure = 0
    
    has_valid_claims = False

    # Loop through the contracts and apply the necessary filters
    for contract in contracts:

        if isinstance(contract, dict):
            bank = contract.get('bank', None)
            loan_summa = contract.get('loan_summa', 0)
            contract_date = contract.get('contract_date', None)
            claim_id = contract.get('claim_id', None)

            # Check if the bank is not in the excluded list and the contract date is not null
            if bank not in excluded_banks and contract_date:
                try:
                    loan_summa = float(loan_summa) if isinstance(loan_summa, (int, float)) else 0
                    if loan_summa > 0:
                        total_loan_exposure += loan_summa

                    # valid claim_id case
                    if claim_id:
                        has_valid_claims = True

                except ValueError:
                    # Log invalid loan_summa and skip
                    logging.error(f"Invalid loan_summa format: {loan_summa} for contract ID: {contract.get('contract_id')}")
                    continue

    if not has_valid_claims:
        return -3

    # If no valid loans at all, return -1
    if total_loan_exposure == 0:
        return -1

    return total_loan_exposure


# Function to calculate the number of days since the last loan
def calculate_day_sinlastloan(row):
    contracts = row['contracts']
    application_date = row['application_date']

    application_date = clean_application_date(application_date=application_date)

    
    # If contracts is a single dictionary, convert it to a list for uniform processing
    if not isinstance(contracts, list):
        contracts = [contracts]
    
    valid_loans = []

    # Loop through the contracts and filter valid loans based on summa
    for contract in contracts:
        if isinstance(contract, dict):
            summa = contract.get('summa', None)
            contract_date = contract.get('contract_date', None)
            
            # Only consider loans where summa is not null and contract_date is present
            if summa and summa > 0 and contract_date:
                valid_loans.append((contract_date, summa))
    
    # If no valid loans are found, return -1
    if not valid_loans:
        return -1

    # Find the latest loan (max contract_date)
    latest_contract_date = max(valid_loans, key=lambda x: datetime.strptime(x[0], "%d.%m.%Y"))[0]
    
    # Convert latest_contract_date to datetime
    latest_contract_date = datetime.strptime(latest_contract_date, "%d.%m.%Y")
        
    # Calculate the difference in days between application_date and latest_contract_date
    days_since_last_loan = (application_date - latest_contract_date).days

    return days_since_last_loan

# Function to calculate total number of contracts
def total_contracts(contracts):
    return len(contracts) if contracts else 0

# Function to  count banks in contracts
def count_by_bank(contracts):

    if not isinstance(contracts, list):
        contracts = [contracts]

    bank_counts = {}
    for contract in contracts:
        bank = contract.get('bank', None)
        if bank:
            bank_counts[bank] = bank_counts.get(bank, 0) + 1
    # here dictionary also involves number of occurences for each bank
    # e.x  TBC : 3 ,  014: 6
    # for now we are just interested to see number of banks
    return len(bank_counts)


# Function to calculate total loan summa for all contracts
def total_loan_summa(contracts):

    if not isinstance(contracts, list):
        contracts = [contracts]

    total = 0
    for contract in contracts:
        loan_summa = contract.get('loan_summa', 0)
        if loan_summa and isinstance(loan_summa, (int, float)):
            total += loan_summa
    return total


def select_columns(df):
    columns = ["id","application_date","tot_claim_cnt_l180d","disb_bank_loan_wo_tbc",
               "day_sinlastloan", "num_contracts","bank_counts","total_loan_summa"]
    
    return df[columns]
