import unittest

from bs4 import BeautifulSoup
from webscraper import extract_main_content, extract_links, extract_matching_sentences

class TestFunctions(unittest.TestCase):
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

    def test_extract_links_a(self):
        sample_html = '<html><body><a href="https://example.com">Link 1</a><a href="https://example.org">Link 2</a> <a href="/example.com">Link 3</a></body></html>'
        soup = BeautifulSoup(sample_html, 'html.parser')

        result = extract_links(soup, full_links=True, links=True)
        
        self.assertEqual(len(result), 2)  
        self.assertTrue(result[0].startswith('http'))

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

