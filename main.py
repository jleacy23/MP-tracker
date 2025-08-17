import argparse
from src.pnl_calculator import Pnl_Calculator

def main():
    parser = argparse.ArgumentParser(description="script to update or report pnl")

    group = parser.add_mutually_exclusive_group()
    group.add_argument("-u", "--update", action="store_true", help="Update the CSV with new pnl")
    group.add_argument("-r", "--report", action="store_true", help="Report current unsettled pnl, and commission")

    parser.add_argument("-s", "--settle", action="store_true", help="Mark the row as settled")

    parser.add_argument("-c", "--csv_file", type=str, help="Path to the CSV file")
    parser.add_argument("-b", "--balance", type=float, help="Account balance")
    parser.add_argument("-nd", "--net_deposits", type=float, help="Net deposits")
    parser.add_argument("-d", "--date", type=str, help="Date for the PnL entry")

    args = parser.parse_args()

    pnl_calculator = Pnl_Calculator("pnl_histories")

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
        pnl_calculator.update_csv_with_profit_change(args.date, args.csv_file, args.balance, args.net_deposits)

    elif args.report:
        pnl_calculator.report_latest_profit_change_and_commission()

    if args.settle:
        for pnl in pnl_calculator.csv_files:
            pnl_calculator.settle_profit(pnl)

if __name__ == "__main__":
    main()