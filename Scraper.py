from email import encoders
from email.mime.base import MIMEBase

import body as body
from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.by import By
import pandas as pd
import smtplib
import os
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
import json



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

def send_email(body):
    try:
        server_ssl = smtplib.SMTP_SSL('smtp.gmail.com', 465)
        server_ssl.ehlo()  # optional

        Sender_email = os.environ.get('sender_email')
        Receiver_email = "pateljaisvi7@gmail.com"
        Sender_password = os.environ.get('gmail_password')

        subject = 'YouTube trending videos'

        # Create the MIMEMultipart object
        msg = MIMEMultipart()

        # Attach the subject directly to the msg object
        msg['From'] = Sender_email
        msg['To'] = Receiver_email
        msg['Subject'] = subject

        # Attach the body of the email
        msg.attach(MIMEText(body, 'plain'))

        # Specify the filename to attach from the project directory
        filename = 'trending.csv'
        # Get the absolute path to the file
        file_path = os.path.abspath(filename)
        # Attach the file
        attachment = open(file_path, 'rb')

        part = MIMEBase('application', 'octet-stream')
        part.set_payload(attachment.read())
        encoders.encode_base64(part)
        part.add_header('Content-Disposition', f'attachment; filename="{filename}"')
        msg.attach(part)

        server_ssl.login(Sender_email, Sender_password)
        server_ssl.sendmail(Sender_email,Receiver_email,msg.as_string())
        server_ssl.close()

    except Exception as e:
        print(f'Something went wrong: {e}')


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
    #print(videos_df)
    videos_df.to_csv('trending.csv', index=None)

    print("send an email with results")
    body = json.dumps(videos_data,indent=3)
    send_email(body)









