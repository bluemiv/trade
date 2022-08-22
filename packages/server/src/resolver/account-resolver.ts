import { Mutation, Query, Resolver } from 'type-graphql';
import { Account } from '../entity';
import { get_upbit_account } from '../service/upbit-service';

@Resolver()
class AccountResolver {
    @Query(() => [Account])
    async accounts() {
        const resData = await get_upbit_account();
        return resData.map(({ currency, balance, locked, avg_buy_price, avg_buy_price_modified, unit_currency }) => {
            return Account.create({
                currency,
                balance,
                locked,
                avgBuyPrice: avg_buy_price,
                avgBuyPriceModified: avg_buy_price_modified,
                unitCurrency: unit_currency,
            });
        });
    }

    @Mutation(() => [Account])
    async insertAccounts() {
        const resData = await get_upbit_account();
        return resData.map(({ currency, balance, locked, avg_buy_price, avg_buy_price_modified, unit_currency }) => {
            const account = Account.create({
                currency,
                balance,
                locked,
                avgBuyPrice: avg_buy_price,
                avgBuyPriceModified: avg_buy_price_modified,
                unitCurrency: unit_currency,
            });
            account.save();
            return account;
        });
    }
}

export default AccountResolver;
