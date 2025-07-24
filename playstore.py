from google_play_scraper import reviews, Sort
import pandas as pd
import time


def scrape_google_play_reviews(app_package_name, max_reviews=5000, sleep_time=1.5):
    all_reviews = []
    next_token = None

    print(f"Starting to scrape reviews for: {app_package_name}")
    while len(all_reviews) < max_reviews:
        batch, next_token = reviews(
            app_package_name,
            lang='en',
            country='kh',
            sort=Sort.NEWEST,
            count=200,
            continuation_token=next_token
        )
        if not batch:
            print("No more reviews found.")
            break

        all_reviews.extend(batch)
        print(f"Fetched {len(all_reviews)} / {max_reviews} reviews...")

        if not next_token:
            break

        time.sleep(sleep_time)

    all_reviews = all_reviews[:max_reviews]
    df = pd.DataFrame(all_reviews)

    if df.empty:
        print("No reviews found.")
        return df

    expected_columns = ['reviewId', 'userName', 'content', 'score', 'at']
    missing_columns = [col for col in expected_columns if col not in df.columns]
    if missing_columns:
        print(f"Missing columns in DataFrame: {missing_columns}")
        print(f"Available columns: {list(df.columns)}")
        return df

    df = df[expected_columns]
    df.columns = ['review_id', 'username', 'content', 'rating', 'review_date']
    return df


if __name__ == "__main__":
    app_package = 'net.omobio.smartsc'
    reviews_df = scrape_google_play_reviews(app_package_name=app_package, max_reviews=5000)

    if not reviews_df.empty:
        output_file = ' googleplay_smartnas_reviews.csv'
        reviews_df.to_csv(output_file, index=False, encoding='utf-8-sig')
        print(f"✅ Exported {len(reviews_df)} reviews to {output_file}")
    else:
        print("⚠️ No data to export.")
