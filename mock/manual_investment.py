from entity.account import Account
from entity.position import Position
from strategy.free_trading import FreeTrading

if __name__ == '__main__':
    FreeTrading.create_account(Account('leo2', 50000))
    # FreeTrading.buy_stock(Account('leo'), Position('9999.sh', 100, 1))
    # FreeTrading.sell_stock(Account('leo'), Position('9999.sh', 100, 1))
    # FreeTrading.cancel_account(Account('leo'))
    # account_list = FreeTrading.query_account_positions(Account('leo'))
    account_list = FreeTrading.show_all_accounts_info()
    for account in account_list:
        print(account)

