# -*- coding: utf-8 -*-

from strategy.installment_purchase import InstallmentPurchase
from utils import config_parser

doc = '''
 __   __             __   __  ___ 
/  ` /  \ | |\ |    |__) /  \  |  
\__, \__/ | | \|    |__) \__/  |  


Strategy
    1. 분할매수/매도 (installment purchase)
'''

if __name__ == '__main__':
    config = config_parser.get_config()
    print(doc)
    while True:
        strategy_number = input('Input strategy number: ')

        if strategy_number == '1':
            break
        else:
            print("Invalid input.")

    black_list = config['black_list']

    if strategy_number == '1':
        disabled_new_buy = input(' > 신규 매수 기능 비활성화 (Y: 비활성화 or N: 활성화): ')
        disabled_buy = input(' > 매수 기능 비활성화 (Y: 비활성화 or N: 활성화): ')
        disabled_sell = input(' > 매도 기능 비활성화 (Y: 비활성화 or N: 활성화): ')
        options = {
            'disabled_new_buy': True if disabled_new_buy in ['y', 'Y'] else False,
            'disabled_buy': True if disabled_buy in ['y', 'Y'] else False,
            'disabled_sell': True if disabled_sell in ['y', 'Y'] else False
        }
        installmentPurchase = InstallmentPurchase(black_list=black_list, options=options)
        installmentPurchase.run()
