import requests
import json
from typing import Dict,Any
import pytest
from select_adult import check_adult_limit

def test_adult_limit():
    url='http://localhost:8000/create_movie'
    response=requests.get(url)
    if response.status_code==200:
        fetch_data=response.json()
        contents=check_adult_limit(fetch_data)
        
    
    assert 'adult' in contents
    assert 'original_title' in contents
    assert response.status_code== 200