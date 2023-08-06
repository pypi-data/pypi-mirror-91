import numpy as np
from quantopian.algorithm import attach_pipeline, pipeline_output
from quantopian.pipeline import Pipeline
from quantopian.pipeline.data.builtin import USEquityPricing
# for pipeline
from quantopian.pipeline.factors import AverageDollarVolume, SimpleMovingAverage, Latest
from quantopian.pipeline.factors import CustomFactor, RSI
from quantopian.pipeline.data.quandl import cboe_vix
from quantopian.pipeline.data.quandl import cboe_vxv
from quantopian.pipeline.data.quandl import cboe_skew
import datetime
import pandas as pd


def handle_data(context, data):
    pass


def initialize(context):
    print("   **************  calling initialize **************  ")
    set_commission(commission.PerShare(cost=0.005))
    set_slippage(slippage.VolumeShareSlippage(volume_limit=0.025, price_impact=0.1))
    context.interval = 60  # every 10 minutes
    context.stop_loss = 0.5  # 0.5%
    context.stocks = symbols('SPY', 'DIA', 'QQQ', 'TLT')
    context.mark_for_close = []
    # for minute in range(60, 390, context.interval):
    #     schedule_function(sell_if_stop_loss_was_hit, date_rules.every_day(), time_rules.market_open(minutes=minute))

    schedule_function(rebalance, date_rules.every_day(), time_rules.market_open(minutes=1))


def before_trading_start(context, data):
    pass


def rebalance(context, data):
    try:
        prices = resample_minute_prices(context, data, 60, 2)
        for stock in context.stocks:
            gap = prices['open'][stock.symbol][1] - prices['close'][stock.symbol][0]
            gap_up = gap > 0
            gap_down = gap < 0
            if gap_up:
                order_target_percent(stock, 0.5)
            if gap_down:
                order_target(stock, 0)

    except:
        pass  # not today

def get_close_prices_as_list(window_size, prices, stock):
    close_prices = prices['close'].iloc[window_size - 2::window_size, :][stock]

    for index, el in list(close_prices.items()):
        if np.isnan(el):
            close_prices[index] = prices['close'].loc[index - datetime.timedelta(minutes=1)][stock]

    close_prices = close_prices.tolist()
    return close_prices


def resample_minute_prices(context, data, window_size, required_sample_size):
    prices = data.history(context.stocks,
                          ['open', 'close', 'high', 'low', 'volume'],
                          required_sample_size * window_size, '1m')
    open_df = pd.DataFrame([])
    close_df = pd.DataFrame([])
    high_df = pd.DataFrame([])
    low_df = pd.DataFrame([])
    volume_df = pd.DataFrame([])
    for stock in context.stocks:
        high_prices = []
        low_prices = []
        volume = []
        open_prices = prices['open'].iloc[0::window_size, :][stock][:required_sample_size]
        close_prices = get_close_prices_as_list(window_size, prices, stock)[:required_sample_size]
        minute_high = prices['high'][stock]
        for l in range(len(minute_high) // window_size):
            high_prices.append(max(minute_high[window_size * l:window_size * (l + 1)].dropna()))
        minute_low = prices['low'][stock]
        for l in range(len(minute_low) // window_size):
            low_prices.append(min(minute_low[window_size * l:window_size * (l + 1)].dropna()))
        minute_volume = prices['volume'][stock]
        for l in range(len(minute_volume) // window_size):
            volume.append(sum(minute_volume[window_size * l:window_size * (l + 1)].dropna()))

        df = pd.DataFrame([])
        df['open'] = open_prices  # sets the index
        df['close'] = close_prices  # uses the existing index
        df['high'] = high_prices  # uses the existing index
        df['low'] = low_prices  # uses the existing index
        df['volume'] = volume  # uses the existing index

        open_df[stock.symbol] = df['open']
        close_df[stock.symbol] = df['close']
        high_df[stock.symbol] = df['high']
        low_df[stock.symbol] = df['low']
        volume_df[stock.symbol] = df['volume']

    result = pd.Panel({'open':   open_df,
                       'close':  close_df,
                       'high':   high_df,
                       'low':    low_df,
                       'volume': volume_df,
                       })
    return result


def sell_if_stop_loss_was_hit(context, data):
    try:
        for position in context.mark_for_close:
            order_target(position, 0)
        context.mark_for_close = []
        if context.portfolio.positions:
            long_stop_loss = 1 - float(
                context.stop_loss) / 100  # so if we want 5%, stop_loss will be 0.95
            for position in context.portfolio.positions:
                buying_price = context.portfolio.positions[position].cost_basis
                amount = context.portfolio.positions[position].amount
                current_price = data.current(position, 'close')
                if amount > 0:
                    low = data.current(position, 'low')
                    if low <= long_stop_loss * buying_price:
                        context.mark_for_close.append(position)


    except Exception as e:
        log.error("Error during sell_if_stop_loss_was_hit: %s", e)