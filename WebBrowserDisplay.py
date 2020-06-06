#!/usr/bin/env python
#coding:utf-8
#簡易利用Windows/Linux Chrome Browser當成播放器使用,Windows/Linux需要些不同的條件及chromedriver.exe的版本
#You may need as:
#sudo pip install selenium

import time
from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from multiprocessing import Process, Pipe

#options=webdriver.Chromeoptions()
#options.add_argument("proxy-server-http://110,73,2.24818123)
#options.add_argument('lang=zh_CN.UTF-8')
#driver = webdriver.Chrome(chrome_options = options)
chrome_driver = "chromedriver.exe"  #chromedriver.exe執行檔所存在的路徑(2.46 version)

def run_ProcessingA():
    web = webdriver.Chrome(chrome_driver)
    web.set_window_position(0,0) #瀏覽器位置
    web.set_window_size(720,768) #瀏覽器大小
    web.get('http://www.cwb.gov.tw/V7/')
    #window='window.open("http://www.cwb.gov.tw/V7/");'
    #web.execute_script(window)
    '''
    web.find_element_by_link_text('天氣預報').click() #點擊頁面上"天氣預報"的連結
    '''
    while True:
        time.sleep(0.5)
    time.sleep(5)
    #web.close() #關閉視窗
    web.quit() #關閉所有視窗
    return

def run_ProcessingB():
    #handles = web.window_handles
    # handles為一個陣列：handles = [視窗1，視窗2，...]
    # 視窗切換，切換為新開啟的視窗
    #web.switch_to_window(handles[-1])
    # 切換回最初開啟的視窗
    #web.switch_to_window(handles[0])

    newweb = webdriver.Chrome(chrome_driver)
    newweb.set_window_position(725,0) #瀏覽器位置
    newweb.set_window_size(520,768) #瀏覽器大小
    newwindow='window.open("https://www.exosite.io/business/auth/login");'
    newweb.execute_script(newwindow)
    '''
    UserName= ('#####')
    UserPass= ('#####')
    newweb.find_element_by_id('account').send_keys(UserName)
    newweb.find_element_by_id('password').send_keys(UserPass)
    newweb.find_element_by_id('password').send_keys(Keys.ENTER)
    newweb.save_screenshot('test.png')  
    '''
    while True:
        time.sleep(0.5)
    time.sleep(5)
    #newweb.close() #關閉視窗
    newweb.quit() #關閉所有視窗
    return


class ProcessingA(Process):
    def __init__(self, pipe):
        Process.__init__(self)
        self.pipe = pipe    #duplex = False 創建單向管道（默認為雙向）

    def run(self):
        #self.pipe.send('Consumer Words')   
        #print ('Consumer Received:%s' % self.pipe.recv())
        run_ProcessingA()
        pass

    #def stop(self):
        #self.web.quit() #關閉所有視窗

class ProcessingB(Process):
    def __init__(self, pipe):
        Process.__init__(self)
        self.pipe = pipe        #duplex = False 創建單向管道（默認為雙向）

    def run(self):
        #print ('Producer Received:%s' % self.pipe.recv())
        #self.pipe.send('Producer Words')
        run_ProcessingB()
        pass

    #def stop(self):
        #self.newweb.quit() #關閉所有視窗


if __name__ == '__main__':
    pipe = Pipe()
    a = ProcessingA(pipe[0])
    b = ProcessingB(pipe[1])
    a.daemon = True     #守護設置為True，則當父進程結束後，子進程會自動被終止
    b.daemon = True     #守護設置為True，則當父進程結束後，子進程會自動被終止
    a.start()
    b.start()
    a.join()            #It will be waitting processing A 子進程都執行完了, windows唉
    b.join()            #It will be waitting processing B 子進程都執行完了, windows唉
    print ('Done!')     #done