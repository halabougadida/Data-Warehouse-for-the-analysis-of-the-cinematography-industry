from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.options import Options
import time
import pandas as pd

# Run browser invisibly (headless mode)
options = Options()
options.add_argument("--headless")
options.add_argument("--no-sandbox")
options.add_argument("--disable-dev-shm-usage")

driver = webdriver.Chrome(options=options)

def scrape_metacritic(movie_slug):
    """
    movie_slug is the URL-friendly name e.g. 'the-dark-knight'
    You get this by replacing spaces with hyphens and lowercasing the title
    """
    url = f"https://www.metacritic.com/movie/{movie_slug}/"
    driver.get(url)
    time.sleep(3)  # wait for page to load

    try:
        # Critic score — the big number on the left
        critic = driver.find_element(
            By.CSS_SELECTOR,
            "div.c-siteReviewScore span"
        ).text.strip()
    except:
        critic = None

    try:
        # User score — smaller number on the right side
        user = driver.find_element(
            By.CSS_SELECTOR,
            "div.c-siteReviewScore_user span"
        ).text.strip()
    except:
        user = None

    return {"slug": movie_slug, "metascore": critic, "user_score": user}

# List of movies to scrape (build this from your Kaggle CSV titles)
movies_to_scrape = ["the-dark-knight", "inception", "interstellar", "avatar"]

results = []
for slug in movies_to_scrape:
    data = scrape_metacritic(slug)
    results.append(data)
    print(f"Scraped: {slug} → {data}")
    time.sleep(2)  # pause between requests to avoid being blocked

driver.quit()

scraped_df = pd.DataFrame(results)
scraped_df.to_csv("metacritic_scores.csv", index=False)