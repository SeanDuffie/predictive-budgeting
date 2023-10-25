# predictive-budgeting

I need a way to manage my money that is more hands-off than manually creating excel sheets and guessing. This is the repository where I will explore my ideas for solutions to this.

# Setup/Installation/Usage

1. Clone from GitHub Repo
    ``` cmd
    git clone https://github.com/SeanDuffie/predictive-budgeting.git
    cd ./predictive-budgeting
    ```
2. Install the environment dependencies
    ``` cmd
    python -m pip install --upgrade pip
    pip install -r ./requirements.txt
    ```
3. Drop any new data entries into the database folder
4. Run main.py
5. Open the Flask Server in a browser at 127.0.0.1.
TODO: Make this more permanent with a port forward and noip.com?

# TODO

1. Budget
    - [x] Automatically read in CSV
    - [ ] Compare new CSV to existing database, compile non duplicates into a cumulative database.
    - [ ] Categorize expenses and incomes
    - [ ] Launch into a Flask Server for graphs and interactive data
        - [x] Pie Chart for how much in each category for both expenses and 
2. Stocks
    - [x] Use yfinance API to access stock data
    - [ ] Milestones to indicate potential causes of pattern changes
3. Loans
    - [ ] Amortization chart?