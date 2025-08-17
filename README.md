# Profit Tracker

This is a command-line tool to track profits and losses from different sources, calculating unsettled profits and potential commissions.All you need to add are the current balances and net deposits for each betting site every time commission is requested. Possibly saving you time if you can figure out how to use this ugly mess.

# Required Modules
- Pandas


## How it works

The tool maintains CSV files in the `pnl_histories` directory. Each file represents a separate account or "bookie".The tool can:
- Update an account with a new balance and net deposits, calculating the profit change.
- Report the total unsettled profit across all accounts.
- Settle all outstanding profit changes.

## CSV File Structure

Each CSV file in the `pnl_histories` directory has the following columns:

- **date**: The date of the entry.
- **balance**: The current balance of the account.
- **net deposits**: The total amount of money deposited into the account minus any withdrawals.
- **profit**: The total profit, calculated as `balance - net deposits`.
- **profit change**: The change in profit since the last settled transaction.
- **settled**: A boolean value (`True` or `False`) indicating whether this row has been settled.

## Usage

The main script to interact with the profit tracker is `main.py`.

### Update PnL

To update the profit and loss for a specific account, use the `-u` or `--update` flag. This requires you to provide the csv file name, the current balance, the net deposits and the date. You can also optionally add any staked amounts that are not yet reflected in the balance.

```bash
python main.py -u -c <bookie_name>.csv -b <balance> -nd <net_deposits> -d <date> -sk <stake1> <stake2> ...
```

**Example:**
```bash
python main.py -u -c betfair.csv -b 1050 -nd 1000 -d 2025-08-17 -sk 25 10
```
This command will add a new entry to `pnl_histories/betfair.csv` with the new balance (plus the sum of stakes) and calculate the profit change since the last settled transaction. In this example, the balance used for calculation will be 1085 (1050 + 25 + 10).

### Report Unsettled PnL

To see the total unsettled profit across all your accounts, use the `-r` or `--report` flag.

```bash
python main.py -r
```
This will scan all CSV files in `pnl_histories` and sum up the latest profit changes that have not been settled. It will also show the calculated commission.

### Settle Profits

To mark all unsettled profits as settled, use the `-s` or `--settle` flag. This is typically done after you have been paid out.

```bash
python main.py -s
```
This will go through all CSV files and mark the final row as settled. The next time you update, the profit change will be calculated from this new settled point.

You can also combine settling with updating:
```bash
python main.py -u -c ladbrokes.csv -b 210 -nd 200 -d 2025-08-17 -s
```
This will first update `ladbrokes.csv` and then settle the profits for all accounts.
