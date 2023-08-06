import talib
import numpy as np

from quantopian.algorithm import attach_pipeline, pipeline_output
from quantopian.pipeline import Pipeline
from quantopian.pipeline.data.builtin import USEquityPricing
# for pipeline
from quantopian.pipeline.factors import AverageDollarVolume, \
    SimpleMovingAverage, Latest
from quantopian.pipeline.factors import CustomFactor, RSI
from quantopian.pipeline.data.quandl import cboe_vix
from quantopian.pipeline.data.quandl import cboe_vxv
from quantopian.pipeline.data.quandl import cboe_skew

import numpy as np
import pandas as pd
import datetime
import dateutil


def handle_data(context, data):
    pass


def init_context_parameters(context):
    context.long_trailing_stop_percentage = 20  # 20%
    context.short_trailing_stop_percentage = 30  # 30%
    context.should_limit_stop_loss_price = True
    context.max_allowed_loss_per_share = 0.4
    context.max_allowed_loss_per_trade = 100  # => 100 % per trade
    context.should_do_a_time_stop = True
    context.num_days_to_hold_a_position = 3

    context.long_target_profit_percentage = 20  # 50%
    context.short_target_profit_percentage = 20  # 50%
    context.should_limit_target_profit_price = True
    context.reasonable_target_profit_per_trade = 200  # 100$ profit per trade is a reasonable profit. so we could limit
    context.reasonable_profit_target_step_amount = 100  # => 100 $ for each trailing stop step
    context.num_of_step_in_trailing_stop = 3  # (how many pieces should we take profits)
    context.profit_target_percentage = 10  # => 1% for each trailing stop step

    context.max_portfolio_allowed_loss = -0.4  # don't allow to lose more than 40% of the portfolio


def initialize(context):
    context.trailing_stop_target_data = {}
    context.positions_closed_today = {'date':        get_datetime(),
                                      'equity_list': []}
    print("   **************  calling initialize **************  ")
    init_context_parameters(context)
    pass

    set_commission(commission.PerShare(cost=0.01))
    set_slippage(slippage.FixedBasisPointsSlippage())

    schedule_function(rebalance, date_rules.every_day(),
                      time_rules.market_open(minutes=10))
    context.equities = [symbol('SPXS'), symbol('SPXL')]


def before_trading_start(context, data):
    print("   ************** calling before_trading_start **************  ")
    init_context_parameters(context)
    context.is_zipline = False

    context.positions_closed_today = {'date':        get_datetime(),
                                      'equity_list': []}


def rebalance(context, data):
    prices = resample_minute_prices(context.equities, data, 60, 42)
    doing_it_with_mean(context, data, prices)
    print(("current_dt: %s " % data.current_dt))


def doing_it_with_mean(context, data, prices):
    short_periods = 12
    long_periods = 26
    positions = get_portfolio_positions(context)
    for equity in context.equities:
        short_ema = \
        pd.Series.ewm(prices['close'][equity.symbol][-short_periods:],
                      span=short_periods).mean().iloc[-1]
        long_ema = \
        pd.Series.ewm(prices['close'][equity.symbol][-long_periods:],
                      span=long_periods).mean().iloc[-1]

        macd = short_ema - long_ema

        if macd > 0:
            if not positions[equity.symbol].amount:
                open_stock_position(context, data, equity, 200, 2, 'open')
        elif macd < 0:
            if positions[equity.symbol].amount:
                close_position(context, data, equity, "close")


def get_close_prices_as_list(window_size, prices, stock):
    close_prices = prices['close'].iloc[window_size - 2::window_size, :][stock]

    for index, el in list(close_prices.items()):
        if np.isnan(el):
            close_prices[index] = \
            prices['close'].loc[index - datetime.timedelta(minutes=1)][stock]

    close_prices = close_prices.tolist()
    return close_prices


