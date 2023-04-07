import re
import os
from json import dumps
from json import loads
from time import sleep

from bs4 import BeautifulSoup
from ez_aio import proxy0, header0
from ez_aio.aio import get
from selenium import webdriver
from selenium.webdriver.common.keys import Keys
# from selenium.webdriver.common.action_chains import ActionChains
script_re = re.compile('.*sKeyword = "(.*)", odayID = \'(.*)\', clsname = \'(.*)\'.*\n'
                       '.*gamename = "(.*)", downID = \'(.*)\',urlID = \'(.*)\', downname = "(.*)".*')


def step1(pages):
    # chrome_options = Options()
    # chrome_options.add_argument("--window-size=1920,1080")
    # driver = Chrome(chrome_options=chrome_options)
    with open('data_1.txt', 'w', encoding='utf-8') as f:
        driver = webdriver.Chrome(r'C:\PyProjects\webdriver\111.0.5563.64\chromedriver.exe')
        driver.set_window_size(1760, 990)
        print('[', end='', file=f)
        for i in range(1, pages+1):
            driver.get(fr"https://down.ali213.net/pcgame/all/0-0-0-0-new-pic-{i}")
            sleep(0.2)
            # driver.execute_script("window.scrollTo(0, 4000)")
            html = driver.find_element('tag name', 'body')
            for _ in range(4):
                sleep(0.2)
                html.send_keys(Keys.PAGE_DOWN)
            lis = driver.find_elements('class name', 'famous-li')
            # for li in lis:
            #     ActionChains(driver).move_to_element(li).perform()
            for li in lis:
                info = {}
                node = li.find_element('class name', 'game-name')
                if node:
                    info['name'] = node.text
                node = li.find_element('tag name', 'a')
                if node:
                    info['url'] = node.get_attribute('href')
                node = li.find_element('tag name', 'img')
                if node:
                    info['img_url'] = node.get_attribute('src')
                try:
                    node = li.find_element('class name', 'game-lang')
                    if node:
                        info['lang'] = node.text
                except Exception:
                    info['lang'] = ''
                hover = li.find_element('class name', 'hover-content')
                if hover:
                    divs = hover.find_elements('tag name', 'div')
                    info['time'] = divs[0].get_attribute('innerHTML').replace('<span>', '').replace('</span>', '')
                    info['size'] = divs[1].get_attribute('innerHTML').replace('<span>', '').replace('</span>', '')
                    p = hover.find_element('tag name', 'p')
                    _tags = p.get_attribute('innerHTML').replace('<span>', '').replace('</span>', '，')
                    info['tags'] = _tags[:-1] if _tags else ''
                print(dumps(info, separators=(',', ':'), indent=None, ensure_ascii=False
                            ) + (']' if i == pages and li is lis[-1] else ','), file=f)
        driver.quit()


# def ali213_get(url):
#     a = get(url, headers=header0, proxy=proxy0)[0]
#     soup = BeautifulSoup(a, 'html.parser')
#     scripts = soup.find_all('script')
#     info = {}
#     for script in scripts:
#         if 'type' in script.attrs:
#             if script.attrs['type'] == 'application/ld+json':
#                 x = loads(script.text)
#                 info['ali213_url'] = x['@id']
#                 info['tile'] = x['title']
#                 info['appid'] = x['appid']
#                 info['upload'] = x['upDate']
#                 info['publish'] = x['pubdate']
#             if script.attrs['type'] == 'text/javascript':
#                 if 'downID' in script.text:
#                     ans = script_re.match(script.text)
#                     info['cname_ename'] = ans[1]
#                     info['forumid'] = ans[2]
#                     info['clsname'] = ans[3]
#                     info['cname'] = ans[4]
#                     info['downid'] = ans[5]
#                     info['urlid'] = ans[6]
#                     info['downname'] = ans[7]
#                     return info
#
#
# def soft128_get(url):
#     a = get(url, headers=header0, proxy=proxy0)[0]
#     info = {}
#     soup = BeautifulSoup(a, 'html.parser')
#     cname = soup.find('li', {'class': 'gamecname'})
#     if cname:
#         info['cname'] = cname.text
#     ename = soup.find('li', {'class': 'gameename'})
#     if ename:
#         info['ename'] = ename.text
#     size = soup.find('li', {'class': 'gamesize'})
#     if size:
#         info['size'] = size.text
#     pic = soup.find('div', {'class': 'gamepic'})
#     if pic:
#         img = pic.find('img')
#         if img:
#             info['pic'] = img.attrs['src']
#
#     alypbox = soup.find('div', {'class': 'alypbox'})
#     if alypbox:
#         d = alypbox.find('a', {'id': 'alypbtn', 'class': 'down_xl'})
#         if d:
#             info['alypbox'] = d.attrs['href']
#
#     newhzbdd = soup.find('div', {'class': 'newhzbdd'})
#     if newhzbdd:
#         d = newhzbdd.find('a', {'id': 'wpbtn', 'class': 'down_bdd'})
#         if d:
#             info['down_bdd'] = d.attrs['data-src']
#
#     return info


# def work(link):
#     game_info = ali213_get(link)
#     if game_info:
#         print(dumps(game_info, indent=2, ensure_ascii=False))
#         down_info = soft128_get(fr'https://www.soft128.com/down/{game_info["downid"]}-1.html')
#         print(dumps(down_info, indent=2, ensure_ascii=False))


