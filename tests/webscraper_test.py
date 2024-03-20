import unittest

from bs4 import BeautifulSoup
from nltk.corpus import stopwords
from webscraper import extract_main_content, extract_links, extract_matching_sentences, remove_stopwords, lemmas, remove_numbers


class TestFunctions(unittest.TestCase):
    
    def test_extract_main_content_no_main_tag(self):
        sample_html = '<html><body><div><p>Test paragraph 1</p><p>Test paragraph 2</p></div></body></html>'
        soup = BeautifulSoup(sample_html, 'html.parser')

        result = extract_main_content(soup)

        self.assertEqual(len(result), 1) 
        self.assertEqual(result[0].name, 'body')

    def test_extract_main_content(self):
        sample_html = '<html><body><main><div><p>Test paragraph 1</p><p>Test paragraph 2</p></div></main></body></html>'
        soup = BeautifulSoup(sample_html, 'html.parser')

        result = extract_main_content(soup)

        self.assertEqual(len(result), 1) 
        self.assertEqual(result[0].name, 'main')
    
    def test_extract_links_a(self):
        sample_html = '<html><body><a href="https://example.com">Link 1</a><a href="https://example.org">Link 2</a></body></html>'
        soup = BeautifulSoup(sample_html, 'html.parser')

        result = extract_links(soup, full_links=False, links=False)
        
        self.assertEqual(len(result), 2)  

    def test_extract_links_href(self):
        sample_html = '<html><body><a href="https://example.com">Link 1</a><a href="https://example.org">Link 2</a> <a href="/example.com">Link 3</a></body></html>'
        soup = BeautifulSoup(sample_html, 'html.parser')

        result = extract_links(soup, full_links=False, links=True)
        
        self.assertEqual(len(result), 3)  

    def test_extract_full_links(self):
        sample_html = '<html><body><a href="https://example.com">Link 1</a><a href="https://example.org">Link 2</a> <a href="/example.com">Link 3</a></body></html>'
        soup = BeautifulSoup(sample_html, 'html.parser')

        result = extract_links(soup, full_links=True, links=True)
        
        self.assertEqual(len(result), 2)  
        self.assertTrue(all(link.startswith('http') for link in result))

    def test_extract_links_no_links(self):
        sample_html = '<html><body><p>No links here</p></body></html>'
        soup = BeautifulSoup(sample_html, 'html.parser')

        result = extract_links(soup, full_links=False, links=False)
        
        self.assertEqual(len(result), 0)

    def test_extract_matching_sentences(self):
        sample_html = '<html><body><p>This is a sample sentence. Another sentence here. This sentence has the sample too. This one does not.</p> <span>This is not a paragraph sample</span></body></html>'
        soup = BeautifulSoup(sample_html, 'html.parser')

        result = extract_matching_sentences(soup, content_type='p', input_kw='sample', get_links=False, get_full_links=False)
        
        self.assertEqual(len(result), 2) 
        self.assertIn('sample', result[0].lower())
    
    def test_extract_matching_sentences_in_links(self):
        sample_html = '<html><body><a href="https://example.com">Link 1</a><a href="https://example.org">Link 2</a> <a href="/example.com">Link 3</a> <p>Non link test</p></body></html>'
        soup = BeautifulSoup(sample_html, 'html.parser')

        result = extract_matching_sentences(soup, content_type='a', input_kw='example', get_links=True, get_full_links=True)
        
        self.assertEqual(len(result), 2) 
        self.assertIn('example', result[0].lower())

    def test_remove_stopwords(self):
        main_text = "This is a test sentence for stopwords."
        language_choice = 'en'
        result = remove_stopwords([main_text], stopwords, language_choice)
        self.assertEqual(result, "test sentence stopwords.")

    def test_lemmas(self):
        main_text = "This is a test sentence for trying out lemmatization"
        language_choice = 'en'
        result = lemmas(main_text, language_choice)
        self.assertEqual(result, ['this', 'be', 'a', 'test', 'sentence', 'for', 'try', 'out', 'lemmatization'])

    def test_remove_numbers(self):
        main_text = "This is a test sentence with numbers 123 and (456)."
        result = remove_numbers(main_text)
        self.assertEqual(result, "This is a test sentence with numbers  and .")


