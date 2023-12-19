
import requests
from bs4 import BeautifulSoup
test_link = "https://www.google.com/search?q=diver+naruto+youtube"

# search_link ='https://www.google.com/search?q=' +'+'.join(mot for mot in words) + '+youtube'
# print('the search link is : ', search_link)
#searching google and registering most of the potential links
web_page = requests.get(test_link)
soup = BeautifulSoup(web_page.content, features='html.parser')

potential_link = soup.find_all('a')[7:]
print(potential_link)
