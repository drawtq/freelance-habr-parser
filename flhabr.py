from excel import Excel
from bs4 import BeautifulSoup

import requests

# Словарь из css-селекторов
selectors: dict = {
    'tasks': '#tasks_list > li > article',
    'heading': 'div > header > div.task__title > a',
    'price': 'aside > div > span',
    'date': 'div > header > div.task__params.params > span.params__published-at.icon_task_publish_at > span',
    'views': 'div > header > div.task__params.params > span.params__views.icon_task_views > i',
    'responses': 'div > header > div.task__params.params > span.params__responses.icon_task_responses > i'
}


class FreelanceHabrParser(object):
    def __init__(self, output: str, query: str = "") -> None:
        self.query: str = query
        self.page: int = 1
        self.parsing: bool = True

        self.excel: Excel = Excel(output)
        self.session: requests.Session = requests.Session()

    # Главный метод (Запуск)
    def run(self) -> None:
        # Записываем названия колонок
        self.excel.write_title(columns=('Заголовок', 'Стоимость', 'Просмотры', 'Отклики', 'Дата', 'Ссылка'))

        # Цикл, который завершится при условии 'self.parsing = False'
        while self.parsing:
            self.step()

        # Записываем результат работы парсера в excel-таблицу
        self.excel.close()

    # Возвращаем url на основе текущей страницы, и запроса
    def generate_url(self) -> str:
        return f"https://freelance.habr.com/tasks?q={self.query}&page={self.page}"

    # Метод итерации
    def step(self) -> None:
        # Сгенерированная ссылка на текущую страницу
        url: str = self.generate_url()

        # http-ответ
        response: object = self.session.get(url=url)

        soup: BeautifulSoup = BeautifulSoup(response.text, 'lxml')

        # Результат работы парсера (tuple)
        tasks: list = self.parse_tasks(soup)
        if tasks:
            print('Текущая страница:', self.page)
            self.page += 1
            for task in tasks:
                self.excel.write(task)
        else:
            self.parsing = False

    def parse_tasks(self, soup: object) -> list:
        tasks_result: list = []
        tasks: list = soup.select(selectors['tasks'])

        for task in tasks:
            title, href = self.parse_heading(task)

            price: str = task.select_one(selectors['price']).text
            date: str = task.select_one(selectors['date']).text

            views: object = task.select_one(selectors['views'])
            responses: object = task.select_one(selectors['responses'])

            # Эти поля необходимо проверить, поскольку в них может не быть текста из за чего будет тип None
            views, responses = (element.text if element else '' for element in (views, responses))

            result: tuple = (title, price, views, responses, date, href)
            tasks_result.append(result)

        return tasks_result

    @staticmethod
    def parse_heading(task: object) -> tuple:
        heading: object = task.select_one(selectors['heading'])
        return heading.text, 'https://freelance.habr.com' + heading.get('href')