def resample_minute_prices(equity_list, data, window_size,
                           required_sample_size):
    prices = data.history(equity_list,
                          ['open', 'close', 'high', 'low', 'volume'],
                          required_sample_size * window_size, '1m')
    open_df = pd.DataFrame([])
    close_df = pd.DataFrame([])
    high_df = pd.DataFrame([])
    low_df = pd.DataFrame([])
    volume_df = pd.DataFrame([])
    for stock in equity_list:
        high_prices = []
        low_prices = []
        volume = []
        open_prices = prices['open'].iloc[0::window_size, :][stock][
                      :required_sample_size]
        close_prices = get_close_prices_as_list(window_size, prices, stock)[
                       :required_sample_size]
        minute_high = prices['high'][stock]
        for l in range(len(minute_high) // window_size):
            high_prices.append(max(
                minute_high[window_size * l:window_size * (l + 1)].dropna()))
        minute_low = prices['low'][stock]
        for l in range(len(minute_low) // window_size):
            low_prices.append(min(
                minute_low[window_size * l:window_size * (l + 1)].dropna()))
        minute_volume = prices['volume'][stock]
        for l in range(len(minute_volume) // window_size):
            volume.append(sum(
                minute_volume[window_size * l:window_size * (l + 1)].dropna()))

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


def get_current_price_avoid_nans_if_possible(context, data, equity,
                                             field='close'):
    current_price = data.current(equity, field)
    if np.isnan(current_price):
        frame = data.history(equity, field, 60, '1m').tolist()
        for l in reversed(frame):
            if not np.isnan(l):
                current_price = l
                break
    if not np.isnan(current_price):
        return current_price


from collections import OrderedDict


def get_portfolio_positions(context):
    positions = context.portfolio.positions
    return positions


from zipline.api import get_open_orders, cancel_order, order_target, get_order, \
    get_datetime, order_target_percent, order


def close_position(context, data, equity, reason) -> str:
    positions = get_portfolio_positions(context)
    current_price = round(positions[equity].last_sale_price, 2)
    cost_basis = round(positions[equity].cost_basis, 2)  # buy price
    amount = positions[equity].amount
    if amount == 0:
        return
    profit = round((current_price - cost_basis) * amount, 2)
    profit_percent = round(
        100 * np.sign(amount) * (current_price - cost_basis) / cost_basis, 2)
    order_id = None
    commission = 0
    tries = 0
    pass
    context.positions_closed_today['equity_list'].append(equity)
    delete_trailing_stop_target_data_for_equity(context, equity)
    log.info(
        "closing position: {symbol}. cost_basis: {cost_basis:.2f}. current_price: {current_price:.2f}. "
        "amount: {amount:d}. profit: {share_profit:.2f}. percent: {profit_percent:.2f}%. "
        "reason: {reason}".format(symbol=equity.symbol,
                                  cost_basis=cost_basis,
                                  current_price=current_price,
                                  amount=amount,
                                  share_profit=profit,
                                  profit_percent=profit_percent,
                                  reason=reason))
    return order_id


def open_stock_position(context,
                        data,
                        equity,
                        amount: int,
                        order_type,
                        message: str,
                        should_limit_bid_ask=True):
    closing_partial_amount = False
    old_amount = None
    old_price = None
    positions = get_portfolio_positions(context)
    if equity in positions:  # we already hold shares, so let's get exact amount
        old_amount = positions[equity].amount
        if old_amount != amount:
            closing_partial_amount = True
        old_price = positions[equity].cost_basis
    order_id = None
    if order_type == 1:
        order_id = order(equity, amount)
    elif order_type == 2:
        order_id = order_target(equity, amount)
    elif order_type == 3:
        order_id = order_target_percent(equity, amount)

    if order_id:
        orderObj = get_order(order_id)
        filled_amount = int(np.sign(amount) * orderObj.filled)
        commission = orderObj.commission

        price = get_current_price_avoid_nans_if_possible(context, data, equity,
                                                         field='close')
        initialize_trailing_stop_target_data(context,
                                             equity,
                                             amount=amount,
                                             cost_basis=price,
                                             short=amount < 0)
        log.info(message)

        if filled_amount:
            log.info(
                " {date}: {message}. filled: {filled}. commission: {commission:.2f}".format(

                    date=str(data.current_dt),
                    message=message,
                    filled=filled_amount,
                    commission=commission))
            if closing_partial_amount:
                pass  # written like this for zipline_to_quantopian
        else:
            pass  # for zipline to Q. don't remove
    return True


def close_all_positions(context, data, reason=""):
    positions = get_portfolio_positions(context)
    if positions:
        log.info(" {date}: Closing all positions: {reason}".format(

            date=str(data.current_dt),
            reason=reason))
        for stock in positions:
            close_position(context, data, stock,
                           "closing all positions" if not reason else reason)


def close_all_positions_at_day_end(context, data):
    close_all_positions(context, data, reason="EOD")


def get_controlled_stop_loss_price(context, stop_loss, buying_price, amount):
    amount = abs(amount)
    stop_loss_price = stop_loss * buying_price
    if not context.should_limit_stop_loss_price:
        return stop_loss_price

    if stop_loss < 1:
        long = True
    else:
        long = False

    if int:
        loss_with_stop_loss = (buying_price - stop_loss_price) * amount

        stop_loss_with_max_loss_per_share = buying_price - context.max_allowed_loss_per_share
        loss_with_max_loss_per_share = context.max_allowed_loss_per_share * amount

        stop_loss_price_with_max_loss_per_trade = buying_price - context.max_allowed_loss_per_trade / amount
        loss_with_max_loss_per_trade = context.max_allowed_loss_per_trade
    else:  # short
        loss_with_stop_loss = (stop_loss_price - buying_price) * amount

        stop_loss_with_max_loss_per_share = buying_price + context.max_allowed_loss_per_share
        loss_with_max_loss_per_share = context.max_allowed_loss_per_share * amount

        stop_loss_price_with_max_loss_per_trade = buying_price + context.max_allowed_loss_per_trade / amount
        loss_with_max_loss_per_trade = context.max_allowed_loss_per_trade
    max_allowed_loss = min(loss_with_stop_loss, loss_with_max_loss_per_share,
                           loss_with_max_loss_per_trade)
    if max_allowed_loss == loss_with_stop_loss:
        return stop_loss_price
    elif max_allowed_loss == loss_with_max_loss_per_share:
        return stop_loss_with_max_loss_per_share
    elif max_allowed_loss == loss_with_max_loss_per_trade:
        return stop_loss_price_with_max_loss_per_trade


def close_position_if_stop_loss_reached(context, data):
    try:
        positions = get_portfolio_positions(context)
        if positions:
            long_stop_loss = 1 - float(
                context.long_trailing_stop_percentage) / 100
            short_stop_loss = 1 + float(
                context.short_trailing_stop_percentage) / 100
            for equity in positions:
                buying_price = positions[equity].cost_basis
                amount = positions[equity].amount
                current_price = get_current_price_avoid_nans_if_possible(
                    context, data, equity, field='close')
                if amount > 0:
                    controlled_stop_loss_price = \
                        get_controlled_stop_loss_price(context, long_stop_loss,
                                                       buying_price, amount)
                    if not current_price or current_price <= controlled_stop_loss_price:
                        close_position(context, data, equity,
                                       "reached stop loss ({:.2f})".format(
                                           controlled_stop_loss_price))
                elif amount < 0:
                    controlled_stop_loss_price = \
                        get_controlled_stop_loss_price(context,
                                                       short_stop_loss,
                                                       buying_price, amount)
                    if not current_price or current_price >= controlled_stop_loss_price:
                        close_position(context, data, equity,
                                       "reached stop loss ({:.2f})".format(
                                           controlled_stop_loss_price))
    except Exception as e:
        log.error("Error during close_position_if_stop_loss_reached: %s", e)


def initialize_trailing_stop_target_data(context, equity, amount, cost_basis,
                                         short=False):
    if equity.symbol not in context.trailing_stop_target_data:
        context.trailing_stop_target_data[equity.symbol] = {}
        context.trailing_stop_target_data[equity.symbol][
            'prev_target_price'] = cost_basis
        context.trailing_stop_target_data[equity.symbol][
            'num_of_closed_parts'] = 0  # so if we close a third every time,this will be in [0:2]
        context.trailing_stop_target_data[equity.symbol][
            'amount_to_close_each_step'] = \
            int(abs(amount / context.num_of_step_in_trailing_stop))
        context.trailing_stop_target_data[equity.symbol][
            'initial_amount'] = amount
        context.trailing_stop_target_data[equity.symbol][
            'should_enable_trailing_stop'] = True
        if short:
            context.trailing_stop_target_data[equity.symbol][
                'stop_loss_factor'] = \
                1 + float(context.short_trailing_stop_percentage) / 100
        else:
            context.trailing_stop_target_data[equity.symbol][
                'stop_loss_factor'] = \
                1 - float(context.long_trailing_stop_percentage) / 100
        context.trailing_stop_target_data[equity.symbol][
            'trailing_stop_price'] = \
            get_controlled_stop_loss_price(context,
                                           context.trailing_stop_target_data[
                                               equity.symbol][
                                               'stop_loss_factor'],
                                           cost_basis,
                                           amount)


def delete_trailing_stop_target_data_for_equity(context, equity):
    if equity.symbol in context.trailing_stop_target_data:
        del context.trailing_stop_target_data[equity.symbol]


def get_controlled_target_profit_price(context, target_profit, buying_price,
                                       amount, reasonable_profit):
    amount = abs(amount)
    target_profit_price = target_profit * buying_price
    if not context.should_limit_target_profit_price:
        return target_profit_price

    if target_profit > 1:
        long = True
    else:
        long = False

    if int:
        profit_with_target_profit = (
                                                target_profit_price - buying_price) * amount
        if profit_with_target_profit > reasonable_profit:
            target_profit_price = reasonable_profit / amount + buying_price
    else:
        profit_with_target_profit = (
                                                buying_price - target_profit_price) * amount
        if profit_with_target_profit > reasonable_profit:
            target_profit_price = buying_price - reasonable_profit / amount
    return target_profit_price


def close_position_if_target_profit_reached(context, data):
    try:
        positions = get_portfolio_positions(context)
        if positions:
            long_target_profit = 1 + float(
                context.long_target_profit_percentage) / 100
            short_target_profit = 1 - float(
                context.short_target_profit_percentage) / 100
            for equity in positions:
                buying_price = positions[equity].cost_basis
                amount = positions[equity].amount
                current_price = get_current_price_avoid_nans_if_possible(
                    context, data, equity, field='close')
                if amount > 0:
                    if not current_price or current_price >= \
                            get_controlled_target_profit_price(context,
                                                               long_target_profit,
                                                               buying_price,
                                                               amount,
                                                               context.reasonable_target_profit_per_trade):
                        close_position(context, data, equity,
                                       "reached target profit")
                elif amount < 0:
                    if not current_price or current_price <= \
                            get_controlled_target_profit_price(context,
                                                               short_target_profit,
                                                               buying_price,
                                                               amount,
                                                               context.reasonable_target_profit_per_trade):
                        close_position(context, data, equity,
                                       "reached target profit")
    except Exception as e:
        log.error("Error during close_position_if_stop_loss_reached: %s", e)


def close_partial_position_in_multi_step_target_scheme(context, data, equity,
                                                       amount, current_price,
                                                       short=False):
    if short:
        profit = context.trailing_stop_target_data[equity.symbol][
                     'prev_target_price'] - current_price
    else:
        profit = current_price - \
                 context.trailing_stop_target_data[equity.symbol][
                     'prev_target_price']
    amount_to_close = context.trailing_stop_target_data[equity.symbol][
        'amount_to_close_each_step']
    message = "closing partial position:{amount} shares of {symbol} at {price:.2f} for a profit of {profit_share:.2f} per share. " \
              "{total_profit:.2f} in total".format(amount=amount_to_close,
                                                   symbol=equity.symbol,
                                                   price=current_price,
                                                   profit_share=profit,
                                                   total_profit=amount_to_close * profit)

    if short:
        new_required_amount = amount + amount_to_close
    else:
        new_required_amount = amount - amount_to_close
    if open_stock_position(context, data, equity, new_required_amount, 2,
                           message):
        context.trailing_stop_target_data[equity.symbol][
            'prev_target_price'] = current_price  # we've reached the target price which is current_price
        context.trailing_stop_target_data[equity.symbol][
            'num_of_closed_parts'] += 1


def multi_step_trailing_target(context, data):
    def _internal(context, equity, current_price, amount, target_profit,
                  short: bool):
        controlled_target_profit_price = \
            get_controlled_target_profit_price(context,
                                               target_profit,
                                               context.trailing_stop_target_data[
                                                   equity.symbol][
                                                   'prev_target_price'],
                                               amount,
                                               context.reasonable_profit_target_step_amount)
        if (short and current_price <= controlled_target_profit_price) or \
                (
                        not short and current_price >= controlled_target_profit_price):
            if context.trailing_stop_target_data[equity.symbol][
                'num_of_closed_parts'] < \
                    context.num_of_step_in_trailing_stop - 1:
                try:
                    close_partial_position_in_multi_step_target_scheme(context,
                                                                       data,
                                                                       equity,
                                                                       amount,
                                                                       current_price,
                                                                       short=short)
                except:
                    log.error(
                        "timeout exception while trying to close partial position for {}".format(
                            equity.symbol))

    positions = get_portfolio_positions(context)
    for equity in positions:
        if equity.symbol not in context.trailing_stop_target_data:
            continue
        amount = positions[equity].amount
        long = True if amount > 0 else False
        current_price = get_current_price_avoid_nans_if_possible(context, data,
                                                                 equity,
                                                                 field='close')
        if not current_price:
            close_position(context,
                           data,
                           equity,
                           "could not get current price. "
                           "closing position in trailing target: {}".format(
                               equity.symbol))
            continue
        if int:
            long_target_profit = 1 + float(
                context.long_target_profit_percentage) / 100
            _internal(context, equity, current_price, amount,
                      long_target_profit, short=False)
        else:
            short_target_profit = 1 - float(
                context.short_target_profit_percentage) / 100
            _internal(context, equity, current_price, amount,
                      short_target_profit, short=True)


def close_position_if_trailing_stop_reached(context, data):
    positions = get_portfolio_positions(context)
    for equity in positions:  # don't delete this remark, it's for zipline to Q
        if equity.symbol not in context.trailing_stop_target_data:
            continue
        if equity.symbol in context.trailing_stop_target_data and \
                context.trailing_stop_target_data[equity.symbol][
                    'should_enable_trailing_stop']:
            amount = positions[equity].amount
            reason = "reached trailing stop of: %.2f" % \
                     context.trailing_stop_target_data[equity.symbol][
                         'trailing_stop_price']
            current_price = get_current_price_avoid_nans_if_possible(context,
                                                                     data,
                                                                     equity,
                                                                     field='close')
            if not current_price:
                close_position(context,
                               data,
                               equity,
                               "could not get current price. "
                               "closing position in trailing stop: {}".format(
                                   equity.symbol))
                continue
            if amount > 0:
                if not current_price or current_price < \
                        context.trailing_stop_target_data[equity.symbol][
                            'trailing_stop_price']:
                    close_position(context, data, equity, reason)
                else:
                    context.trailing_stop_target_data[equity.symbol][
                        'trailing_stop_price'] = \
                        round(max(
                            context.trailing_stop_target_data[equity.symbol][
                                'trailing_stop_price'],
                            get_controlled_stop_loss_price(context,
                                                           context.trailing_stop_target_data[
                                                               equity.symbol][
                                                               'stop_loss_factor'],
                                                           current_price,
                                                           amount)), 2)
            else:
                if not current_price or current_price > \
                        context.trailing_stop_target_data[equity.symbol][
                            'trailing_stop_price']:
                    close_position(context, data, equity, reason)
                else:
                    context.trailing_stop_target_data[equity.symbol][
                        'trailing_stop_price'] = \
                        round(min(
                            context.trailing_stop_target_data[equity.symbol][
                                'trailing_stop_price'],
                            get_controlled_stop_loss_price(context,
                                                           context.trailing_stop_target_data[
                                                               equity.symbol][
                                                               'stop_loss_factor'],
                                                           current_price,
                                                           amount)), 2)