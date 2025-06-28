from selenium import webdriver 
#from selenium.common.exceptions         import TimeoutException
from selenium.common.exceptions         import NoSuchElementException
from selenium.webdriver.chrome.options  import Options
from selenium.webdriver.chrome.service  import Service as ChromeService
#from selenium.webdriver.common.by       import By
#from selenium.webdriver.support         import expected_conditions as EC
#from selenium.webdriver.support.ui      import WebDriverWait

from datetime import datetime
import pandas as pd
import csv
import time
import easygui
import traceback

# Initialize Chrome driver instance
#driver = webdriver.Chrome(service=ChromeService(executable_path=ChromeDriverManager().install()))
#from webdriver_manager.chrome           import ChromeDriverManager

print("pick csv input file")
while(True):
    file_path = easygui.fileopenbox()
    print("Selected file:", file_path)
    if file_path != None:
        break
        # when valid path grabbed


# Step 1: Read the existing CSV file into a DataFrame
df = pd.read_csv(file_path)


channels = [[],[]]
fail_counter = 0
start_pos = 0 
'''
might be easier when running to keep start_pos as 0

or find where country not filled == ""
'''
counter = start_pos

number = 1000 # point to force stop, useful for sampling?
end_pos = start_pos + number
# not really using above 2

countries = []
channel_icon_LINKS = []
sub_counts = []

ALT_START = 0


about = r"/about"


non_country_ANS = ["DELETED","REMOVED","NO_EXIST","UNAVAILABLE","no idea","AUTO_GEN"]
# for channelFailFunc()

#r'sub_list\subscriptions.csv'
with open( file_path , newline='', encoding="utf8") as csvfile:
    reader = csv.reader(csvfile)
    next(reader, None)# skips header
    for row in reader:
        if row == []:
            break
        channels[0].append(row[1] + '/about') # urls
        channels[1].append(row[2]) # names
        
        # check if grabbing false row
        # throws error or ''
        ##
        #then if country (row[3]) exists and make into start pos
        # or make way to choose


### C:\Users\ [UserName] \Documents\webscraping_2
### "C:\Users\ [UserName] \Documents\my things\webscraping3\chromedriver-win64\chromedriver.exe"
path = r'\chromedriver-win64\chromedriver.exe'
# have note.txt with take chromedriver from LINK

chrome_options = Options()
# chrome_options.add_argument("--disable-extensions")
# chrome_options.add_argument("--disable-gpu")
# chrome_options.add_argument("--no-sandbox") # linux only
chrome_options.add_argument("--headless=new") # for Chrome >= 109
# chrome_options.add_argument("--headless")
# chrome_options.headless = True # also works

service = ChromeService(executable_path=path)


##################################


cookies_rejected = False
# xpath syntax: //tagName[@AttributeName="value"]
about_row_xpath = "//tr[@class='description-item style-scope ytd-about-channel-renderer']"
fifth_last_row_xpath = about_row_xpath + "[position() = (last() - 4)]//td"

