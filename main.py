import common.graph.graph_drawer as graph
from common.quotation.data_filter import Filter
from common.quotation.data_wrapper import Client
import common.quotation.indicator as indicator
from common.utils import yml_loader as config
from common.utils import mapping_util
from strategy import oscillation_zone as strategy
from strategy.turtle_trade import Turtle
import talib as ta
import time

if __name__ == '__main__':
    # strategy = Turtle(1000)
    sum = Turtle.real_atr(1, 2)
    print(sum)
