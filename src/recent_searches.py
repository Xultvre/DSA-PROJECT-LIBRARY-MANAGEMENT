from collections import deque

# Initialize Recent Searches
def create_recent_searches(capacity=5):
    return deque(maxlen=capacity)

# Add a search query
def add_recent_search(recent_searches, query):
    recent_searches.append(query)

# Get recent searches
def get_recent_searches(recent_searches):
    return list(recent_searches)