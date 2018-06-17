from urllib import request
from bs4 import BeautifulSoup
import time, json

def get_posts(url, pages_count):
    post_urls = []
    for index in range(1, pages_count + 1):
        with request.urlopen(url + 'page{}/'.format(index)) as conn:
            soup = BeautifulSoup(conn.read(), 'html.parser')
            time.sleep(1)
        posts = soup.find_all('div', 'post')
        for post in posts:
            a_s = post.find_all('a', 'comments_count')
            for a in a_s:
                post_urls.append(a.get('href'))
    return post_urls

def get_comments(url):
    good = []
    bad = []

    try:
        conn = request.urlopen(url)
        soup = BeautifulSoup(conn.read(), 'html.parser')
    except:
        print('Cannot open url!')
        return good, bad
    comments = soup.find_all('div', 'comment_item')
    for comment in comments:
        for text_html in comment.find_all('div', 'text_html'):
            message = ''.join(text_html.findAll(text=True))
            for span in comment.find_all('span', 'positive'):
                good.append(message)
            for span in comment.find_all('span', 'negative'):
                bad.append(message)
    return good, bad

def dump_comments(comments, file_name):
    with open(file_name, 'w') as out_file:
        json.dump({'comments': comments}, out_file, indent=4, ensure_ascii=False)

posts = get_posts('https://m.geektimes.ru/hub/it_regulation/', 141)
good_comments = []
bad_comments = []

i = 1
for post in posts:
    print('Post', i, 'from', len(posts), post)
    good, bad = get_comments(post)
    good_comments = good_comments + good
    bad_comments = bad_comments + bad
    time.sleep(1)
    i = i + 1

dump_comments(good_comments, 'good_comments.json')
dump_comments(bad_comments, 'bad_comments.json')

print('Bad comments:', len(bad_comments))
print('Good comments:', len(good_comments))
