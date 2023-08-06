import re
import requests
import json

HEADERS = {
    "accept":"text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,*/*;q=0.8",
    "accept-encoding":"deflate",
    "accept-language":"en-US,en;q=0.8,zh-CN;q=0.6,zh;q=0.4",
    "cache-control":"no-cache",
    'user-agent':'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/81.0.4044.92 Safari/537.36',
}

H0 = "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/81.0.4044.92 Safari/537.36"
H1 = "Mozilla/5.0 (iPhone; CPU iPhone OS 13_2_3 like Mac OS X) AppleWebKit/605.1.15 (KHTML, like Gecko) Version/13.0.3 Mobile/15E148 Safari/604.1"


class dydownload():
    def __init__(self):
        super(dydownload, self).__init__()
        self.url = "https://v.douyin.com/JtsX7DB/"
        self.headers = HEADERS
        self.path = r'./'
        # self.url = sys.argv[1]
        # self.path = sys.argv[2]



    def __get_real_url(self):
        session = requests.Session()
        req = session.get(self.url , timeout = 5 , headers = self.headers)
        vid = req.url.split("/")[5]
        # print(vid)
        videoInfo = session.get("https://www.iesdouyin.com/web/api/v2/aweme/iteminfo/?item_ids=" + vid,
            timeout = 5 , headers = self.headers)
        # print(videoInfo.text)
        playAddr = re.findall(r'https://aweme.snssdk.com/aweme[\S]*?"',videoInfo.text)[0][:-1]
        # print(playAddr)
        parsedAddr = playAddr.replace("/playwm/","/play/")
        desc = json.loads(videoInfo.text)["item_list"][0]["desc"]
        # print(parsedAddr)
        return vid,parsedAddr,session,desc

    def __download(self, vid, info, session,desc,path):
        self.headers['user-agent'] = H1
        videoBin = session.get(info,timeout = 5, headers = self.headers)
        try:
            with open('%s\%s.mp4' % (path,desc),'wb') as fb:
                fb.write(videoBin.content)
            self.headers['user-agent'] = H0
            print("下载完成!",'%s\%s.mp4' % (path,desc))
            return "下载完成"
        except:
            with open('%s\%s.mp4' % (path,vid),'wb') as fb:
                fb.write(videoBin.content)
            self.headers['user-agent'] = H0
            print("下载完成!",'%s\%s.mp4' % (path,desc))
            return "下载完成"

    def run(self, url,path):  #
        try:
            self.url = url
            self.path = path
            vid,info,session,desc = self.__get_real_url()
            return self.__download(vid, info, session,desc,path)
        except Exception as e:
            raise e

# class dyvideo(dydownload):
#     def __init__(self):
