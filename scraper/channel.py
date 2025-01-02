import configparser
import os

config = configparser.ConfigParser()
current_dir = os.path.dirname(os.path.abspath(__file__))
config_path = os.path.join(current_dir, '../config/config.ini')
config.read(config_path, encoding='utf-8')


import urllib
import json

def get_all_video_in_channel(channel_id):
    api_key = YOUR API KEY

    base_video_url = 'https://www.youtube.com/watch?v='
    base_search_url = 'https://www.googleapis.com/youtube/v3/search?'

    first_url = base_search_url+'key={}&channelId={}&part=snippet,id&order=date&maxResults=25'.format(api_key, channel_id)

    video_links = []
    url = first_url
    while True:
        inp = urllib.urlopen(url)
        resp = json.load(inp)

        for i in resp['items']:
            if i['id']['kind'] == "youtube#video":
                video_links.append(base_video_url + i['id']['videoId'])

        try:
            next_page_token = resp['nextPageToken']
            url = first_url + '&pageToken={}'.format(next_page_token)
        except:
            break
    return video_links


if __name__ == "__main__":
    print("start")

    req_url = 'https://www.youtube.com/watch?v=kuDuJWvho7Q'

    # video = scrape(req_url)

    # 출력 경로 정의
    # output_path = 'output/video.json'
    # output_dir = os.path.dirname(output_path)
    #
    # # 디렉토리 생성 확인
    # if not os.path.exists(output_dir):
    #     os.makedirs(output_dir)
    #
    # with open(output_path, 'w', encoding='utf-8') as file:
    #     json.dump(video, file, ensure_ascii=False, indent=4)

    print("finish")
