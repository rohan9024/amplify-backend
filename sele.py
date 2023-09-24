from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.service import Service as ChromeService
from selenium.webdriver.chrome.options import Options as ChromeOptions


def fetch_recent_tweets(username, count=10):
    # Set up Chrome WebDriver
    chrome_options = ChromeOptions()
    # Run Chrome in headless mode (no browser window)
    chrome_options.add_argument("--headless")
    # Replace with the path to your chromedriver.exe
    service = ChromeService(executable_path="path_to_your_chromedriver.exe")
    driver = webdriver.Chrome(service=service, options=chrome_options)

    url = f"https://twitter.com/{username}"
    driver.get(url)

    # Scroll to load more tweets (modify this loop depending on the number of tweets you want to load)
    for _ in range(count // 5):  # Assuming 5 tweets are loaded with each scroll
        driver.execute_script(
            "window.scrollTo(0, document.body.scrollHeight);")
        driver.implicitly_wait(5)  # Wait for tweets to load

    # Extract tweet elements
    tweets = driver.find_elements(By.XPATH, "//div[@data-testid='tweet']")

    recent_tweets = []
    for tweet in tweets[:count]:
        tweet_text = tweet.find_element(
            By.XPATH, ".//div[@lang]").get_attribute("aria-label")
        recent_tweets.append(tweet_text)

    # Close the WebDriver
    driver.quit()

    return recent_tweets


if __name__ == "__main__":
    account_name = "imVkohli"  # Replace this with the account you want to fetch tweets from
    recent_tweets = fetch_recent_tweets(account_name, count=10)

    if recent_tweets:
        for index, tweet in enumerate(recent_tweets, start=1):
            print(f"{index}. {tweet}")
    else:
        print("No tweets fetched.")
