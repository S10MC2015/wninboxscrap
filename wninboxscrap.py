#Credits:
#https://stackoverflow.com/a/12657803 for venv advice
#https://realpython.com/beautiful-soup-web-scraper-python/#what-is-web-scraping for teaching me how to web scrape
#That guy on the python discord who helped me
#Another guy on python discord who helped me
#Thanks to fanficfare for inadvertantly teaching me what decompose does and i really wish i knew you existed before i started this lol.
#Also thank you to fanficfare as i used your stylesheet without permission please forgive me.
#https://stackoverflow.com/a/35156699 for venv.sh thing
#Also thanks to https://towardsdatascience.com/how-to-download-an-image-using-python-38a75cfa21c for telling me how to download the cover image. 
#Also Thanks to Ghost and Ultra for the help.
#https://stackoverflow.com/a/58614037 for selenium code
#https://towardsdatascience.com/in-10-minutes-web-scraping-with-beautiful-soup-and-selenium-for-data-professionals-8de169d36319 for how to use selenium

#This is based off of my shepub thing thus has alot of comments from it

#Import all the things that will be needed
import os
import subprocess
import datetime
import logging
import time

#bs4 for parsing and requests for maybe doing requests when not using selenium.
import requests
import bs4

#START of Selenium things. selenium due to the site using js.
import selenium
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.common.exceptions import TimeoutException
from selenium.common.exceptions import NoSuchElementException
from selenium.common.exceptions import ElementNotInteractableException
#i use brave and a different chromedriver path
driver_path = "C:/Users/User/Desktop/VSC Projects/wninboxscrap/Selenium/chromedriver.exe"
brave_path = "C:/Program Files/BraveSoftware/Brave-Browser-Beta/Application/brave.exe"

option = webdriver.ChromeOptions()
option.binary_location = brave_path
# option.add_argument("--incognito") OPTIONAL
# option.add_argument("--headless") OPTIONAL
option.add_argument("user-data-dir=C:\\Users\\User\\Desktop\\VSC Projects\\wninboxscrap\\SeleniumProfile")
option.add_argument("--profile-directory=Profile 1")
#option.add_argument("--auto-open-devtools-for-tabs") #open devtools 

#kill old instance of brave
subprocess.run('taskkill /fi "WINDOWTITLE eq Notifications - Webnovel - Brave"')

# Create new Instance of brave
driver = webdriver.Chrome(executable_path=driver_path, chrome_options=option)
# END of selenium things

#logging things to both terminal and file for some of the testing
logging.basicConfig(format='%(asctime)s %(message)s \n \n', filemode="w", filename = "latest.log",level=logging.DEBUG, datefmt='%d-%m-%Y %H:%M:%S')
logging.getLogger().addHandler(logging.StreamHandler())

logging.debug("\nLogging is enabled! \n \n")

#function for current time
def gettime():
  time = datetime.datetime.now()
  gettime.timestr = time.strftime("%d-%m-%Y  %H:%M:%S")

driver.get("https://www.webnovel.com/")
driver.get("https://www.webnovel.com/notifications")
driver.refresh()

time.sleep(2)

#def check_exists_by_xpath(xpath):
#    try:
#        driver.find_element_by_xpath(xpath)
#    except NoSuchElementException:
#        return False
#    return True

#if check_exists_by_xpath('/html/body/div[8]/form/a') == True:
#  try:
#    driver.find_element_by_xpath('/html/body/div[8]/form/a').click()
#  except ElementNotInteractableException:
#    logging.debug('The "Download Webnovel App" element was not interactable/found thus the X coule not be clicked.')


try:
  driver.find_element_by_xpath('/html/body/div[8]/form/a').click()
except ElementNotInteractableException:
  logging.debug('The "Download Webnovel App" element was not interactable/found thus the X could not be clicked. (ElementNotInteractableException)')
except NoSuchElementException:
  logging.debug('The "Download Webnovel App" element was not interactable/found thus the X could not be clicked. (NoSuchElementException)') 

