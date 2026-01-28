import redis

try:
    # Attempt to connect to local Redis
    r = redis.Redis(host='localhost', port=6379, db=0)
    # Write a test key
    r.set('test_status', 'Connected to Redis!')
    # Read it back
    value = r.get('test_status')
    print(f"SUCCESS: {value.decode('utf-8')}")
except Exception as e:
    print(f"FAILED: Could not connect to Redis. Error: {e}")