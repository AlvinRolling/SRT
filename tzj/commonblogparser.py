from blogparser import BlogParser
from bs4 import BeautifulSoup


class CommonBlogParser(BlogParser):
    def __init__(self):
        BlogParser.__init__(self)

    def _parse_blog(self, blogsoup):
        # mid
        self.blog['mid'] = self._get_attr(blogsoup, 'mid')
        # mc
        msgsoup = blogsoup.find('div', attrs={'node-type': 'feed_list_content'})
        self.blog['mc'] = self._get_text(msgsoup)
        # rrc,rcc,rc,cc
        statsouplist = blogsoup.find_all('div', class_='WB_handle')
        if len(statsouplist) == 2:
            self.blog['rc'], self.blog['cc'] = self._parse_statistics(statsouplist[1])
            self.blog['rrc'], self.blog['rcc'] = self._parse_statistics(statsouplist[0])
        elif len(statsouplist) == 1:
            self.blog['rc'], self.blog['cc'] = self._parse_statistics(statsouplist[0])
        # run, ruid
        ruinfosoup = blogsoup.find(attrs={'node-type': 'feed_list_originNick'})
        if ruinfosoup:
            self.blog['run'] = self._get_attr(ruinfosoup, 'nick-name')
            self.blog['ruid'] = self._get_attr(ruinfosoup, 'usercard')
        # rmc
        rmcsoup = blogsoup.find(attrs={'node-type': 'feed_list_reason'})
        self.blog['rmc'] = self._get_text(rmcsoup)
        # rpt,rpage,page,pt,srn
        fromsouplist = blogsoup.find_all('div', class_='WB_from')
        if len(fromsouplist) == 2:
            page, pt, srn = self._parse_blog_from(fromsouplist[0])
            self.blog['rpage'] = page
            self.blog['rpt'] = pt
            self.blog['page'], self.blog['pt'], self.blog['srn'] = self._parse_blog_from(fromsouplist[1])
        elif len(fromsouplist) == 1:
            self.blog['page'], self.blog['pt'], self.blog['srn'] = self._parse_blog_from(fromsouplist[0])
        
        return self.blog


if __name__ == '__main__':
    from downloader import Downloader
    
    parser = CommonBlogParser()
    url = 'http://weibo.com/p/1005051995234631/home?is_search=0&visible=0&is_tag=0&profile_ftype=1&page=2'
    #url = 'http://weibo.com/p/1005051059713187/weibo?count=15&is_tag=0&is_search=0&pre_page=10&profile_ftype=1&visible=0&pagebar=0&page=10'
    cookie = 'SINAGLOBAL=1741986363194.8828.1402790278112; __gads=ID=c89a3aae13e8c3fb:T=1439276319:S=ALNI_Ma4dDrxRssSQmWPGRnmbUMuXggH2g; myuid=5680912796; wvr=6; un=595463155@qq.com; YF-V5-G0=8a3c37d39afd53b5f9eb3c8fb1874eec; SUS=SID-2198840781-1440032052-GZ-s849g-460ec2d7418e98f7ba73ff0dcd5660b2; SUE=es%3Db8fb58e8d4ba85910d0316e97689dfc1%26ev%3Dv1%26es2%3D43d3a74a1a96e2740e833edf5f89531c%26rs0%3DsuKJLH8TSZ%252FcKueYVwCyEXLo1qJBX08KBoxqzd1i%252Fnl6prd08N1zoZ22dqZqxsdJcIc2lcmz8T%252F%252BiMnHemaUEyizlqtlPd%252Bn%252Fb8qTbmBGE6o4MdQW5%252FWsaW7S2Lg9fNkeD9fPjtV07YcjNWFsHm%252BLTGlUkWXd%252BMWUgOBCXcPAVM%253D%26rv%3D0; SUP=cv%3D1%26bt%3D1440032052%26et%3D1440118452%26d%3Dc909%26i%3D60b2%26us%3D1%26vf%3D0%26vt%3D0%26ac%3D0%26st%3D0%26uid%3D2198840781%26name%3D595463155%2540qq.com%26nick%3D%25E6%2589%2580%25E6%259C%2589%25E6%25B5%2581%25E6%25B5%25AA%25E7%259A%2584%25E7%25BB%2588%25E7%2582%25B9%26fmp%3D%26lcp%3D2012-01-18%252012%253A13%253A29; SUB=_2A2540VVkDeTxGeRP4loZ9C7Lwz2IHXVbp8GsrDV8PUNbu9BeLUL_kW9FBt7hnsnU013KTFZ-2PNhFYmjDg..; SUBP=0033WrSXqPxfM725Ws9jqgMF55529P9D9W56UcJIJGJ6mhRLk-T6h53C5JpX5Kzt; SUHB=03oEa-w2ygZUJX; ALF=1471568051; SSOLoginState=1440032052; _s_tentry=login.sina.com.cn; Apache=3630375503562.3906.1440032051163; ULV=1440032051224:48:18:10:3630375503562.3906.1440032051163:1439971935664; UOR=,,login.sina.com.cn; YF-Page-G0=3d55e26bde550ac7b0d32a2ad7d6fa53; WBStore=4e40f953589b7b00|undefined; YF-Ugrow-G0=4703aa1c27ac0c4bab8fc0fc5968141e'
    
    downloader = Downloader(cookie)
    content = downloader.download(url)
    content = content.replace('\\/', '/')
    w = open("C:/Users/hp1/Desktop/weibo_crawler/test8.txt","w")
    w.write(content)
    w.close()
    '''writer = open('tmp1.html', 'w')
    writer.write(content)
    writer.close()'''
    parser.init_user('1410812623')
    blogsoup = parser.parse(content)
    print blogsoup
    w = open("C:/Users/hp1/Desktop/weibo_crawler/test9.txt","w")
    w.write(blogsoup)
    w.close()
    