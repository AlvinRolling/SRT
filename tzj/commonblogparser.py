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
    url = 'http://weibo.com/p/1005051995234631/home?is_search=0&visible=0&is_tag=0&profile_ftype=1&page=1'
    #url = 'http://weibo.com/p/1005051059713187/weibo?count=15&is_tag=0&is_search=0&pre_page=10&profile_ftype=1&visible=0&pagebar=0&page=10'
    downloader = Downloader()
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
    