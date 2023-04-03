from ez_aio.aio import get
from ez_aio import proxy0, header0
from bs4 import BeautifulSoup
from json import loads, dumps
import re


script_re = re.compile('.*sKeyword = "(.*)", odayID = \'(.*)\', clsname = \'(.*)\'.*\n'
                       '.*gamename = "(.*)", downID = \'(.*)\',urlID = \'(.*)\', downname = "(.*)".*')


def ali213_get(link0):
    a = get(link0, headers=header0, proxy=proxy0)[0]
    soup = BeautifulSoup(a, 'html.parser')
    scripts = soup.find_all('script')
    info = {}
    for script in scripts:
        if 'type' in script.attrs:
            if script.attrs['type'] == 'application/ld+json':
                x = loads(script.text)
                info['ali213_url'] = x['@id']
                info['tile'] = x['title']
                info['appid'] = x['appid']
                info['upload'] = x['upDate']
                info['publish'] = x['pubdate']
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
                    return info


def soft128_get(link0):
    a = get(link0, headers=header0, proxy=proxy0)[0]
    info = {}
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

    return info


def work(link):
    game_info = ali213_get(link)
    if game_info:
        print(dumps(game_info, indent=2, ensure_ascii=False))
        down_info = soft128_get(fr'https://www.soft128.com/down/{game_info["downid"]}-1.html')
        print(dumps(down_info, indent=2, ensure_ascii=False))


def main():
    work(r'https://down.ali213.net/pcgame/tmosth.html')


if __name__ == '__main__':
    main()
