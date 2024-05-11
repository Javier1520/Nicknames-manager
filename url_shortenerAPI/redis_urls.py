import redis, string
from datetime import timedelta
from django.utils import timezone

redis_client = redis.StrictRedis(host='localhost', port=6379, db=0)

BASE62_ALPHABET = string.digits + string.ascii_lowercase + string.ascii_uppercase
next_token_counter = 1

def generate_next_token():
    global next_token_counter
    token = encode_base62(next_token_counter).rjust(8, '0')  # Ensure length of token is 8
    next_token_counter += 1
    return token

def encode_base62(number):
    base62_encoded = ''
    while number:
        number, remainder = divmod(number, 62)
        base62_encoded = BASE62_ALPHABET[remainder] + base62_encoded
    return base62_encoded

def shorten_url(original_url, user_id, expires_at=timezone.now() + timedelta(days=365*5)):
    global next_token_counter
    token = generate_next_token()

    url_data = {
        'original_url': original_url,
        'user_id': user_id,
        'created_at': timezone.now().isoformat(),
        'expires_at': expires_at.isoformat(),
        'last_visited': ''
    }
    with redis_client.pipeline() as pipe:
        pipe.hmset(token, url_data)
        pipe.expire(token, 157788000)
        pipe.execute()
    return f"short.url/{token}"

def get_original_url(token):
    original_url = redis_client.hget(token, 'original_url')
    if original_url:
        redis_client.hset(token, 'last_visited', timezone.now().isoformat())
        return original_url.decode('utf-8')
    return None
