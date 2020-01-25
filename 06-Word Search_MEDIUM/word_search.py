import pandas as pd
import re
from typing import List, Set, Dict, Tuple, Optional


class Point:
    def __init__(self, x: int, y: int) -> None:
        self.x = x
        self.y = y

    def __eq__(self, other: object) -> bool:
        if not isinstance(other, Point):
            return NotImplemented

        return self.x == other.x and self.y == other.y


class WordSearch:
    """ The implemented solution for finding specific words in the square of letters is to make all possible valid
    strings sequence including left-to-right, right-to-left, vertical and diagonal in the square and then
    look for specific words in them.
    For a better understanding of the algorithm, uncomment the two print statement
    """
    def __init__(self, puzzle: list) -> None:
        self.puzzle = puzzle
        self.df = None

    def search(self, word: str) -> Optional[Tuple[Point, Point]]:
        self.make_sequences()
        start, end = self.find_word(word)
        if not start:
            return None
        return start, end

    def make_sequences(self) -> None:
        """
        set a dataFrame with all possible sequence directions, including left-to-right, right-to-left, vertical and
        diagonal, dataFrame's column are 'letter sequences', and 'its corresponding coordinates'.
        for example 'ab' and '[(0,0), (1,1)]'
        """
        df = pd.Series(self.puzzle).to_frame('string')
        col_range = [str(col) for col in list(range(len(self.puzzle[0])))]

        df[col_range] = df['string'].apply(lambda x: pd.Series(list(x)))
        df.drop(['string'], axis=1, inplace=True)

        for ind, row in df.iterrows():
            for col in col_range:  # add coordinate to each cell
                df.iloc[ind, int(col)] = row[col] + ',' + f'({col},{ind});'

        horizontal: List[str] = [''.join(row[:].tolist()) for _, row in df.iterrows()]  # creating horizontal sequences
        vertical: List[str] = [''.join(df[col].tolist()) for col in col_range]  # creating vertical sequences

        for _ in range(len(col_range) - 1):  # adding blank rows which is needed for preservation of shifted column
            df.loc[df.index.max() + 1] = None

        diagonal: List[str] = []
        # converting southwest-northeast diagonal, and northwest-southeast diagonal to horizontal by shifting
        for columns in [col_range, reversed(col_range)]:
            df_dummy = df.copy(deep=True)
            for enum, col in enumerate(columns):
                df_dummy[col] = df_dummy[col].shift(enum)
            df_dummy.fillna('', inplace=True)
            # print(df_dummy)
            diagonal += df_dummy[col_range].apply(lambda row: ''.join(row.values.astype(str)), axis=1).tolist()
        all_possible_seq = horizontal + vertical + diagonal

        df = pd.Series(all_possible_seq).to_frame('coordinated_seq')
        df['seq'] = df['coordinated_seq'].apply(lambda x: "".join(re.findall("[a-zA-Z]+", x)))
        df['coordinates'] = df['coordinated_seq'].apply(lambda x: re.findall("\(\d+,\d+\)", x))
        df.drop(['coordinated_seq'], axis=1, inplace=True)
        # print(df)
        self.df = df

    def find_word(self, word: str) -> Tuple[Optional[Point], Optional[Point]]:
        df = self.df
        for enum, word in enumerate([word, word[::-1]]):
            df["indexes"] = df["seq"].str.find(word)
            mask = df['indexes'] >= 0
            if mask.any():
                ind = df.loc[mask]['indexes'].values[0]
                coordinates = df.loc[mask]['coordinates'].values[0][ind: ind + len(word)]
                start: Tuple[int, int] = eval(coordinates[0].replace("'", ''))
                start: Point = Point(int(start[0]), int(start[1]))
                end: Tuple[int, int] = eval(coordinates[-1].replace("'", ''))
                end: Point = Point(int(end[0]), int(end[1]))
                return (start, end) if enum == 0 else (end, start)
        return None, None
