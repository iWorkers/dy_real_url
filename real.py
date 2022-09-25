import re
import sys

import requests


def get_real_url(url,try_count = 1):
    if try_count > 3:
       return url
    try:
       rs = requests.get(url,headers=http_headers,timeout=10)
       if rs.status_code > 400:
           return get_real_url(url,try_count+1)
       return rs.url
    except:
       return get_real_url(url, try_count + 1)


DEBUG = False


http_headers = {
                    'Accept': '*/*',
                    'Connection': 'keep-alive',
                    'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/53.0.2785.116 Safari/537.36'
                }

    




headers = {
    'authority': 'v.douyin.com',
    'user-agent': 'Mozilla/5.0 (iPhone; CPU iPhone OS 10_3_1 like Mac OS X) AppleWebKit/603.1.30 (KHTML, like Gecko) Version/10.0 Mobile/14E304 Safari/602.1',
}

share_url = input('请输入抖音直播分享链接：')
url=get_real_url(share_url , 1)
print(url)
m=re.search('reflow/(.*?)\?u_code', url)
print(m)
if m:
    room_id = m.group(1)
else:
    try:
        url = re.search(r'(https.*)', url).group(1)
        response = requests.head(url, headers=headers)
        url = response.headers['location']
        room_id = re.search(r'\d{19}', url).group(0)
    except Exception as e:
        if DEBUG:
            print(e)
        print('获取room_id失败')
        sys.exit(1)
print('room_id', room_id)
try:
    headers.update({
        'authority': 'webcast.amemv.com',
        'cookie': '_tea_utm_cache_1128={%22utm_source%22:%22copy%22%2C%22utm_medium%22:%22android%22%2C%22utm_campaign%22:%22client_share%22}',
    })

    params = (
       ('type_id', '0'),
       ('live_id', '1'),
       ('room_id', room_id),
       ('app_id', '1128'),
    )

    response = requests.get('https://webcast.amemv.com/webcast/room/reflow/info/', headers = headers, params = params).json()

    rtmp_pull_url = response['data']['room']['stream_url']['rtmp_pull_url']
    hls_pull_url = response['data']['room']['stream_url']['hls_pull_url']
    print(rtmp_pull_url)
    print(hls_pull_url)
except Exception as e:
    if DEBUG:
       print(e)
       print('获取real url失败')