driver.execute_script("window.scrollTo(0, document.body.scrollHeight);var lenOfPage=document.body.scrollHeight;return lenOfPage;")

lenOfPage = driver.execute_script("window.scrollTo(0, document.body.scrollHeight);var lenOfPage=document.body.scrollHeight;return lenOfPage;")
match = False
while(match == False):
  lastCount = lenOfPage
  time.sleep(3)
  lenOfPage = driver.execute_script("window.scrollTo(0, document.body.scrollHeight);var lenOfPage=document.body.scrollHeight;return lenOfPage;")
  if lastCount==lenOfPage:
    match=True


time.sleep(20)

subprocess.run('taskkill /fi "Notifications - Webnovel - Brave"')












'''

#Declares authornote normal and chapter text normal and passes variables just in case.
annorm = ""
chpnorm = ""
passes = 0
chpcontentraw = []
chptitlelist = []

#URL of SH story.
URL = input("Please put in the URL of the story. Eg. https://www.scribblehub.com/series/14190/the-novels-redemption/ \n \n")
#logging.debug("Auto URL to https://www.scribblehub.com/series/14190/the-novels-redemption/ to save dev time. \n Remove in release. \n \n")
#URL = "https://www.scribblehub.com/series/14190/the-novels-redemption/"
#logging.debug("Auto URL to https://www.scribblehub.com/series/150204/world-of-joy/ to save dev time. \n Remove in release. \n \n")
#URL = "https://www.scribblehub.com/series/150204/world-of-joy/"


#Requests the story startpage and stores the html code into startpage variable. Then uses BeautifulSoup to get the actual contents.
startpage = requests.get(URL)
sphtml = bs4.BeautifulSoup(startpage.text, 'lxml')

#gets current time with function and then logs it
gettime()
starttime = "Start Time of Scraping: %s" %(gettime.timestr)
starttimetime = gettime.timestr.replace("  "," ")
logging.debug(starttime)

#Finds the element for author name then takes the text out of it.
storytitle = sphtml.find(class_='fic_title')
storytitle = storytitle.get_text()
print("\nStory Title: " + storytitle + "\n \n")

#Finds the element for author name then takes the text out of it.
authorname = sphtml.find(class_='auth_name_fic')
authorname = authorname.get_text()
print("Author: " + authorname + "\n \n")


latestchpupload = sphtml.find(class_='fic_date_pub')
latestchpupload = latestchpupload['title']
print("Latest Chapter Upload Time: " + latestchpupload + "\n \n")

#Finds element for synopsis then finds all text in the <p> tags. Then it adds then to the variable with line breaks.
synopsisraw = sphtml.find(class_='wi_fic_desc')
if synopsisraw.find(class_='seriesna'):
  synopsis = "No Synopsis found."
  synopsisraw = "<p>No Synopsis found</p>"
  pass
else:
  synopsisrawp = synopsisraw.find_all('p')
  synopsis = ""
  for i in synopsisrawp:
    synopsis += i.get_text() + "\n \n"
  print("Synopsis: " + synopsis + "\n \n")

#Finds element for genre then finds all elements with <a> tag then takes all text out and adds comma+space. Next it adds an extra space to last one and replaces comma+space+space with a full stop.
genreraw = sphtml.find(class_='wi_fic_genre')
if genreraw.find(class_='seriesna'):
  genre = "No Genres found."
  genreraw = "<p>No Genres found</p>"
  pass
else:
  genrerawp = genreraw.find_all('a')
  genre = ""
  for i in genrerawp:
    genre += i.get_text() + ", "
  genre += " "
  genre = genre.replace(",  ",".")
  print("Genre: " + genre + "\n \n")


#Finds element for tags then finds all elements with <a> tag then takes all text out and adds comma+space. Next it adds an extra space to last one and replaces comma+space+space with a full stop.
tagsraw = sphtml.find(class_='wi_fic_showtags_inner')
if tagsraw.find(class_='seriesna'):
  tags = "No Tags found."
  tagsraw = "<p>No Tags found</p>"
  pass
else:
  tagsrawp = tagsraw.find_all('a')
  tags = ""
  for i in tagsrawp:
    tags += i.get_text() + ", "
  tags += " "
  tags = tags.replace(",  ",".")
  print("Tags: " + tags + "\n \n")

#Finds element for the read button then finds the hyperlink url.
firstchpurl = sphtml.find(class_='read_buttons')
firstchpurl = firstchpurl.find('a')['href']
if firstchpurl == None:
  logging.debug("No Chapters found. Exiting.")
  exit()
else:
  print("First Chapter URL: " + firstchpurl + "\n \n")

#Finds the element for coverimage then takes the image source url out of it.
coverimageurl = sphtml.find(class_='fic_image')
coverimageurl = coverimageurl.find('img')['src']
print("CoverImage URL: " + coverimageurl + "\n \n")


#create book uid but i am an idiot.
bookid = URL
bookid = bookid.replace("https://","")
bookid = bookid.replace("http://","")
bookid = bookid.replace("www.scribblehub.com/read/","")
bookid = bookid.replace("www.scribblehub.com/series/","")
bookid = bookid.replace("/","")
bookid = bookid.replace("-","")
bookid = bookid.replace("_","")

#set some of the things for the book
book.set_identifier(bookid)
book.set_title(storytitle)
book.set_language('en')
book.add_author(authorname)
book.add_metadata('DC', 'description', synopsis)

synopsisbook = str(synopsisraw)

ch0fix = bs4.BeautifulSoup('<html><meta http-equiv="Content-Type" content="application/xhtml+xml; charset=utf-8" /><body><h2>'+ storytitle +'</h2><h3> Details about the story.</h3><p>Created by: '+ authorname +'</p><p>Last Chapter Upload: '+ latestchpupload +'</p><p></p><p>Genre: '+ genre +'</p><p></p><p>Tags: '+ tags +'</p><p></p><p>Scrapped at: '+ starttimetime +'</p><p>Ebook made using SHepub.</p><p></p><p>Synopsis: '+ synopsisbook +'</p></body></html>', features="lxml")

ch0 = epub.EpubHtml(title='Details',
                   file_name='OEBPS/details.xhtml',
                   lang='en')

ch0fix = ch0fix.prettify()
ch0fix = ch0fix.replace("\n","")
ch0fix = ch0fix.replace("  ","")
ch0fix = ch0fix.replace("> <","><")

ch0.content = ch0fix


style = 'body { font-family: Open Sans, Lato;}'#  background-color: #ffffff; text-align: justify; margin: 2%; adobe-hyphenate: none; } pre { font-size: x-small; } h1 { text-align: center; } h2 { text-align: center; } h3 { text-align: center; } h4 { text-align: center; } h5 { text-align: center; } h6 { text-align: center; } .CI { text-align:center; margin-top:0px; margin-bottom:0px; padding:0px; } .center {text-align: center;} .cover {text-align: center;} .full     {width: 100%; } .quarter  {width: 25%; } .smcap {font-variant: small-caps;} .u {text-decoration: underline;} .bold {font-weight: bold;} .big { font-size: larger; } .small { font-size: smaller; }'

nav_css = epub.EpubItem(uid="style_nav",
                        file_name="style\nav.css",
                        media_type="text/css",
                        content=style)

ch0.add_item(nav_css)

book.add_item(ch0)

book.toc = [ch0]
book.spine = ['cover',ch0]

URL = firstchpurl

def chpdata(URL,passes):

  passes += 1

  #Requests the chapter page and stores the html code into chapter variable. Then uses BeautifulSoup to get the actual contents.
  chapter = requests.get(URL)
  chphtml = bs4.BeautifulSoup(chapter.text, 'lxml')

  #make it faster by straining
  chphtml = chphtml.find(id="primary")

  #Finds the element for chapter title then takes the text out of it.
  chptitle = chphtml.find(class_='chapter-title')
  chptitle = chptitle.get_text()
  print("Chapter Title: " + chptitle + "\n \n")

  #Declares authornote normal and chapter text normal variables
  annorm = ""
  chpnorm = ""

  #Finds element for authornote then finds all elements with <a> tag then takes all text with element tags out.
  anraw = chphtml.find(class_='wi_authornotes_body')
  

  #Finds element for chaptertext then finds all elements with <p> tag then takes all text with element tags out. If it finds the authornotes elements inside, it will decompose them.
  chpraw = chphtml.find(id='chp_raw')
  if chpraw.find(class_='sp-wrap sp-wrap-default'):
    chpraw.find(class_='sp-wrap sp-wrap-default').decompose()

  if chpraw.find(class_='wi_authornotes'):
    chpraw.find(class_='wi_authornotes').decompose()

  if anraw == None:
    chpcontentsingle = ("%s" % (chpraw))
  else:
    chpcontentsingle = ("%s Author Notes: %s" % (chpraw, anraw))

  chpcontentsingle = chpcontentsingle.replace("\n","")
  #chpcontentsingle = chpcontentsingle.replace("\'","")
  chptitle = chptitle.replace("\n","")
  #chptitle = chptitle.replace("\'","")

  chpcontentsinglefix = bs4.BeautifulSoup('<html><link href="stylesheet.css" type="text/css" rel="stylesheet"/><meta http-equiv="Content-Type" content="application/xhtml+xml; charset=utf-8" /><body><h2>'+ chptitle +'</h2><p></p>'+ chpcontentsingle +'</body></html>', features="lxml")
  
  chptitlelist.append(chptitle)
  chpcontentraw.append(chpcontentsinglefix)

  #Finds element for the read button then finds the hyperlink url.
  nextchpurl = chphtml.find(class_='btn-wi btn-next')
  if nextchpurl == None:
    chppathnum = 1
    chpcontent = []
    gettime()
    endtimetime = gettime.timestr
    endtime = str("End Time of Scraping: " + endtimetime)
    logging.debug(endtime)
    print("Passes: ", passes)
    chpcontentlen = len(chpcontentraw)
    print("This should be the same number as passes. \n chpcontentraw.len() = ", chpcontentlen)

    for i in range(len(chpcontentraw)):
        chppath = 'OEBPS/ch%s.xhtml' % str(chppathnum)
        chpcontent.append(epub.EpubHtml(title=chptitlelist[i], file_name=chppath, lang='en'))

        chpcontentraw[i] = chpcontentraw[i].prettify()
        chpcontentraw[i] = chpcontentraw[i].replace("\n","")
        #chpcontentraw[i] = chpcontentraw[i].replace("  ","")
        #chpcontentraw[i] = chpcontentraw[i].replace("> <","><")

        chpcontent[i].content = chpcontentraw[i]
        chpcontent[i].add_item(nav_css)
        book.add_item(chpcontent[i])
        book.spine.append(chpcontent[i])
        book.toc.append(chpcontent[i])
        chppathnum += 1

    logging.debug(chpcontent)

    book.add_item(nav_css)
    book.add_item(epub.EpubNcx())
    #book.add_item(epub.EpubNav()) #this doesnt work for whatever reason
    endtimetitle = endtimetime.replace(":","-")
    epubtitle = '{0} (Scrapped at {1}).epub'.format(storytitle, endtimetitle)
    epub.write_epub(epubtitle, book, {})
    os.remove("cover.jpg")
    exit()
  else:
    nextchpurl = nextchpurl['href']
    logging.debug("Next Chapter URL: " + nextchpurl + "\n \n \n \n")
    print("Passes: ", passes)
    chpdata(nextchpurl,passes)


chpdata(firstchpurl,passes)

'''
