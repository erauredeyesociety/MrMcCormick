from selenium import webdriver
from time import sleep
from selenium.webdriver.common.keys import Keys
from random import randint

driver = webdriver.Chrome()
login_email = "develspamz@gmail.com"
login_passw = "toortoor"

# setup

def open_tinder():
    driver.get('https://tinder.com')

    sleep(2)

    login = driver.find_element('xpath', '/html/body/div[1]/div/div[1]/div/main/div[1]/div/div/div/div/header/div/div[2]/div[2]/a/div[2]/div[2]')
    login.click()
    sleep(1)
    facebook_login()

    sleep(6)
    try:
        allow_location_button = driver.find_element('xpath', '//*[@id="t-1917074667"]/main/div/div/div/div[3]/button[1]')
        allow_location_button.click()
    except:
        print('no location popup')

    try:
        notifications_button = driver.find_element('xpath', '/html/body/div[2]/main/div/div/div/div[3]/button[2]')
        notifications_button.click()
    except:
        print('no notification popup')

def facebook_login():
    # find and click FB login button
    login_with_facebook = driver.find_element('xpath', '/html/body/div[2]/main/div/div[1]/div/div/div[3]/span/div[2]/button')
    login_with_facebook.click()

    
    # save references to main and FB windows
    sleep(2)
    base_window = driver.window_handles[0]
    fb_popup_window = driver.window_handles[1]
    # switch to FB window
    driver.switch_to.window(fb_popup_window)

    # find enter email, password, login
    cookies_accept_button = driver.find_element('xpath', '/html/body/div[2]/div[2]/div/div/div/div/div[3]/button[1]')
    cookies_accept_button.click()

    # login to FB

    email_field = driver.find_element('xpath', '/html/body/div/div[2]/div[1]/form/div/div[1]/div/input')
    pw_field = driver.find_element('xpath', '/html/body/div/div[2]/div[1]/form/div/div[2]/div/input')
    login_button = driver.find_element('xpath', '/html/body/div/div[2]/div[1]/form/div/div[3]/label[2]/input')
    # enter email, password and login
    email_field.send_keys(login_email)
    pw_field.send_keys(login_passw)
    login_button.click()
    driver.switch_to.window(base_window)

# matching

def right_swipe():
    doc = driver.find_element('xpath', '//*[@id="Tinder"]/body')
    doc.send_keys(Keys.ARROW_RIGHT)

def left_swipe():
    doc = driver.find_element('xpath', '//*[@id="Tinder"]/body')
    doc.send_keys(Keys.ARROW_LEFT)

def close_match():
    match_popup = driver.find_element('xpath', '//*[@id="modal-manager-canvas"]/div/div/div[1]/div/div[3]/a')
    match_popup.click()

def auto_swipe():
    while True:
        # add some random delay
        delay = 2 + randint(1, 4)
        try:
            sleep(delay)
            right_swipe()
        except:
            close_match()

# messaging 

def get_matches():
    match_profiles = driver.find_elements('class name', 'matchListItem')
    message_links = []
    for profile in match_profiles:
        if profile.get_attribute('href') == 'https://tinder.com/app/my-likes' or profile.get_attribute('href') == 'https://tinder.com/app/likes-you':
            continue
        message_links.append(profile.get_attribute('href'))
    return message_links

def send_message(link):
    driver.get(link)
    sleep(2)
    text_area = driver.find_element('xpath', '/html/body/div[1]/div/div[1]/div/main/div[1]/div/div/div/div[1]/div/div/div[3]/form/textarea')

    text_area.send_keys('hi')

    text_area.send_keys(Keys.ENTER)

def send_messages_to_matches():
    links = get_matches()
    for link in links:
        send_message(link)
