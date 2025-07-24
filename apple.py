import pandas as pd
from app_store_scraper import AppStore

app = AppStore(country='kh', app_name='SmartNas', app_id='1205849979')
app.review(how_many=2000)

df = pd.DataFrame(app.reviews)

df = df.rename(columns={
    'id': 'review_id',
    'userName': 'username',
    'review': 'content',
    'rating': 'rating',
    'date': 'review_date'
})

df = df[['review_id', 'username', 'content', 'rating', 'review_date']]

# Optional: Export to CSV
df.to_csv("appstore_reviews.csv", index=False, encoding='utf-8-sig')
print(f"✅ Exported {len(df)} reviews.")
