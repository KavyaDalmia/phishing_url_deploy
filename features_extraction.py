import re
from urllib.parse import urlparse
from datetime import datetime
import urllib
import urllib.request
from bs4 import BeautifulSoup
import whois
import requests

# 3.1 IP Address in the URL
def has_ip_address(url):
    ipv4_pattern = r'\b(?:\d{1,3}\.){3}\d{1,3}\b'
    ipv6_pattern = r'\b(?:[A-F0-9]{1,4}:){7}[A-F0-9]{1,4}\b'
    has_ipv4 = re.search(ipv4_pattern, url) is not None
    has_ipv6 = re.search(ipv6_pattern, url) is not None
    return 1 if (has_ipv4 | has_ipv6) else 0

# 3.2 Checking the length of the URL
def length(url):
    return 1 if len(url) >= 54 else 0

# 3.3 If there is a @ in a URL
def checkAtSign(url):
    return 1 if "@" in url else 0

# 3.4 Domain Age
def calc_domain_age(url, threshold=30):
    try:
        domain = urlparse(url).netloc
        domain_info = whois.whois(domain)
        creation_date = domain_info.creation_date
        if isinstance(creation_date, list):
            creation_date = creation_date[0]
        if creation_date:
            current_date = datetime.now()
            domain_age = (current_date - creation_date).days
            return 1 if (domain_age and domain_age <= threshold) else 0
    except:
        pass
    return 0

# 3.5 URL shortening
def check_shortening(url):
    shortening_services = r"bit\.ly|goo\.gl|shorte\.st|go2l\.ink|x\.co|ow\.ly|t\.co|tinyurl|tr\.im|is\.gd|cli\.gs|" \
                          r"yfrog\.com|migre\.me|ff\.im|tiny\.cc|url4\.eu|twit\.ac|su\.pr|twurl\.nl|snipurl\.com|" \
                          r"short\.to|BudURL\.com|ping\.fm|post\.ly|Just\.as|bkite\.com|snipr\.com|fic\.kr|loopt\.us|" \
                          r"doiop\.com|short\.ie|kl\.am|wp\.me|rubyurl\.com|om\.ly|to\.ly|bit\.do|lnkd\.in|db\.tt|" \
                          r"qr\.ae|adf\.ly|goo\.gl|bitly\.com|cur\.lv|tinyurl\.com|ow\.ly|bit\.ly|ity\.im|q\.gs|is\.gd|" \
                          r"po\.st|bc\.vc|twitthis\.com|u\.to|j\.mp|buzurl\.com|cutt\.us|u\.bb|yourls\.org|x\.co|" \
                          r"prettylinkpro\.com|scrnch\.me|filoops\.info|vzturl\.com|qr\.net|1url\.com|tweez\.me|v\.gd|" \
                          r"tr\.im|link\.zip\.net"
    return 1 if re.search(shortening_services, url) else 0

# 3.6 Web traffic
def web_traffic(url):
    try:
        url = urllib.parse.quote(url)
        rank = BeautifulSoup(urllib.request.urlopen("http://data.alexa.com/data?cli=10&dat=s&url=" + url).read(), "xml").find("REACH")['RANK']
        return 1 if int(rank) < 100000 else 0
    except:
        return 1

# 3.7 HTML and JS based features
def check_for_iframe(response):
    if response == "":
        return 1
    try:
        if response.status_code == 200:
            html_content = response.text
            soup = BeautifulSoup(html_content, 'html.parser')
            iframes = soup.find_all('iframe')
            return 1 if iframes else 0
        else:
            return 0
    except Exception as e:
        return 0

def check_for_bar_manipulation(response):
    if response == "":
        return 1
    try:
        if response.status_code == 200:
            html_content = response.text
            js_code = re.findall(r'<script.*?onmouseover.*?>.*?</script>', html_content, re.DOTALL)
            return 1 if js_code and any("window.status" in code or "status=" in code for code in js_code) else 0
    except Exception as e:
        return 0

def check_for_right_click_disabled(response):
    if response == "":
        return 1
    try:
        if response.status_code == 200:
            html_content = response.text
            js_code = re.findall(r'<script.*?>.*?</script>', html_content, re.DOTALL)
            return 1 if js_code and any("event.button==2" in code or "status=" in code for code in js_code) else 0
    except Exception as e:
        return 0

def featureExtraction(url, target_label):
    features = []
    try:
        response = requests.get(url)
    except:
        response = ""
    features.append(has_ip_address(url))
    features.append(length(url))
    features.append(checkAtSign(url))
    features.append(calc_domain_age(url, 30))
    features.append(check_shortening(url))
    features.append(check_for_iframe(response))
    features.append(check_for_bar_manipulation(response))
    features.append(check_for_right_click_disabled(response))
    features.append(web_traffic(url))
    features.append(target_label)
    return features

def featureExtraction(url):
    features = []
    try:
        response = requests.get(url)
    except:
        response = ""
    features.append(has_ip_address(url))
    features.append(length(url))
    features.append(checkAtSign(url))
    features.append(calc_domain_age(url, 30))
    features.append(check_shortening(url))
    features.append(check_for_iframe(response))
    features.append(check_for_bar_manipulation(response))
    features.append(check_for_right_click_disabled(response))
    features.append(web_traffic(url))
    return features
# Example usage:
# features = featureExtraction("https://www.example.com", 0)
# print(features)