START_TIME = time.time()
print("Started scraping", len(channels[0]), "channels at:", datetime.now())
try:
    while counter < len(channels[0]):
        # does following for every url
        if not cookies_rejected:
            driver = webdriver.Chrome(options=chrome_options)
            #service=service, 
        website = channels[0][counter]
        driver.get(website)
        
        
        if not cookies_rejected:
            # find_element_by_xpath() has been removed
            last_reject_cookies = driver.find_element("css selector", 'button[aria-label="Reject all"]:last-of-type')
            # "xpath", '//button[@aria-label="Reject all"][last()]'
            
            last_reject_cookies.click()
            cookies_rejected = True
        
        time.sleep(max(4, fail_counter/2)) # may need to wait
        
        # delay = max(4, fail_counter/2)
        # myElem = WebDriverWait(driver, delay).until(EC.presence_of_element_located((By.ID, 'accessibility')))
        
        ########
        
        # check current url for /about here, add it on and wait again if not
        
        inner_url = driver.current_url
        if inner_url[-6:] != about:
            driver.get(inner_url + about)
            
            time.sleep(max(4, fail_counter/2))
        
        ########
        
        def channelFailFunc(my_channel, fail_num):
            countries.append( non_country_ANS[fail_num] )
            
            if fail_num != -1:
                print("channel: " + my_channel)
                sub_counts.append("0")
                channel_icon_LINKS.append("EMPTY")
            
            match fail_num:
                case  0:
                    print("has been terminated")
                case  1:
                    print("broke guidelines")
                case  2:
                    print("does not exist")
                case  3:
                    print("unavailable")
                case -1:
                    print("Auto-generated channel: " + my_channel)
                    # these have sub counts - will let run but fix afterward
                    sub_counts.append("search for sub count")
                    
                    # image also different format
                    channel_icon_LINKS.append( driver.find_element("css selector", "#box-art img").get_attribute("src") )
                    # "xpath", '//*[@id="box-art"]/img'
                    
                    # syntax
                    # https://yt3.googleusercontent.com/UNIQUE_75_CHAR_URL=s540-w390-h540-c-k-c0x00ffffff-no-nd-rj
                    
                case _:
                    print("other problems :-(")
        
        
        try:
            driver.find_element("xpath", 
                fifth_last_row_xpath + "//yt-icon//span//div//*[local-name() = 'svg']//*[local-name() = 'path']")
            #check for globe
            
        except NoSuchElementException:
            # check if channel still exists
            try:
                channel_check = driver.find_element("css selector", "#container yt-formatted-string")
                # "xpath", '//*[@id="container"]/yt-formatted-string'
                
                channel_status = channel_check.get_attribute("innerText")
                ch1count = channels[1][counter]
                
                if   ("This account has been terminated") in channel_status:
                    channelFailFunc( ch1count, 0 )
                    counter += 1
                    
                elif ("This channel was removed")         in channel_status:
                    channelFailFunc( ch1count, 1 )
                    counter += 1
                    
                elif ("This channel does not exist")      in channel_status:
                    channelFailFunc( ch1count, 2 )
                    counter += 1
                    
                elif ("This channel is not available")    in channel_status:
                    channelFailFunc( ch1count, 3 )
                    counter += 1
                
                elif channel_status:
                    channelFailFunc( ch1count, 4 )
                    counter += 1
                
            except NoSuchElementException:
                pass
            
            # check if "Topic" channel for video games
            ## need to deal with same for music?
            try:
                channel_check = driver.find_element("css selector", "#auto-generated")
                # "xpath", '//*[@id="auto-generated"]'
                
                if ("Auto-generated by YouTube") in (channel_check.get_attribute("innerHTML")):
                    channelFailFunc( ch1count, -1 )
                    counter += 1
            except NoSuchElementException:
                pass
            
            
            fail_counter += 1
            if (fail_counter-1) % 3 == 0:
                print("try again, fails:", fail_counter)
            if fail_counter == 5:
                end_pos = counter
                break
            continue
            ## tries current channel again
            # assumes page didnt load in time
        
        ############
        
        # find elements and just save the one with text "subscriber"
        ## dont need to care about 0 subs since the user IS a sub
        # then just grab text up to first space " "
        
        
        to_find_SubCount = driver.find_elements("css selector", 
            "#page-header yt-content-metadata-view-model > div > span:first-of-type")
        # "xpath", '//*[@id="page-header"]/yt-page-header-renderer/yt-page-header-view-model/div/div[1]/div/yt-content-metadata-view-model/div/span[1]'
        # "css selector", "#page-header > yt-page-header-renderer > yt-page-header-view-model > div > div:first-of-type > div > yt-content-metadata-view-model > div > span:first-of-type"
        # will output list/array
        
        correct_SubCount = ""
        for sc in to_find_SubCount:
            sc_test_text = sc.get_attribute("innerText")
            
            sub_index = sc_test_text.find(" subscriber")
            # i should update this for different languages
            # (alternates to "subscriber")
                
            if sub_index != -1:
                correct_SubCount = sc_test_text[:sub_index]
                sub_counts.append(correct_SubCount)
                # will mult by k(1000) ,m(1,000,000) in html
                break
        else:
            #for loop never finds " subscriber"
            sub_counts.append("search for sub count")
        
        
        channel_icon_LINKS.append( driver.find_element("xpath", 
            '//div[contains(@class, "yt-spec-avatar-shape__image-overlays yt-spec-avatar-shape__image")]/preceding-sibling::img[1]'
            ).get_attribute("src") )
        
        # "css selector", 'div[class*="yt-spec-avatar-shape__image-overlays yt-spec-avatar-shape__image"] > preceding-sibling::img:first-of-type'
        
        # img class grab src ## [44:89]
        
        # https://yt3.googleusercontent.com/ytc/AIdro_UNIQUE_45_CHAR_URL=s160-c-k-c0x00ffffff-no-rj
        # some 44 and will have "=" as last - deal on html
        
        # can also be longer char url so need to check length and replace values as required
        # https://yt3.googleusercontent.com/OfM7P0tWu8buZX262SOt4ydefY4LSz0bG3O83RO7f5r2o6HR3u3vOS-mkrFLCTLR7NNwlazkbA=s160-c-k-c0x00ffffff-no-rj
        #                                  |                                                                          |
        
        # just make full text and not mess around it
        # OR 34 first and -c-k-c0x00ffffff-no-rj (-21)
        # but better in long run not to

        ########################
        
        country = driver.find_element("xpath", 
            fifth_last_row_xpath + '[@class="style-scope ytd-about-channel-renderer"][last()]')
        
        if len(country.text) == 0:
            countries.append("N/A")
            print("no country")
        else:
            countries.append((country.get_attribute("innerHTML")).replace("&amp;", "and"))
            # turn '&' into 'and' for countries like Trinidad and Tobago
            
            print(country.text)
        
        if ((counter % 100) == 0) and (counter > 0):
            print("passed another 100,", counter, "completed")
            
            progress_in_percent = counter/len(channels[0])
            print("Progress:", 100 * progress_in_percent, "%" )
            
            current_time = time.time()
            current_duration = current_time - START_TIME
            print( current_duration//60 , "minutes and", current_duration%60 ,"seconds running")
            
            projected_time = START_TIME + round( current_duration * (1/progress_in_percent) )
            projected_END_time = time.localtime( projected_time )
            print("projected end time =", time.asctime(projected_END_time) )
        
        counter+=1
        fail_counter = 0
        
        # force stop at end pos?
        #if counter >= 500:
        #    end_pos = counter
        #    break
    else:
        #reach end normally
        end_pos = counter
except Exception as e:
    print(traceback.format_exc())
    print("exception encountered")
    print("current fail_counter:", fail_counter)
    print("current counter:", counter)
    end_pos = counter+1
####################################

print("ended at:", end_pos)
driver.quit()
print("Ending time:", datetime.now())

#plan: make into string array
#then add to rows of csv doc

# Step 2: Define the values for the new column
#make function with column as input
def valuesToFullColumnRow(my_column):
    full_column = []
    
    for i in range(1, start_pos):
        full_column.append('')

    for m in my_column:
        full_column.append(m)

    for i in range(start_pos+len(my_column), len(channels[0]) ):
        full_column.append('')
        
    while len(full_column) < len(channels[0]):
        full_column.append('')
        # this is just failsafe
    
    return full_column

# Step 3: Add the new columns to the DataFrame
df['Country'] =          valuesToFullColumnRow(countries)

df['Channel icon'] =     valuesToFullColumnRow(channel_icon_LINKS)
df['Subscriber count'] = valuesToFullColumnRow(sub_counts)

# Step 4: Write the DataFrame back to the CSV file

#import os
#if not os.path.exists(directory):
#    os.makedirs(directory)
#### TRY THIS LATER


df.to_csv( (r'subs_out_' + str( len(channels[0]) ) + '_channels.csv') , index=False)
# allow pick file location?

print("SUCCESS")

################################################################################
## add:
# UI - progress bar
# grab subs and channel icon - TICK

## x path changed now first after one that matches the channel name/5th last
# [position() = (last() - 4)]
# 5th last

#////////add notification every hundred for approx time left and %
# also create output folder if doesnt exizt

### 
# put all 3 in index box at once (country, icon, count) think fine though

############################

            # UCITk7Ky4iE5_xISw9IaHqpQ,http://www.youtube.com/channel/UCITk7Ky4iE5_xISw9IaHqpQ,LordiofficialVEVO
            # caused error - see no sub showing up not sure what else - error was at country stage
            #check whether sub button exists
            # //div[@id="page-header"]/yt-page-header-renderer/yt-page-header-view-model/div/div[1]/div/yt-flexible-actions-view-model/div/button-view-model/button/div
            # //button[@aria-label="Subscribe"]/div
            # globe is IN html data for /about - subs still to fix but error at 
            
            # /about takes to new page that need own /about
            # check current url and if no /about add one on?

# refine aot with
# https://stackoverflow.com/questions/5868439/wait-for-page-load-in-selenium

######################

# skip @channelname
#if sc_test_text.find("@") == -1:
    # should be correct span
    
    

## SEE BOTTOM NOTES

# sc_test_text[ 0 : sc_test_text.find(" subscriber") ]
# is doing [0:-1] since cant find subscribe

## for loop around 260

# worked :0 
# but 9 video as sub num

#            try:
#                # testing for LACK of sub button
#                pass
#            except NoSuchElementException:
#                pass
#                # wont be pass since want to deal with no sub button