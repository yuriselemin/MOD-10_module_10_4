import threading
import random
import queue
import time

# Домашнее задание по теме "Очереди для обмена данными между потоками."


class Table:
    def __init__(self, number):
        self.number = number
        self.guest = None

class Guest(threading.Thread):
    def __init__(self, name):
        super().__init__()
        self.name = name

    def run(self):
        time_to_wait = random.randint(3, 10)
        time.sleep(time_to_wait)

class Cafe:
    def __init__(self, *tables):
        self.queue = queue.Queue()
        self.tables = tables

    def guest_arrival(self, *guests):
        for guest in guests:
            if any(table.guest is None for table in self.tables):
                table = next(table for table in self.tables if table.guest is None)
                table.guest = guest
                guest.start()
                print(f"{guest.name} сел(а) за стол номер {table.number}.")
            else:
                self.queue.put(guest)
                print(f"{guest.name} в очереди.")

    def discuss_guests(self):
        while not self.queue.empty() or any(table.guest is not None for table in self.tables):
            for table in self.tables:
                if table.guest is not None and not table.guest.is_alive():
                    print(f"{table.guest.name} поел(а) и ушел(а).")
                    table.guest = None
                    print(f"Стол номер {table.number} свободен.")
                    if not self.queue.empty():
                        guest = self.queue.get()
                        table.guest = guest
                        guest.start()
                        print(f"{guest.name} вышел из очереди и сел за стол номер {table.number}.")

# Создание столов
tables = [Table(number) for number in range(1, 6)]
# Имена гостей
guests_names = [
'Maria', 'Oleg', 'Vakhtang', 'Sergey', 'Darya', 'Arman',
'Vitoria', 'Nikita', 'Galina', 'Pavel', 'Ilya', 'Alexandra'
]
# Создание гостей
guests = [Guest(name) for name in guests_names]
# Заполнение кафе столами
cafe = Cafe(*tables)
# Приём гостей
cafe.guest_arrival(*guests)
# Обслуживание гостей
cafe.discuss_guests()


