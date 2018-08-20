from contentful import Client

client = Client(
  '9h3t1bvarz5p',
  '117a572bc204f8e4dbbb055b60903adbcc2e4f50787b98762724f7d2fe71103b'
)

post_urls = None

def get_post_urls():
    
    if post_urls == None:
        load_blog_posts()
        
    return post_urls
    
def clear_post_urls():
    global post_urls
    post_urls = None
    
def load_blog_posts():
    
    global post_urls
    post_urls = []
    
    entries = client.entries({'content_type': 'blogPost'})
    
    for post in entries:
        post_urls.append(post.url)