# -*- coding: utf-8 -*-

from strategy.installment_purchase import InstallmentPurchase

if __name__ == '__main__':
    installmentPurchase = InstallmentPurchase(black_list=['KRW-BTT'])
    installmentPurchase.run()
