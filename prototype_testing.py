import datetime
import pandas as pd

import helpers

data_01 = [[datetime.date(2021, 12, 23), 12, "Some comment from df 1"],
           [datetime.date(2021, 11, 26), "23", "Another comment from df 1"]]
data_02 = [[datetime.date(2021, 4, 13), 20, "Some comment from df 2"],
           [datetime.date(2021, 10, 6), "5", "Another comment from df 2"],
           [datetime.date(2022, 1, 12), "35", "One more comment from df 2"]]
columns = ["Date", "Lessons", "Comment"]
df_1 = pd.DataFrame(data=data_01, columns=columns)
df_2 = pd.DataFrame(data=data_02, columns=columns)

print(df_1)
print(df_2)
