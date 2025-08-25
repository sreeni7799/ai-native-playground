import requests
from bs4 import BeautifulSoup
from typing import List
import time
from urllib.parse import urljoin

class NewsAgent:
    def __init__(self, base_url: str = "https://news.ycombinator.com"):
        self.base_url = base_url
        self.session = requests.Session()
        self.session.headers.update({
            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36'
        })
    
    def fetch_headlines(self, max_headlines: int = 10) -> List[dict]:
        try:
            response = self.session.get(self.base_url)
            response.raise_for_status()
            
            soup = BeautifulSoup(response.content, 'html.parser')
            headlines = []
            
            if "news.ycombinator.com" in self.base_url:
                headlines = self._parse_hackernews(soup, max_headlines)
            elif "reddit.com" in self.base_url:
                headlines = self._parse_reddit(soup, max_headlines)
            else:
                headlines = self._parse_generic(soup, max_headlines)
            
            print(f"✓ Fetched {len(headlines)} headlines from {self.base_url}")
            return headlines
            
        except requests.RequestException as e:
            print(f"✗ Error fetching news: {e}")
            return []
    
    def _parse_hackernews(self, soup: BeautifulSoup, max_headlines: int) -> List[dict]:
        headlines = []
        title_links = soup.find_all('span', class_='titleline')
        
        for i, title_elem in enumerate(title_links[:max_headlines]):
            link_elem = title_elem.find('a')
            if link_elem:
                title = link_elem.get_text(strip=True)
                url = link_elem.get('href', '')
                if url and not url.startswith('http'):
                    url = urljoin(self.base_url, url)
                
                headlines.append({
                    'title': title,
                    'url': url,
                    'source': 'Hacker News'
                })
        
        return headlines
    
    def _parse_reddit(self, soup: BeautifulSoup, max_headlines: int) -> List[dict]:
        headlines = []
        title_elements = soup.find_all('h3', class_='_eYtD2XCVieq6emjKBH3m')
        
        for i, title_elem in enumerate(title_elements[:max_headlines]):
            title = title_elem.get_text(strip=True)
            headlines.append({
                'title': title,
                'url': '',
                'source': 'Reddit'
            })
        
        return headlines
    
    def _parse_generic(self, soup: BeautifulSoup, max_headlines: int) -> List[dict]:
        headlines = []
        
        title_selectors = ['h1', 'h2', 'h3', '.headline', '.title']
        for selector in title_selectors:
            elements = soup.select(selector)
            if elements:
                for i, elem in enumerate(elements[:max_headlines]):
                    title = elem.get_text(strip=True)
                    if len(title) > 20:
                        link_elem = elem.find('a') or elem.find_parent('a')
                        url = ''
                        if link_elem:
                            url = urljoin(self.base_url, link_elem.get('href', ''))
                        
                        headlines.append({
                            'title': title,
                            'url': url,
                            'source': 'Generic News Site'
                        })
                        
                        if len(headlines) >= max_headlines:
                            break
                break
        
        return headlines