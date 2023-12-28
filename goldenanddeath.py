import yfinance as yf
from backtesting import Backtest, Strategy
from backtesting.lib import crossover


# Define strategy class
class GoldenDeathCross(Strategy):
    def __init__(self, short_ma, long_ma):
        self.short_ma = short_ma
        self.long_ma = long_ma

    def next(self):
        if crossover(self.data.Close, self.short_ma) and crossover(self.short_ma, self.long_ma):
            self.buy()
        elif crossover(self.long_ma, self.short_ma):
            self.sell()


# Define function to run backtest and print metrics
def run_backtest(ticker):
    # Download historical price data using yfinance
    ohlcv = yf.download(ticker, start='2010-01-01', end='2022-04-03')
    close = ohlcv['Close']

    # Define short-term and long-term moving averages
    short_ma = close.rolling(window=50).mean()
    long_ma = close.rolling(window=200).mean()

    # Create instance of strategy and backtest
    strategy = GoldenDeathCross(short_ma, long_ma)
    bt = Backtest(close, strategy, cash=100000, commission=0.001)
    bt.run()

    # Calculate metrics
    total_trades = bt.total_trades
    win_trades = bt.total_wins
    loss_trades = bt.total_losses
    win_pct = bt.percent_profitable
    loss_pct = bt.percent_unprofitable
    avg_win = bt.average_win
    avg_loss = bt.average_loss
    total_return = bt.returns[-1] * 100
    end_principal = bt.end_principal
    total_gain = end_principal - bt.starting_cash
    ann_return = bt.annual_return
    max_drawdown = bt.max_drawdown * 100
    calmar = ann_return / abs(max_drawdown)

    # Print metrics
    print(f'Total Trades: {total_trades}')
    print(f'Win Trades: {win_trades} ({win_pct:.2f}%)')
    print(f'Loss Trades: {loss_trades} ({loss_pct:.2f}%)')
    print(f'Average Win: {avg_win:.2f}%')
    print(f'Average Loss: {avg_loss:.2f}%')
    print(f'Total Return: {total_return:.2f}%')
    print(f'End Principal: {end_principal:.2f}')
    print(f'Total Gain: {total_gain:.2f}')
    print(f'Avg Annual Return: {ann_return * 100:.2f}%')
    print(f'Max Drawdown: {max_drawdown:.2f}%')
    print(f'Calmar: {calmar:.2f}')


# Example usage
run_backtest("RELIANCE.NS")


