# Profit Tracker

This is a command-line tool to track profits and losses from different sources, calculating unsettled profits and potential commissions.

# Required Modules
- Pandas


## How it works

The tool maintains CSV files in the `pnl_histories` directory. Each file represents a separate account or "bookie".The tool can:
- Update an account with a new balance and net deposits, calculating the profit change.
- Report the total unsettled profit across all accounts.
- Settle all outstanding profit changes.

## CSV File Structure

Each CSV file in the `pnl_histories` directory has the following columns:

- **balance**: The current balance of the account.
- **net deposits**: The total amount of money deposited into the account minus any withdrawals.
- **profit**: The total profit, calculated as `balance - net deposits`.
- **profit change**: The change in profit since the last settled transaction.
- **settled**: A boolean value (`True` or `False`) indicating whether this row has been settled.

## Usage

The main script to interact with the profit tracker is `src/main.py`.

### Update PnL

To update the profit and loss for a specific account, use the `-u` or `--update` flag. This requires you to provide the csv file name, the current balance, and the net deposits.

```bash
python -m src.main -u -c <bookie_name>.csv -b <balance> -nd <net_deposits>
```

**Example:**
```bash
python -m src.main -u -c betfair.csv -b 1050 -nd 1000
```
This command will add a new entry to `pnl_histories/betfair.csv` with the new balance and calculate the profit change since the last settled transaction.

### Report Unsettled PnL

To see the total unsettled profit across all your accounts, use the `-r` or `--report` flag.

```bash
python -m src.main -r
```
This will scan all CSV files in `pnl_histories` and sum up the latest profit changes that have not been settled. It will also show the calculated commission.

### Settle Profits

To mark all unsettled profits as settled, use the `-s` or `--settle` flag. This is typically done after you have been paid out.

```bash
python -m src.main -s
```
This will go through all CSV files and mark the final row as settled. The next time you update, the profit change will be calculated from this new settled point.

You can also combine settling with updating:
```bash
python -m src.main -u -c ladbrokes.csv -b 210 -nd 200 -s
```
This will first update `ladbrokes.csv` and then settle the profits for all accounts.
