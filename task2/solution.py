import requests
from bs4 import BeautifulSoup
import csv
from collections import defaultdict

def get_animals_count():

    letter_counts = defaultdict(int)
    
    url = "https://ru.wikipedia.org/wiki/Категория:Животные_по_алфавиту"
    
    pages_count = 0

    while True:
        response = requests.get(url)
        soup = BeautifulSoup(response.text, 'html.parser')
        category_div = soup.find('div', {'class': 'mw-category mw-category-columns'})
        if not category_div:
            break
            
        links = category_div.find_all('a')
        for link in links:
            title = link.get('title', '')
            if title:
                first_letter = title[0].upper()
                if 'А' <= first_letter <= 'Я':
                    letter_counts[first_letter] += 1
        
        next_page = soup.find('a', string='Следующая страница')
        if not next_page:
            break
            
        url = "https://ru.wikipedia.org" + next_page.get('href')

        pages_count += 1

        print(f'\rСтраниц посетели: {pages_count}/236', end='')
    
    return letter_counts

def save_to_csv(letter_counts, filename='beasts.csv'):
    sorted_counts = sorted(letter_counts.items(), key=lambda x: x[0])
    
    with open(filename, 'w', newline='', encoding='utf-8') as csvfile:
        writer = csv.writer(csvfile)
        writer.writerow(['Буква', 'Количество'])
        for letter, count in sorted_counts:
            writer.writerow([letter, count])

if __name__ == "__main__":
    counts = get_animals_count()
    save_to_csv(counts)
    print()
    print("Данные сохранены в beasts.csv")