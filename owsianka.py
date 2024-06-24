import pandas as pd
import sys

from ingredients import ingredients


amounts = {
    'kakao': 10,
    'platki owsiane': 50,
    'bialko': 20,
    'maslo orzechowe': 15,
    'jogurt': 150,
    'woda': 90,
}


def get_df():
    df = (
        pd.DataFrame(ingredients)
        .drop(columns=['name'])
        .set_index('type')
        .assign(amount=pd.Series(amounts))
        .assign(
            price_per_100g=lambda x: x['package_price'] / x['package_weight'] * 100,
            price=lambda x: x['price_per_100g'] / 100 * x['amount']
        )
        .drop(columns=['package_price', 'package_weight'])
    )

    total_portion = {
        key: round(df[key].mul(df['amount']).sum() / 100, 1)
        for key in df.keys()
    }
    total_portion['amount'] = df.amount.sum()
    total_portion['price'] = df.price.sum()
    df = pd.concat([df, pd.DataFrame(total_portion, index=['total_portion'])])
    total_per_100g = {
        key: round(total_portion[key] / total_portion['amount'] * 100, 1)
        for key in total_portion.keys()
    }
    df = pd.concat([df, pd.DataFrame(total_per_100g, index=['total_per_100g'])])
    return df


def main():
    df = get_df()

    if len(sys.argv) <= 1:
        print(df.round(2))
        return

    elif len(sys.argv) == 2:
        print('Invalid argument')
    elif len(sys.argv) == 3:
        if sys.argv[1] == 'calories':
            calories = int(sys.argv[2])
            if calories < 0:
                print('Calories must be a positive number')
                return
            g_for_calories = calories / df['calories']['total_per_100g'] * 100
            print('ile gramow owsianki na', calories, 'kcal', ': ', round(g_for_calories, 1))
            print()
            print(df.loc['total_per_100g'].mul(g_for_calories / 100))
        elif sys.argv[1] == 'portion':
            total_weight = int(sys.argv[2])
            if total_weight < 0:
                print('Portion weight must be a positive number')
                return
            proportions = df['amount'] / df.loc['total_portion', 'amount']
            new_portion = proportions * total_weight
            print('Amount of each ingredient for a', total_weight, 'g portion:')
            print(new_portion.drop(['total_per_100g', 'total_portion']).astype(int).to_string(header=False))
        else:
            print('Invalid argument')
    else:
        print('Invalid argument')


if __name__ == '__main__':
    main()
