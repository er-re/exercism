import pandas as pd


class Luhn:
    def __init__(self, card_num: str) -> None:
        self.card_num = card_num.replace(' ', '')

    def valid(self) -> bool:
        """
        :return: True if a given string is valid Luhn sequence, False if not
        """
        if len(self.card_num) < 2 or not self.card_num.isnumeric():
            return False
        df = pd.Series(list(self.card_num)).to_frame('digit').astype(int)
        even = df.iloc[-2::-2].copy(deep=True)
        odd = df.iloc[-1::-2].copy(deep=True)
        even['digit'] = even['digit'].apply(lambda x: x*2-9 if x*2 > 9 else x*2)
        return True if (even['digit'].sum() + odd['digit'].sum()) % 10 == 0 else False

