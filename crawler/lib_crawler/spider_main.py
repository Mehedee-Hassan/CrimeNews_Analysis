import threading
from queue import Queue

import crawler.util.Counter
from crawler.lib_crawler.domain import *
from crawler.lib_crawler.general import *
from crawler.lib_crawler.spider import Spider

PROJECT_NAME = 'temp_history'
# HOMEPAGE = 'http://www.thedailystar.net/newspaper'
HOMEPAGE = 'http://www.newagebd.net/archive'
# HOMEPAGE = 'http://www.observerbd.com/'

DOMAIN_NAME = get_domain_name(HOMEPAGE)
QUEUE_FILE = PROJECT_NAME + '/queue.txt'
CRAWLED_FILE = PROJECT_NAME + '/crawled.txt'
NUMBER_OF_THREADS = 8
queue = Queue()
Spider(PROJECT_NAME, HOMEPAGE, DOMAIN_NAME)


# Create worker threads (will die when main exits)
def create_workers():
    for _ in range(NUMBER_OF_THREADS):
        t = threading.Thread(target=work)
        t.daemon = True
        t.start()

        # start every 1 minuit
        # time.sleep(60)

# Do the next job in the queue
def work():
    while True:
        url = queue.get()
        Spider.crawl_page(threading.current_thread().name, url)
        queue.task_done()

        # start in every 10 seconds
        # time.sleep(10)


# Each queued link is a new job
def create_jobs():
    for link in file_to_set(QUEUE_FILE):
        queue.put(link)
    queue.join()
    crawl()


# Check if there are items in the queue, if so crawl them
def crawl():
    queued_links = file_to_set(QUEUE_FILE)
    if len(queued_links) > 0:
        print(str(len(queued_links)) + ' links in the queue')
        create_jobs()












def Local_Main():

    print("homepage : "+HOMEPAGE+"\n\n")

    # inp = ""
    #
    # while inp != 'y' and inp != 'n':
    #     inp = input('Start from previous ? (y,n):')
    #
    #
    # if inp == 'n':
    #     f1 = open(QUEUE_FILE,'w')
    #     f1.write(HOMEPAGE)
    #     f1.close()
    #
    #     f1 = open(CRAWLED_FILE,'w')
    #     f1.write("")
    #     f1.close()




    create_workers()
    crawl()


if __name__=='__main__':
    Local_Main()

    print(crawler.util.Counter.Counter.cnt)





