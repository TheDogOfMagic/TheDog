import requests
from pyquery import PyQuery as pq
from setting import BASE_HEADERS
import time


class ProxyMetaclass(type):
    def __new__(cls, name, bases, attrs):
        count = 0
        attrs['__CrawlFunc__'] = []
        for k, v in attrs.items():
            if 'crawl_' in k:
                attrs['__CrawlFunc__'].append(k)
                count += 1
        attrs['__CrawlFuncCount__'] = count
        return type.__new__(cls, name, bases, attrs)

class Crawler(object, metaclass=ProxyMetaclass):
    def get_proxies(self, callback):
        '''
        动态调用抓取代理方法
        '''
        proxies = []
        for proxy in eval("self.{}()".format(callback)):
            print('成功获取到代理', proxy)
            proxies.append(proxy)
        return proxies
       
    def crawl_daili66(self, page_count = 5):
        '''
        抓取66代理网的代理 www.66ip.cn
        page_count = 页码
        return 代理
        '''
        start_url = 'http://www.66ip.cn/{}.html'
        urls = [start_url.format(page) for page in range(1, page_count + 1)]
        for url in urls:
            print('Crawling', url)
            html = get_page(url)
            if html:
                doc = pq(html)
                trs = doc('.containerbox table tr:gt(0)').items()
                for tr in trs:
                        ip = tr.find('td:nth-child(1)').text()
                        port = tr.find('td:nth-child(2)').text()
                        position = tr.find('td:nth-child(3)').text()
                        position = position.encode('iso-8859-1') 
                        position = position.decode('gbk').encode('utf-8').decode('utf-8')
                        yield ':'.join([ip, port])+'('+position+')'
    
    def crawl_ip3300(self, page_count = 5):
        '''
        抓取云代理 www.ip3366.net
        page_count = 页码
        return 代理
        '''
        for page in range(1, page_count+1):
            start_url = 'http://www.ip3366.net/free/?stype=1&page={}'.format(page)
            html = get_page(start_url)
            if html:
                doc = pq(html)
                trs = doc('.table-bordered tr:gt(0)').items()
                for tr in trs:
                    ip = tr.find('td:nth-child(1)').text()
                    port = tr.find('td:nth-child(2)').text()
                    position = tr.find('td:nth-child(5)').text()
                    position = position.encode('iso-8859-1') 
                    position = position.decode('gbk').encode('utf-8').decode('utf-8')
                    yield ':'.join([ip, port])+'('+position+')'

    def crawl_kuaidaili(self, page_count = 5):
        '''
        抓取快代理 www.kuaidaili.com
        page_count = 页码
        return 代理
        '''
        for page in range(1, page_count+1):
            start_url = 'http://www.kuaidaili.com/free/inha/{}/'.format(page)
            html = get_page(start_url)
            if html:
                doc = pq(html)
                trs = doc('.table-bordered tr:gt(0)').items()
                for tr in trs:
                    ip = tr.find('td:nth-child(1)').text()
                    port = tr.find('td:nth-child(2)').text()
                    position = tr.find('td:nth-child(5)').text()
                    yield ':'.join([ip, port])+'('+position+')'

    def crawl_xicidaili(self, page_count = 4):
        '''
        抓取西刺代理 www.xicidaili.com
        常返回503状态码
        page_count = 页码
        return 代理
        '''
        for page in range(1, page_count+1):
            start_url = 'http://www.xicidaili.com/nn/{}/'.format(page)
            html = get_page(start_url)
            if html:
                doc = pq(html)
                trs = doc('#ip_list tr:gt(0)').items()
                for tr in trs:
                    ip = tr.find('td:nth-child(2)').text()
                    port = tr.find('td:nth-child(3)').text()
                    position = tr.find('td:nth-child(4)').text()
                    yield ':'.join([ip, port])+'('+position+')'

    def crawl_ip89(self, page_count = 5):
        '''
        抓取89代理 www.89ip.com
        page_count = 页码
        return 代理
        '''
        for page in range(1, page_count+1):
            start_url = 'http://www.89ip.cn/index_{}.html'.format(page)
            html = get_page(start_url)
            if html:
                doc = pq(html)
                trs = doc('.layui-table tr:gt(0)').items()
                for tr in trs:
                    ip = tr.find('td:nth-child(1)').text()
                    port = tr.find('td:nth-child(2)').text()
                    position = tr.find('td:nth-child(3)').text()
                    yield ':'.join([ip, port])+'('+position+')'

    def crawl_qudaili(self, page_count = 5):
        '''
        抓取旗云代理 www.qydaili.com
        page_count = 页码
        return 代理
        '''
        for page in range(1, page_count+1):
            start_url = 'http://www.qydaili.com/free/?action=china&page={}'.format(page)
            html = get_page(start_url)
            if html:
                doc = pq(html)
                trs = doc('.table-bordered tr:gt(0)').items()
                for tr in trs:
                    ip = tr.find('td:nth-child(1)').text()
                    port = tr.find('td:nth-child(2)').text()
                    position = tr.find('td:nth-child(5)').text()
                    yield ':'.join([ip, port])+'('+position+')'

    def crawl_daili31(self, pages = ['广东', '安徽', '江苏', '北京']):
        '''
        抓取31代理 31f.cn
        pages += [浙江， 山东， 上海， 湖南， 河南]
        pages = 页面
        return 代理
        '''
        for page in pages:
            start_url = 'http://31f.cn/region/{}/'.format(page)
            html = get_page(start_url)
            if html:
                doc = pq(html)
                trs = doc('.table-striped tr:gt(0)').items()
                for tr in trs:
                    ip = tr.find('td:nth-child(2)').text()
                    port = tr.find('td:nth-child(3)').text()
                    position = tr.find('td:nth-child(4)').text()
                    position += tr.find('td:nth-child(5)').text()
                    yield ':'.join([ip, port])+'('+position+')'
    
    def crawl_jisudaili(self, page_count = 5):
        '''
        抓取极速代理 www.superfastip.com
        page_count = 页码
        return 代理
        '''
        for page in range(1, page_count+1):
            start_url = 'http://www.superfastip.com/welcome/freeip/{}'.format(page)
            html = get_page(start_url)
            if html:
                doc = pq(html)
                trs = doc('.table-striped tr:gt(0)').items()
                for tr in trs:
                    ip = tr.find('td:nth-child(1)').text()
                    port = tr.find('td:nth-child(2)').text()
                    position = tr.find('td:nth-child(5)').text()
                    yield ':'.join([ip, port])+'('+position+')'



    # def crawl_data5u(self):
    #     start_url = 'http://www.data5u.com/free/gngn/index.shtml'
    #     html = get_page(start_url)
    #     if html:
    #         doc = pq(html)
    #         uls = doc('.wlist ul li ul:gt(0)').items()
    #     for ul in trulss:
    #         ip = ul.find('td:nth-child(2)').text()
    #         port = ul.find('td:nth-child(3)').text()
    #         position = ul.find('td:nth-child(4)').text()
    #         yield ':'.join([ip, port])+'('+position+')'

def get_page(url, options={}):
    '''
    抓取代理
    url = 代理网址
    options = 额外请求头
    return 抓取的网页
    '''
    headers = dict(BASE_HEADERS, **options)
    time.sleep(0.8)
    print('正在抓取', url)
    try:
        response = requests.get(url, headers=headers)
        if response.status_code == 200:
            print('抓取成功', url, response.status_code)
            return response.text
        else:
            print('抓取失败', response.status_code)
            return None
    except ConnectionError:
        print('抓取失败', url)
        return None


if __name__ == "__main__":
    a = Crawler()
    for i in a.crawl_jisudaili():
        print(i)
        # pass