import pandas as pd
df = pd.DataFrame([{"name": "John", "role": "", "base_price": 100, "email": "j@t.com"}])
df.to_excel("dummy.xlsx", index=False)
