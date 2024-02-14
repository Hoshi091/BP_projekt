from flask import Flask, render_template, request
from bs4 import BeautifulSoup
import requests
import re

import nltk
from nltk.tokenize import sent_tokenize

from selenium import webdriver 
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.chrome.service import Service as ChromeService 
from webdriver_manager.chrome import ChromeDriverManager 

import time




app = Flask(__name__)

nltk.download('punkt')


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

        

def extract_matching_sentences(soup, content_type, input_kw):
    text_elements = soup.find_all(content_type)
    if not text_elements:
        text_elements = soup.find_all('body')
    #print(content_type)
    #print(soup)
    text=""
    for element in text_elements:
        el_text = element.get_text()
        if not el_text.endswith('.'):
            el_text += '. ' 
        text += el_text + " "
    text = re.sub(r'(?<!\.)\n', '. ', text)
    sentences = sent_tokenize(text)
    print(sentences)
    pattern=[]
    for sentence in sentences:
        if input_kw.lower() in sentence.lower():
            pattern.append(sentence)
    return pattern


def extract_dynamic_content(url, content_type, input_keyword, get_full_links,get_links):
    """ options = Options()
    options.add_argument('--headless')  
    options.add_argument('--disable-gpu')
    driver = webdriver.Chrome(service=ChromeService(ChromeDriverManager().install()), options=options)
    driver.get(url)
    content = driver.page_source
    driver.quit()
    print(content)
    soup = BeautifulSoup(content, 'html.parser')
    clean_text = soup.get_text(strip=True)
    clean_text = re.sub(r'\s+', ' ', clean_text)
    return clean_text """
    options = Options()
    options.add_argument('--headless')  
    options.add_argument('--disable-gpu')
    options.add_argument('--incognito')
    driver = webdriver.Chrome(service=ChromeService(ChromeDriverManager().install()), options=options)
    driver.get(url)
    driver.implicitly_wait(10)
    driver.execute_script("window.scrollTo(0, document.body.scrollHeight);")
    time.sleep(2)
    page_source = driver.page_source
    page_source = re.sub(r'<br\s*/?>|\n', ' ', page_source)
    soup = BeautifulSoup(page_source, 'html.parser')
    driver.quit()
    result=None

    if content_type != "main":
        if content_type == "a":
            result = extract_links(soup, get_full_links, get_links)
            return result
        else:
            result = soup.find_all(content_type)
            return result
    elif input_keyword !="":
            result = extract_matching_sentences(soup, content_type, input_keyword)
            return result
    else:
        return soup


    

@app.route('/', methods=['GET', 'POST'])
def index():
    head = None

    if request.method == 'POST':
        url = request.form['url']
        source = requests.get(url).text
        content_type = request.form['content_type']
        input_keyword = request.form['keyword_input']
        get_links = request.form.get('get_links', default=False, type=bool)
        get_full_links = request.form.get('get_full_links', default=False, type=bool)
        dynamic_content = request.form.get('get_dynamic_content', default=False, type=bool)
        soup = BeautifulSoup(source, 'lxml')
        if dynamic_content:
            head = extract_dynamic_content(url, content_type, input_keyword, get_full_links,get_links)
        elif input_keyword !="":
            head = extract_matching_sentences(soup, content_type, input_keyword)
        elif content_type == "a":
            head = extract_links(soup,get_full_links,get_links)
        else:
            head = soup.find_all(content_type)

    return render_template('index.html', head=head)

if __name__ == '__main__':
    app.run(debug=True)
