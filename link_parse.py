import requests
from bs4 import BeautifulSoup
import re

class Link_parser():

    def __init__(self):
        
        self.potential_link = None

        self.final_link = []

    #this function will check if the link has the watch tag so that it redirects towards youtube

    def process_words(self, words):
        
        #turning the link into usable google link
        if len(words) > 20:
            self.potential_link = [words]
            print('direct link')
            return
        else : print('not direct link')
        

        search_link ='https://www.google.com/search?q=' +'+'.join(mot for mot in words) + '+youtube'
        print('the search link is : ', search_link)
        #searching google and registering most of the potential links
        web_page = requests.get(search_link)
        soup = BeautifulSoup(web_page.content, features='html.parser')

        self.potential_link = soup.find_all('a')[7:]
        


    def check_youtube(self, lien):
        # check if the watch keyword is present so that we know it is a youtube link
        lien = str(lien)
        if re.search('watch', lien) :
            return True

        return False
    def test(self):
        return self.potential_link

    #function to check if some links were found with this search then returning them    
    def analyze_link(self):
        self.final_link = []

        if len(self.potential_link) < 1 :
            return False

        # we'll step through the links this way to avoid link duplicate from google formatting
        for x in range(0, len(self.potential_link), 2):
            lien = self.potential_link[x]

            #we check if it's youtube link
            if self.check_youtube(lien=lien):
                try :
                    link = self.treat_tag(str(lien))
                    print(link)
                    self.final_link.append(link)
                    
                    #check if we got at least five links then return them
                    if len(self.final_link) > 4 :
                        return self.final_link
                
                except :
                    continue
                
        #if the whole loop runs, we check if we got at least one link then return a response
        if len(self.final_link) > 1:
            return self.final_link
        else :
            return self.final_link        


    def treat_tag(self, test_link):

        raw_lien = re.split('&', test_link, 1)
        lien = raw_lien[0]
        lien_start = re.search('http', lien).start()
        lien = lien[lien_start:]
        # print(lien)

        section = re.split('%', lien)
        debut = section[0]
        id = section[-1][2:]

        final_link = debut + '?v=' +id

        return final_link


# cherche = ['food', 'wars', 'snow', 'drop']

# recherche = Link_parser(cherche)
# liens = recherche.analyze_link()

# for link in liens :
#     print(link)



# cherche = ['monster', 'hunter', 'rise', 'mere']

# lot = Link_parser(cherche)
# la = lot.verifie()
# print(la)


# page = requests.get('https://www.google.com/search?q=food+wars+snw+drop+youtube')
# soup = BeautifulSoup(page.content)

# # links = soup.findAll("a")
# # for link in  soup.find_all("a",href=re.compile("(?<=/url\?q=)(htt.*://.*)")):
# #     print (re.split(":(?=http)", link["href"].replace("/url?q=", "")))
# def treat_tag(test_link):

#     raw_lien = re.split('&', test_link, 1)
#     lien = raw_lien[0]
#     lien_start = re.search('http', lien).start()
#     lien = lien[lien_start:]
#     # print(lien)

#     section = re.split('%', lien)
#     debut = section[0]
#     id = section[-1][2:]

#     final_link = debut + '?v=' +id

#     return final_link

# links = soup.find_all('a')

# for index, link in enumerate(links[15:]) :
#     if re.search('watch', str(link)):
#         lien = treat_tag(str(link))

#         print(index, '  :  ', lien)
# # https://www.youtube.com/watch?v=OZ9hY4SNBvk

# # https://www.youtube.com/watch%3Fv%3DOZ9hY4SNBvk&amp;sa=U&amp;ved=2ahUKEwj90rSbvuT9AhU6STABHeYHCg4QtwJ6BAgJEAE&amp;usg=AOvVaw0Vz4OIqVYpAGWe0LG350MC

# # test_link = "https://www.youtube.com/watch%\3Fv%\3DOZ9hY4SNBvk&amp;sa=U&amp;ved=2ahUKEwj90rSbvuT9AhU6STABHeYHCg4QtwJ6BAgJEAE&amp;usg=AOvVaw0Vz4OIqVYpAGWe0LG350MC" 

# link = ' <a href="/url?q=https://www.youtube.com/watch%3Fv%3DOZ9hY4SNBvk&amp;sa=U&amp;ved=2ahUKEwi9wYW5v-T9AhXGD1kFHRDwDLYQtwJ6BAgAEAE&amp;usg=AOvVaw23Em1J5f9kxvNHtgDarOo2"><div class="DnJfK"><div class="j039Wc"><h3 class="zBAuLc l97dzf"><div class="BNeawe vvjwJb AP7Wnd">Food Wars! The Second Plate - Ending | Snow Drop - YouTube</div></h3></div><div class="sCuL3"><div class="BNeawe UPmit AP7Wnd lRVwie">www.youtube.com › watch</div></div></div></a>'

