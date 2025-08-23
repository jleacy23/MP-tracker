import argparse
from src.pnl_calculator import Pnl_Calculator

def main():
    parser = argparse.ArgumentParser(
        description="A command-line tool to track profits and losses from different sources.",
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog="""
Usage Examples:

To update the profit and loss for a specific account:
  python main.py -u -c <bookie_name>.csv -b <balance> -nd <net_deposits> -d <date>

To include staked amounts that are not yet reflected in the balance:
  python main.py -u -c betfair.csv -b 1050 -nd 1000 -d 2025-08-17 -sk 25 10

To see the total unsettled profit across all your accounts:
  python main.py -r

To mark all unsettled profits as settled:
  python main.py -s

To combine settling with updating:
  python main.py -u -c ladbrokes.csv -b 210 -nd 200 -d 2025-08-17 -s
""")

    group = parser.add_mutually_exclusive_group()
    group.add_argument("-u", "--update", action="store_true", help="Update the CSV with new pnl")
    group.add_argument("-r", "--report", action="store_true", help="Report current unsettled pnl, and commission")

    parser.add_argument("-s", "--settle", action="store_true", help="Mark the row as settled")

    parser.add_argument("-c", "--csv_file", type=str, help="Path to the CSV file")
    parser.add_argument("-b", "--balance", type=float, help="Account balance")
    parser.add_argument("-nd", "--net_deposits", type=float, help="Net deposits")
    parser.add_argument("-d", "--date", type=str, help="Date for the PnL entry")
    parser.add_argument("-sk", "--stakes", type=float, nargs = '+', help='Values of staked bets')

    args = parser.parse_args()

    pnl_calculator = Pnl_Calculator("pnl_histories")
    stake_sum = sum(args.stakes) if args.stakes else 0

    if args.update:
        missing = []
        if not args.csv_file:
            missing.append("--csv_file")
        if args.balance is None:
            missing.append("--balance")
        if args.net_deposits is None:
            missing.append("--net_deposits")
        if args.date is None:
            missing.append("--date")
        if missing:
            parser.error(f"{', '.join(missing)} required with --update")
        pnl_calculator.update_csv_with_profit_change(args.date, args.csv_file, args.balance + stake_sum, args.net_deposits)

    elif args.report:
        pnl_calculator.report_total_profit()
        pnl_calculator.report_latest_profit_change_and_commission()

    if args.settle:
        for pnl in pnl_calculator.csv_files:
            pnl_calculator.settle_profit(pnl)

if __name__ == "__main__":
    main()