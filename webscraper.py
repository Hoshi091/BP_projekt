from flask import Flask, redirect, render_template, request, url_for
from bs4 import BeautifulSoup
import requests
import re

import tkinter
from tkinter import filedialog


import nltk
from nltk.tokenize import sent_tokenize
from nltk.corpus import stopwords

import stanza

from selenium import webdriver 
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.chrome.service import Service 
from selenium.webdriver.common.by import By
from webdriver_manager.chrome import ChromeDriverManager 
from selenium.common.exceptions import TimeoutException, NoSuchElementException

import time
import os



app = Flask(__name__)


app.secret_key = os.urandom(24)
nltk.download('punkt')
nltk.download('stopwords')

def extract_main_content(soup):
    main_content = soup.find_all('main')
    if not main_content:
        main_content = soup.find_all('body')
    for tag in main_content:
        inline_content = tag.find_all(['p', 'span', 'td', 'th', 'a', 'h1', 'h2', 'h3', 'h4', 'h5', 'h6'])
        for element in inline_content:
            element.insert_before(' ')
            element.insert_after(' ')
    return main_content
    

def extract_links(soup, full_links, links):
        if links:
            links_list = []
            content=soup.find_all("a")

            for element in content:
                temp = element.get("href")
                if full_links and temp.startswith("http"):
                    links_list.append(temp)
                elif not full_links:
                    links_list.append(temp)
            return links_list
        else:
            return soup.find_all("a")

        
def extract_matching_sentences(soup, content_type, input_kw, get_links, get_full_links):
    if content_type == "a" and get_links:
        links = extract_links(soup, get_full_links, get_links)
        text = '. '.join(map(str, links))
    else:
        text_elements = soup.find_all(content_type)
        if not text_elements:
            text_elements = soup.find_all('body')
        text=""
        for element in text_elements:
            inline_content = element.find_all(['p', 'span', 'td', 'th', 'a', 'h1', 'h2', 'h3', 'h4', 'h5', 'h6'])
            for el in inline_content:
                el.insert_after('. ')
            el_text = element.get_text()
            if not el_text.endswith('.'):
                el_text += '. ' 
            text += el_text + " "
    text = re.sub(r'(?<!\.)\n', '. ', text)
    sentences = sent_tokenize(text)
    pattern=[]
    for sentence in sentences:
        if input_kw.lower() in sentence.lower():
            pattern.append(sentence)
    return pattern


def extract_dynamic_content(url, content_type, input_keyword, get_full_links,get_links):
    options = Options()
    options.add_argument('--headless')  
    options.add_argument('--disable-gpu')
    options.add_argument('--incognito')
    driver = webdriver.Chrome(service=Service(ChromeDriverManager().install()), options=options)
    driver.get(url)
    

    try:
        WebDriverWait(driver, 10).until(expected_conditions.presence_of_all_elements_located)
    except TimeoutException:
        print("Timed out on the page load")
        return None

    
    dismiss_popups(driver)
    page_source=""
    pagination_usage = request.form.get('pagination_scrape', default=False, type=bool)
    if pagination_usage:
        pagination_count = 0
        pagination_count = int(request.form['pagination_count'])
        original_url = driver.current_url
        if pagination_count>0:
            pagination_texts = ['Next', 'next', 'Next Page', 'Next page', '>','›', 'Continue', 'Next >', 'Forward', 'More', 'Proceed', 'Next »', 'Ďalej', 'Ďalej>', 'Ďalšie', 'Ďalšie >', 'Ďalšia', 'Ďalšia strana', 'Ďalšia >', 'Ďalšia strana >', 'Pokračovať', 'Pokračovať >', 'Nasledujúca stránka']
            for i in range(1,pagination_count+1):
                page_source += driver.page_source
                next_button = None
                for text in pagination_texts:
                    try:
                        next_button = driver.find_element(By.XPATH, f"//a[contains(text(), '{text}')]")
                        break 
                    except NoSuchElementException:
                        pass
                """if not next_button:  # If no button found, try finding it as a link element
                    try:
                        next_button = driver.find_element(By.CSS_SELECTOR, 'link[rel="next"]')
                    except NoSuchElementException:
                        next_button = None
                        pass"""       
                if next_button:
                    print("Next button found")
                    previous_url = driver.current_url
                    dismiss_popups(driver)
                    driver.execute_script("arguments[0].click();", next_button)
                    time.sleep(2)  
                    url = driver.current_url
                    driver.get(url)
                    if url == previous_url:
                        break
                else:
                    print("Next button not found")
                    next_page_url = construct_next_page_url(original_url, i+1)  
                    print(next_page_url)
                    response = requests.get(next_page_url)
                    if response.status_code == 200:
                        driver.get(next_page_url)
                        time.sleep(2)
                    else:
                        driver.execute_script("window.scrollTo(0, document.body.scrollHeight);")
                        time.sleep(2)
                        if driver.execute_script("return window.innerHeight + window.pageYOffset") >= driver.execute_script("return document.body.scrollHeight"):
                            print("Reached end of page")
                            break
                        break

    else:
        page_source += driver.page_source
    
    if content_type != "a":
        page_source = re.sub(r'<br\s*/?>|\n', ' ', page_source)
        page_source = re.sub(r'\.(?![\"”\)\]])', '. ', page_source) 
        page_source = re.sub(r'\?(?![\"”\)\]])', '? ', page_source) 
        page_source = re.sub(r'\!(?![\"”\)\]])', '! ', page_source) 
    driver.quit()
    soup = BeautifulSoup(page_source, 'html.parser')
    result=None

    if input_keyword != "":
        result = extract_matching_sentences(soup, content_type, input_keyword, get_links, get_full_links)
        return result
    elif content_type == "main":
        result = extract_main_content(soup)
        return result
    elif content_type == "a" and input_keyword =="":
        result = extract_links(soup, get_full_links, get_links)
        return result
    else:
        result = soup.find_all(content_type)
        return result
    
   
    
