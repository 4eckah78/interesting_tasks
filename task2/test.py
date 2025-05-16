import unittest
from unittest.mock import patch, Mock
from collections import defaultdict
from solution import get_animals_count, save_to_csv

class TestWikiParser(unittest.TestCase):
    
    @patch('requests.get')
    def test_get_animals_count_single_page(self, mock_get):
        """Тест обработки одной страницы категории"""
        html = """
        <div class="mw-category">
            <div class="mw-category mw-category-columns">
                <h3>А</h3>
                <ul>
                    <li><a title="Аист">Аист</a></li>
                    <li><a title="Акула">Акула</a></li>
                </ul>
                <h3>Б</h3>
                <ul>
                    <li><a title="Барсук">Барсук</a></li>
                </ul>
            </div>
        </div>
        """
        mock_response = Mock()
        mock_response.text = html
        mock_get.return_value = mock_response
        
        result = get_animals_count()
        
        expected = defaultdict(int, {'А': 2, 'Б': 1})
        self.assertEqual(result, expected)

    @patch('requests.get')
    def test_get_animals_count_multiple_pages(self, mock_get):
        """Тест обработки нескольких страниц с пагинацией"""
        html_page1 = """
        <div class="mw-category">
            <div class="mw-category mw-category-columns">
                <h3>А</h3>
                <ul>
                    <li><a title="Аист">Аист</a></li>
                </ul>
            </div>
        </div>
        <a href="/w/index.php?title=Категория:Животные_по_алфавиту&amp;pagefrom=Барсук#mw-pages" 
           title="Категория:Животные по алфавиту">Следующая страница</a>
        """
        
        html_page2 = """
        <div class="mw-category">
            <div class="mw-category mw-category-columns">
                <h3>Б</h3>
                <ul>
                    <li><a title="Барсук">Барсук</a></li>
                </ul>
            </div>
        </div>
        """
        
        mock_get.side_effect = [
            Mock(text=html_page1),
            Mock(text=html_page2)
        ]
        
        result = get_animals_count()
        expected = defaultdict(int, {'А': 1, 'Б': 1})
        self.assertEqual(result, expected)

    @patch('requests.get')
    def test_ignore_non_cyrillic(self, mock_get):
        """Тест игнорирования не-кириллических символов"""
        html = """
        <div class="mw-category">
            <div class="mw-category mw-category-columns">
                <h3>A</h3>
                <ul>
                    <li><a title="Ant">Ant</a></li>
                </ul>
                <h3>Б</h3>
                <ul>
                    <li><a title="Барсук">Барсук</a></li>
                </ul>
            </div>
        </div>
        """
        mock_response = Mock()
        mock_response.text = html
        mock_get.return_value = mock_response
        
        result = get_animals_count()
        expected = defaultdict(int, {'Б': 1})
        self.assertEqual(result, expected)

    def test_save_to_csv(self):
        """Тест сохранения в CSV"""
        import os
        import csv
        
        test_data = defaultdict(int, {'А': 5, 'Б': 3})
        test_filename = 'test_beasts.csv'
        
        save_to_csv(test_data, test_filename)
        
        self.assertTrue(os.path.exists(test_filename))
        
        with open(test_filename, 'r', encoding='utf-8') as f:
            reader = csv.reader(f)
            rows = list(reader)
            
        expected_rows = [
            ['Буква', 'Количество'],
            ['А', '5'],
            ['Б', '3']
        ]
        self.assertEqual(rows, expected_rows)
        
        os.remove(test_filename)

    @patch('requests.get')
    def test_empty_category(self, mock_get):
        """Тест пустой категории"""
        mock_response = Mock()
        mock_response.text = '<div class="mw-category"></div>'
        mock_get.return_value = mock_response
        
        result = get_animals_count()
        self.assertEqual(result, defaultdict(int))

if __name__ == '__main__':
    unittest.main()