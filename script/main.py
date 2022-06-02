# -*- coding: utf-8 -*-

'''
# 전략 1. 무한 매매
 - 10000원으로 구매
 - -10%일때 구매한 금액만큼 추가 매수
 - +5% 수익일때는 전량 매도
 - 15분 간격으로 배치 실행
'''

from strategy.installment_purchase import InstallmentPurchase

if __name__ == '__main__':
    installmentPurchase = InstallmentPurchase()
    installmentPurchase.run()