def construct_next_page_url(base_url, page_number):
    query_param_url = f"{base_url}?page={page_number}"
    
    response = requests.get(query_param_url)
    print(response)
    if response.status_code != 404:
        return query_param_url
    
    patterns = [
        f"{base_url.rstrip('/')}/page/{page_number}",
        f"{base_url}&page={page_number}",
        f"{base_url}?page_num={page_number}",
        f"{base_url}?strana={page_number}"
    ]
    
    for pattern in patterns:
        response = requests.get(pattern)
        print(pattern)
        print(response)
        if response.status_code == 200:
            return pattern

    return patterns[-1]


def dismiss_popups(driver):
    try:
        accept_button = driver.find_element(By.XPATH, '//button[contains(text(), "Accept") or contains(text(), "Accept All") or contains(text(), "Accept cookies") or containts(text(), " OK, got it") or contains(text(), "Accept & Continue") or contains(text(), "Continue") or contains(text(), "Povoliť") or contains(text(), "Povoliť všetko") or contains(text(), "Súhlasím") or contains(text(), "Súhlasím s používaním súborov cookies") or contains(text(), "Prijať všetky súbory cookies") or contains(text(), "Súhlasím so všetkými cookies") or contains(text(), "Potvrdiť")]')
        driver.execute_script("arguments[0].scrollIntoView();", accept_button)
        accept_button.click()
        print("Popup dismissed successfully.")
    except NoSuchElementException:
        try:
            accept_button = driver.find_element(By.XPATH, '//a[contains(text(), "Accept") or contains(text(), "Accept All") or contains(text(), "Accept cookies") or containts(text(), " OK, got it") or contains(text(), "Accept & Continue") or contains(text(), "Continue") or contains(text(), "Povoliť") or contains(text(), "Povoliť všetko") or contains(text(), "Súhlasím") or contains(text(), "Súhlasím s používaním súborov cookies") or contains(text(), "Prijať všetky súbory cookies") or contains(text(), "Súhlasím so všetkými cookies") or contains(text(), "Potvrdiť")]')
            driver.execute_script("arguments[0].scrollIntoView();", accept_button)
            accept_button.click()
            print("Popup dismissed successfully.")
        except NoSuchElementException:
            print("Accept button not found.")
    except Exception:
        print("Error occurred while dismissing popup:", Exception)
    except:
        pass

def load_from_file(path):
    with open(path, 'r', encoding='utf-8') as file:
        loaded_content = [line.strip() for line in file]
    
    return loaded_content


def remove_stopwords(main_text, stop_words, language_choice):
    if language_choice == 'sk':
        picked_stopwords = load_from_file('stopwords-sk.txt')
    else:
        picked_stopwords = stop_words.words('english')
    
    print(picked_stopwords)
    filtered_texts=  [' '.join([word for word in string.split() if word.lower() not in picked_stopwords]) for string in main_text] 
    return ' '.join(filtered_texts)

