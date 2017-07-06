import platform
from bs4 import BeautifulSoup
from selenium import webdriver
from itertools import islice


__d = "@-DEBUG:"
__start_position = 0


def main():
    # PhantomJS files have different extensions
    # under different operating systems
    if platform.system() == 'Windows':
        PHANTOMJS_PATH = 'D:/google_drive/MSc Research/implement/nlp python/classification/classification1/webscrapping/dynamic_link_extraction/test1/tools/phantomjs-2.1.1-windows/bin/phantomjs.exe'
    else:
        PHANTOMJS_PATH = 'D:/google_drive/MSc Research/implement/nlp python/classification/classification1/webscrapping/dynamic_link_extraction/test1/tools/phantomjs-2.1.1-windows'


    # here we'll use pseudo browser PhantomJS,
    # but browser can be replaced with browser = webdriver.FireFox(),
    # which is good for debugging.
    service_arg=['--load-images=false']

    browser = webdriver.PhantomJS(executable_path=PHANTOMJS_PATH,service_args=service_arg)
    print(__d,"1 here")

    __init_url = 'http://www.thedailystar.net/newspaper'




def crawl(init_url,browser):



    print(__d,"2 here")
    # let's parse our html

    l2v_file_reader = open('data/link_to_visit.bin','r+')


    parse_me(browser, init_url, l2v_file_reader)

    line_no = lates_pos()

    for current_base in islice(l2v_file_reader,line_no,None):
        parse_me(browser, current_base, l2v_file_reader)


    l2v_file_reader.close()



def put():
    pass

def pull():
    pass

def update_start():
    pass

def lates_pos():
    return __start_position


def parse_me(browser, current_base, l2v_file_reader):
    browser.get(current_base)
    soup = BeautifulSoup(browser.page_source, "html.parser")

    temp_links_file = open('data/temp_links','a+')



    for a in soup.find_all('a', href=True):
        temp_link = a['href']

        print("Found the URL:", temp_link)

        if 'http' in temp_link or 'www' in temp_link:
            temp_links_file.write(temp_link)
        else:
            if current_base[-1] != '/':
                temp_links_file.write(current_base +'/'+ temp_link)
            else:
                temp_links_file.write(current_base + temp_link)

    temp_links_file.close()




if __name__=="__main__":
    main()