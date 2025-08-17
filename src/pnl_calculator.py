import os
import pandas as pd

class Pnl_Calculator:

    def __init__(self, directory: str):
        self.directory = directory
        self.csv_files = self.find_csv_files(directory)

    def find_csv_files(self, directory: str):
        csv_files = []
        if not os.path.exists(directory):
            os.makedirs(directory)
            return csv_files
        for root, dirs, files in os.walk(directory):
            for file in files:
                if file.endswith('.csv'):
                    csv_files.append(file)
        return csv_files

    def update_csv_with_profit_change(self, date: str, csv_file: str, balance: float, net_deposits: float):

        if not csv_file.endswith('.csv'):
            csv_file += '.csv'

        if csv_file in self.csv_files:
            df = pd.read_csv(f"{self.directory}/{csv_file}")
        else:
            df = pd.DataFrame(columns=["date","balance", "net deposits", "profit", "profit change", "settled"])
            self.csv_files.append(csv_file)

        profit = balance - net_deposits

        if not df.empty and df["settled"].any():
            last_settled_profit = df.loc[df["settled"] == True, "profit"].iloc[-1]
        else:
            last_settled_profit = 0

        profit_change = profit - last_settled_profit

        new_row = {
            "date": date,
            "balance": round(balance, 2),
            "net deposits": round(net_deposits, 2),
            "profit": round(profit, 2),
            "profit change": round(profit_change, 2),
            "settled": False
        }

        df = pd.concat([df, pd.DataFrame([new_row])], ignore_index=True)
        df.to_csv(f"{self.directory}/{csv_file}", index=False)

        return profit_change

    def report_latest_profit_change_and_commission(self, commission_ratio: float = 0.5):
        profit_change = 0
        for csv_file in self.csv_files:
            if os.path.exists(f"{self.directory}/{csv_file}"):
                df = pd.read_csv(f"{self.directory}/{csv_file}")
                if not df.empty and "profit change" in df.columns:
                    #check if balance has been settled
                    if df["settled"].iloc[-1] == False:
                        latest_profit_change = df["profit change"].iloc[-1]
                        profit_change += latest_profit_change
        print(f"Total unsettled profit across all bookies: {profit_change}")
        print(f"Total commission (at {commission_ratio * 100}%): {profit_change * commission_ratio}")

    def settle_profit(self, csv_file: str):
        if os.path.exists(f"{self.directory}/{csv_file}"):
            df = pd.read_csv(f"{self.directory}/{csv_file}")
            if not df.empty:
                df["settled"] = True
                df.to_csv(f"{self.directory}/{csv_file}", index=False)
                print(f"Settled all rows in {csv_file}")
            else:
                print(f"No data to settle in {csv_file}")
        else:
            print(f"{csv_file} does not exist.")

    