def lemmas(main_text, language_choice):
    if language_choice == 'sk':
        nlp = stanza.Pipeline(lang='sk', processors='tokenize,mwt,pos,lemma')
    else:
        nlp = stanza.Pipeline(lang='en', processors='tokenize,mwt,pos,lemma')
    doc = nlp(main_text)
    lemmas = [word.lemma for sent in doc.sentences for word in sent.words]
    return lemmas 

def remove_numbers(main_text):
    if isinstance(main_text, list):
        main_text = ' '.join(main_text)
    return re.sub(r'[\(\[\{]\d+–?\d*[\)\]\}]|\d', '', main_text)

def save_to_file(data, file_name):
    parsed_data = BeautifulSoup(data, 'html.parser')
    final_data = parsed_data.get_text()
    final_data = re.sub(r'\s+', ' ', final_data)
    final_data = final_data.lstrip('[').rstrip(']')
    final_data = final_data.strip()

    root = tkinter.Tk()
    root.withdraw() 

    destination_folder = filedialog.askdirectory(title="Select Destination Folder")

    if destination_folder:
        file_path = os.path.join(destination_folder, f"{file_name}.txt")
        try:
            with open(file_path, 'w', encoding='utf-8') as f:
                f.write(final_data)
            return True
        except Exception:
            return False
    else:
        print("No destination folder selected.")
        return False

    


@app.route('/', methods=['GET', 'POST'])
def index():
    head = None
    language_choice = ""

    if request.method == 'POST':
        url = request.form['url']
            
        content_type = request.form['content_type']
        input_keyword = request.form['keyword_input']
        get_links = request.form.get('get_links', default=False, type=bool)
        get_full_links = request.form.get('get_full_links', default=False, type=bool)
        dynamic_content = request.form.get('get_dynamic_content', default=False, type=bool)
        language_choice = request.form['language_picker']
        clean_stopwords = request.form.get('clean_stopwords', default=False, type=bool)
        get_lemmas = request.form.get('get_lemmas', default=False, type=bool)
        clean_numbers = request.form.get('delete_numbers', default=False, type=bool) 
        try:
            source = requests.get(url).text
        except Exception:
            if language_choice == "en":
                return render_template('index.html',head="Sorry! Something went wrong", language=language_choice)
            else:
               return render_template('index.html',head="Prepáčte! Niečo sa pokazilo", language=language_choice) 


        soup = BeautifulSoup(source, 'lxml')
        if dynamic_content:
            head = extract_dynamic_content(url, content_type, input_keyword, get_full_links,get_links)
        elif input_keyword !="":
            head = extract_matching_sentences(soup, content_type, input_keyword, get_links, get_full_links)
        elif content_type == "main":
            head = extract_main_content(soup)
        elif content_type == "a" and input_keyword =="":
            head = extract_links(soup,get_full_links,get_links)
        else:
            head = soup.find_all(content_type)

    plain_text=""
    if head and content_type != "a":
        for element in head:
            if isinstance(element, str): 
                text = element.strip()
            else:
                text = element.get_text().strip()
            plain_text +=  text +' '
        plain_text = re.sub(r'\s*([,.?!;:])\s*', r'\1 ', plain_text)
        plain_text = re.sub(r'\s+', ' ', plain_text)
    if head and content_type == "a":
        for element in head:
            if isinstance(element, str): 
                text = element.strip()
            else:
                text = element.get_text().strip()
            plain_text +=  text +'\n'

    if head:
        if clean_stopwords:
            plain_text = remove_stopwords([plain_text], stopwords, language_choice)
        if get_lemmas:
            plain_text = lemmas(plain_text, language_choice)
            pass
        if clean_numbers:
            plain_text = remove_numbers(plain_text)
            pass 

    return render_template('index.html', head=plain_text, language=language_choice)

@app.route('/save', methods=['GET', 'POST'])
def save():
    try:
        data = request.form['data']
        file_name = request.form['file_name']
        language = request.form['language']
        if all([data,file_name,language]):
            saved = save_to_file(data, file_name) 

            if language == 'sk':
                if saved:
                    message = "Úspešne uložené"
                else:
                    message = "Nepodarilo sa uložiť"
                btn_message = "Opätovné dolovanie"
            else:
                if saved:
                    message = "Saved successfully"
                else:
                    message = "Failed to save"
                btn_message = "Scrape again"
            return render_template('save.html', message=message, saved=saved, btn_message = btn_message)
        else:
            return redirect(url_for('index'))
    except KeyError:
        return redirect(url_for('index'))


    

@app.route('/<path:invalid_path>')
def invalid_route(invalid_path):
    return redirect(url_for('index'))

if __name__ == '__main__':
    app.run(debug=True)
