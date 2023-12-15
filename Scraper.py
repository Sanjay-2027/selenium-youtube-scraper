from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.by import By
import pandas as pd

YouTube_trending_URL = 'https://www.youtube.com/feed/trending'


def get_driver():
   chrome_options = Options()
   chrome_options.add_argument('--no-sandbox')
   chrome_options.add_argument('--headless')
   chrome_options.add_argument('--disable-dev-shm-usage')
   driver = webdriver.Chrome(options=chrome_options)
   return driver

def get_videos(driver):
    Video_Div_Tag = 'ytd-video-renderer'
    driver.get(YouTube_trending_URL)
    Videos = driver.find_elements(By.TAG_NAME, Video_Div_Tag)
    return Videos

def parse_video(video):
    title_tag = video.find_element(By.ID, 'video-title')
    title = title_tag.text
    url = title_tag.get_attribute('href')

    thumbnail_tag = video.find_element(By.TAG_NAME, 'img')
    thumbnail_url = thumbnail_tag.get_attribute('src')

    channel_div = video.find_element(By.CLASS_NAME, 'ytd-channel-name')
    channel_name = channel_div.text

    description = video.find_element(By.ID, 'description-text').text

    views = video.find_element(By.CSS_SELECTOR, 'span.style-scope.ytd-video-meta-block').text

    time_uploaded = video.find_element(By.CSS_SELECTOR, 'span.style-scope.ytd-video-meta-block + span').text

    return {
        "title ": title,
        "video url ": url,
        "thumbnail url ": thumbnail_url,
        "channel_name ": channel_name,
        "video_description ": description,
        "total_views ": views,
        "time_uploaded ": time_uploaded
    }


if __name__ == "__main__":
    print("creating the driver:")
    driver = get_driver()

    print("fetching trending videos:")
    videos = get_videos(driver)

    print(f'found {len(videos)} videos')

    print("parsing the top 10 videos:")

    videos_data = [parse_video(video) for video in videos[:10]]
    print(videos_data)

    print("save the data to a dataframe: ")
    videos_df = pd.DataFrame(videos_data)
    print(videos_df)
    videos_df.to_csv('trending.csv', index=None)








