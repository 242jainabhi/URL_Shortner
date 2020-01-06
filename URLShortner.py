import hashlib
# import string

class ShortenURL():
    def __init__(self):
        self.dict = {}

    def long_to_short(self, long_url):
        short_url = hashlib.md5(long_url.encode()).hexdigest()[-7:]
        if short_url not in self.dict:
            self.dict[short_url] = long_url
        return short_url

    def short_to_long(self, short_url):
        if short_url in self.dict:
            return self.dict[short_url]

tiny_url = ShortenURL()
str = 'Abhishe Jain'
print('Original URL: ', str)
shortened_url = tiny_url.long_to_short(str)
print('Shortened url: ', shortened_url)
print('Original url: ', tiny_url.short_to_long(shortened_url))