# def batch():
#     c = 1
#     with open('data_2.txt', 'r', encoding='utf-8') as f1, open('data_3.txt', 'w', encoding='utf-8') as f2:
#         info0s = loads(f1.read())
#         for info0 in info0s:
#             if info0['url'].startswith('https://down'):
#                 game_info = ali213_get(info0['url'])
#                 if game_info:
#                     down_info = soft128_get(fr'https://www.soft128.com/down/{game_info["downid"]}-1.html')
#                     info0.update(game_info)
#                     info0.update(down_info)
#             print(dumps(info0, indent=None, ensure_ascii=False) + ',', file=f2)
#             print(f'\r{c}', end='')
#             c += 1


def func2(a, d):
    for char in r'<>:"/\|?*':
        d = d.replace(char, '')
    with open(f'step2/{d}', 'w', encoding='utf-8') as f:
        print(a, file=f)
    info = {}
    soup = BeautifulSoup(a, 'html.parser')
    scripts = soup.find_all('script')
    for script in scripts:
        if 'type' in script.attrs:
            if script.attrs['type'] == 'application/ld+json':
                try:
                    x = loads(script.text, strict=False)
                    info['ali213_url'] = x['@id']
                    info['tile'] = x['title']
                    info['appid'] = x['appid']
                    info['upload'] = x['upDate']
                    info['publish'] = x['pubdate']
                except Exception:
                    print(script.text)
                    print(a)
            if script.attrs['type'] == 'text/javascript':
                if 'downID' in script.text:
                    ans = script_re.match(script.text)
                    info['cname_ename'] = ans[1]
                    info['forumid'] = ans[2]
                    info['clsname'] = ans[3]
                    info['cname'] = ans[4]
                    info['downid'] = ans[5]
                    info['urlid'] = ans[6]
                    info['downname'] = ans[7]
    m = soup.find('div', {'class': 'm'})
    if m:
        divs = m.find_all('div')
        for div in divs:
            if div['class'] == 'tit':
                info['namec'] = div.find('a').text
                info['namee'] = div.find('span').text
            if div['class'] == 'time':
                info['time'] = div.text
            if div['class'] == 'pt':
                info['pt'] = div.text
            if div['class'] == 'type':
                info['type'] = div.text
            if div['class'] == 'zz':
                info['zz'] = div.text
            if div['class'] == 'lang':
                info['lang'] = div.text
            if div['class'] == 'fx':
                info['fx'] = div.text
    with open('data_2.txt', 'a', encoding='utf-8') as f:
        print(dumps(info, separators=(',', ':'), indent=None, ensure_ascii=False) + ',', file=f)
    # return info


def func3(a, d):
    with open(f'step3/{d}', 'w', encoding='utf-8') as f:
        print(a, file=f)
    try:
        dd = d.split('-')[0]
        info = {'number': dd}
        soup = BeautifulSoup(a, 'html.parser')
        cname = soup.find('li', {'class': 'gamecname'})
        if cname:
            info['cname'] = cname.text
        ename = soup.find('li', {'class': 'gameename'})
        if ename:
            info['ename'] = ename.text
        size = soup.find('li', {'class': 'gamesize'})
        if size:
            info['size'] = size.text
        pic = soup.find('div', {'class': 'gamepic'})
        if pic:
            img = pic.find('img')
            if img:
                info['pic'] = img.attrs['src']
        alypbox = soup.find('div', {'class': 'alypbox'})
        if alypbox:
            d = alypbox.find('a', {'id': 'alypbtn', 'class': 'down_xl'})
            if d:
                info['alypbox'] = d.attrs['href']
        newhzbdd = soup.find('div', {'class': 'newhzbdd'})
        if newhzbdd:
            d = newhzbdd.find('a', {'id': 'wpbtn', 'class': 'down_bdd'})
            if d:
                info['down_bdd'] = d.attrs['data-src']
        btbtn = soup.find('a', {'id': 'btbtn'})
        if btbtn:
            info['btbtn'] = btbtn['href']
        eks = soup.find_all('input', {'name': 'fileck'})
        if eks:
            info['btbtn'] = [ek['value'] for ek in eks]
        if info['cname']:
            with open('data_4.txt', 'a', encoding='utf-8') as f:
                print(dumps(info, separators=(',', ':'), indent=None, ensure_ascii=False) + ',', file=f)
    except Exception as e:
        print(e)
        print(a)
    # return info


def step2():
    with open('data_1.txt', 'r', encoding='utf-8') as f:
        info0s = loads(f.read())
    urls = [info0['url'] for info0 in info0s if info0['url'].startswith(r'https://down')]
    data = get(urls, func=func2, fdata=[url.split('/')[-1] for url in urls], proxy=proxy0, headers=header0)
    # with open('data_2.txt', 'a', encoding='utf-8') as f:
    #     print(dumps(data, indent=None, ensure_ascii=False) + ',', file=f)


def step3():
    # 基于data_2.txt
    # with open('data_2.txt', 'r', encoding='utf-8') as f:
    #     info0s = loads(f.read())
    # urls = [fr'https://www.soft128.com/down/{info0["downid"]}-1.html' for info0 in info0s if 'downid' in info0]
    # http://www.soft128.com:880/down/

    # 暴力
    urls = [fr'http://www.soft128.com:880/down/{x}-1.html' for x in range(4, 90000)]

    data = get(urls, func=func3, fdata=[url.split('/')[-1] for url in urls], proxy=proxy0, headers=header0)
    # with open('data_3.txt', 'w', encoding='utf-8') as f:
    #     print(dumps(data, indent=2, ensure_ascii=False), file=f)


def main():
    step1(pages=736)
    # os.makedirs('step2')
    # step2()
    # add [ del , add ]
    # os.makedirs('step3')
    # step3()
    # work(r'https://down.ali213.net/pcgame/tmosth.html')
    # work(r'https://down.ali213.net/pcgame/neophyte.html')


if __name__ == '__main__':
    main()
