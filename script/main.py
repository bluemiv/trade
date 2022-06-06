# -*- coding: utf-8 -*-

from strategy.installment_purchase import InstallmentPurchase

if __name__ == '__main__':
    black_list = ['KRW-BTT', 'KRW-NU', 'KRW-LTC', 'KRW-XEM']
    installmentPurchase = InstallmentPurchase(init_krw=10100, black_list=black_list)
    installmentPurchase.run()
