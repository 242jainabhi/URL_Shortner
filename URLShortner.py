import hashlib
import string

class ShortenURL():
    _ALPHABET = string.ascii_letters + string.digits
    _BASE = len(_ALPHABET)

    def __init__(self):
        self.tiny_to_long = {}

    def _convert_to_base(self, x):
        result = []
        while x:
            x, r = divmod(x, ShortenURL._BASE)
            result.append(ShortenURL._ALPHABET[r])
        return ''.join(result)

    def encode(self, longUrl):
        """Encodes a URL to a shortened URL.

        :type longUrl: str
        :rtype: str
        """
        md5_hash = hashlib.md5(longUrl.encode()).hexdigest()
        # md5_hash has 32 bytes
        # get 3 slices of 10 bytes each and xor them so we end up with a shorter URL suffix of len 8
        size = len(md5_hash)

        x = md5_hash[:size//3]
        y = md5_hash[size//3:-size//3]
        z = md5_hash[-size//3:]
        x_as_int = int(x, 16)
        y_as_int = int(y, 16)
        z_as_int = int(z, 16)
        xored = x_as_int ^ y_as_int ^ z_as_int

        suffix = self._convert_to_base(xored)
        # tiny_url = ShortenURL._PREFIX + '/' + suffix
        # if tiny_url not in self.tiny_to_long:
        #     self.tiny_to_long[tiny_url] = longUrl

        return suffix

    def decode(self, shortUrl):
        """Decodes a shortened URL to its original URL.

        :type shortUrl: str
        :rtype: str
        """
        return self.tiny_to_long.get(shortUrl)

if __name__ == '__main__':
    tiny_url = ShortenURL()
    str = 'Abhishe Jain'
    print('Original URL: ', str)

    shortened_url = tiny_url.encode(str)
    print('Shortened url: ', shortened_url)
    print('Original url: ', tiny_url.decode(shortened_url))
