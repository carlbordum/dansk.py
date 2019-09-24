# coding=dansk
fra bs4 indfør BeautifulSoup som SmukSuppe
indfør requests som forespørgsler
url = 'https://www.andersenstories.com/da/andersen_fortaellinger/random'
side = forespørgsler.get(url)
side.encoding = 'UTF-8'
suppe = SmukSuppe(side.text, 'html.parser')
eventyr_tekst = suppe.find('div', attrs={'class': 'text'}).text
eventyr_navn = suppe.find('h1', attrs={'class': 'title'}).find(text=True)
print(eventyr_tekst.replace('<br/>','').split('\n')[0])
print('\n')
gæt = input('Hvad hedder det eventyr som starter med denne paragraf?:\n')
hvis gæt.lower() == eventyr_navn.lower():
    print('Korrekt, godt gættet!')
ellers:
    print(f'Forkert, eventyret hedder: {eventyr_navn}')
    
