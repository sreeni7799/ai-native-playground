import re
import requests
from typing import List, Dict, Optional
from urllib.parse import urlparse
import time


class RedditClient:
    """Client for fetching Reddit post comments without requiring API authentication."""
    
    def __init__(self):
        self.session = requests.Session()
        self.session.headers.update({
            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36'
        })
    
    def extract_post_id(self, reddit_url: str) -> Optional[str]:
        """Extract post ID from Reddit URL."""
        patterns = [
            r'reddit\.com/r/\w+/comments/(\w+)',
            r'redd\.it/(\w+)',
            r'/comments/(\w+)'
        ]
        
        for pattern in patterns:
            match = re.search(pattern, reddit_url)
            if match:
                return match.group(1)
        return None
    
    def fetch_post_comments(self, reddit_url: str, limit: int = 100) -> Dict:
        """
        Fetch comments from a Reddit post using the JSON API.
        
        Args:
            reddit_url: URL of the Reddit post
            limit: Maximum number of comments to fetch
            
        Returns:
            Dict containing post info and comments
        """
        post_id = self.extract_post_id(reddit_url)
        if not post_id:
            raise ValueError("Invalid Reddit URL format")
        
        # Use Reddit's JSON API endpoint
        json_url = f"https://www.reddit.com/comments/{post_id}.json?limit={limit}&sort=top"
        
        try:
            response = self.session.get(json_url)
            response.raise_for_status()
            data = response.json()
            
            if not data or len(data) < 2:
                raise ValueError("Unable to fetch post data")
            
            post_data = data[0]['data']['children'][0]['data']
            comments_data = data[1]['data']['children']
            
            post_info = {
                'title': post_data.get('title', ''),
                'author': post_data.get('author', ''),
                'score': post_data.get('score', 0),
                'num_comments': post_data.get('num_comments', 0),
                'subreddit': post_data.get('subreddit', ''),
                'created_utc': post_data.get('created_utc', 0),
                'selftext': post_data.get('selftext', ''),
                'url': reddit_url
            }
            
            comments = self._extract_comments(comments_data)
            
            return {
                'post_info': post_info,
                'comments': comments,
                'total_comments_fetched': len(comments)
            }
            
        except requests.RequestException as e:
            raise Exception(f"Error fetching Reddit data: {str(e)}")
    
    def _extract_comments(self, comments_data: List) -> List[Dict]:
        """Extract comment text and metadata from Reddit API response."""
        comments = []
        
        for comment_obj in comments_data:
            comment_data = comment_obj.get('data', {})
            
            # Skip deleted/removed comments and "more comments" objects
            if comment_data.get('kind') == 'more':
                continue
                
            body = comment_data.get('body', '')
            if not body or body in ['[deleted]', '[removed]']:
                continue
            
            comment = {
                'body': body,
                'author': comment_data.get('author', ''),
                'score': comment_data.get('score', 0),
                'created_utc': comment_data.get('created_utc', 0),
                'edited': comment_data.get('edited', False),
                'controversiality': comment_data.get('controversiality', 0),
                'depth': comment_data.get('depth', 0)
            }
            
            comments.append(comment)
            
            # Recursively extract replies
            replies = comment_data.get('replies')
            if replies and isinstance(replies, dict):
                reply_children = replies.get('data', {}).get('children', [])
                if reply_children:
                    comments.extend(self._extract_comments(reply_children))
        
        return comments
    
    def validate_reddit_url(self, url: str) -> bool:
        """Validate if the provided URL is a valid Reddit post URL."""
        reddit_patterns = [
            r'https?://(?:www\.)?reddit\.com/r/\w+/comments/\w+',
            r'https?://redd\.it/\w+'
        ]
        
        return any(re.match(pattern, url) for pattern in reddit_patterns)