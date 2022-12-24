import pandas as pd
from datetime import datetime

# print(datetime.timestamp(datetime.now()))
session_timeout = 180
df = pd.DataFrame([['022', '99063', 1668622460.805502],
                  ['033', '99631', 1668622495.790475],
                  ['044', '56789', 1668622495.790475],
                  ['022', '99063', 1668623460.805502],
                  ['033', '789', 1668622795.790475],
                  ['044', '5632478', 1668622795.790475],
                  ['022', '01025', 1668707367.867665],
                  ['033', '678', 1668622895.790475],
                  ['044', '64728', 1668707367.867666]],
                  columns=['customer_id', 'product_id', 'timestamp'])

customers_count = df['customer_id'].nunique()
df['new'] = None
df1 = df.sort_values(by=['customer_id'])# .groups
# print(df1)


# print(df2)
# print(df3)

# for customer_id, timestamp in df.groupby(['customer_id']):
#     print(customer_id, timestamp)
    # print(group)
# s = df.groupby(['customer_id']) #.sort_values(by=['timestamp'])
session_counter = 0
for window in df1.rolling(window=2):
    try:
        a = window.iloc[1].timestamp
    except:
        pass
    else:
        if abs(window.iloc[0].timestamp-window.iloc[1].timestamp) < session_timeout:
            # df1[]['new'] = session_counter
            print(window.iloc[0])
            print()
        else:
            session_counter += 1

    # #     window.iloc[0].
    # try:
    #     print(window.iloc[0].timestamp-window.iloc[1].timestamp)
    # except:
    #     print(window.iloc[0].timestamp)
    # print(df1)






