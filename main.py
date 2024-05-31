import sqlalchemy as sq
from sqlalchemy.orm import declarative_base, relationship, sessionmaker
from  models import create_tables, Publisher, Shop, Book, Stock, Sale

password = '.....'
db_name = 'books'
login = 'postgres'
host = '5432'
DSN = f'postgresql://{login}:{password}@localhost:{host}/{db_name}'
engine = sq.create_engine(DSN)

create_tables(engine)

p1 = Publisher(name='Альпина', book = [
    Book(title="Картина Сархана"),
    Book(title="Его последние дни")])
p2 = Publisher(name='АСТ', book = [
    Book(title="Мартин Иден"),
    Book(title="машина пространства")])
b1 = Book(title="Сирены Титана", publisher=p2)
b2 = Book(title="Колыбель для кошки", publisher=p2)
b3 = Book(title="Мифы Поволжья", publisher=p1)
b4 = Book(title= "Цветы для Элджернона", publisher=p2)
b5 = Book(title="Отец смотрит на запад", publisher=p1)         
shop1 = Shop(name="Галилео")
shop2 = Shop(name="Студент")
stock1 = Stock(book=b1, shop=shop1, count=20)
sale1 = Sale(price=450, date_sale='2024-05-14',stock=stock1, count=25)
stock2 = Stock(book=b3, shop=shop1, count=200)
sale2 = Sale(price=300, date_sale='2024-05-11',stock=stock2, count=15)
stock3 = Stock(book=b2, shop=shop2, count=50)
sale3 = Sale(price=250, date_sale='2024-05-10',stock=stock3, count=25)
stock4 = Stock(book=b2, shop=shop1, count=50)
sale4 = Sale(price=300, date_sale='2024-05-14',stock=stock4, count=5)
stock5 = Stock(book=b4, shop=shop1, count=10)
sale5 = Sale(price=300, date_sale='2024-05-12',stock=stock5, count=10)
stock6 = Stock(book=b5, shop=shop2, count=10)
sale6 = Sale(price=300, date_sale='2024-05-15',stock=stock6, count=25)

Session = sessionmaker(bind=engine)
s = Session()
s.add_all([p1, p2, b1, b2, b3,b4, b5, shop1, shop2, stock1, stock2, stock3, stock4,stock5,stock6, sale1, sale2, sale3, sale4, sale5, sale6])
s.commit()


def getshops(publ):
    q = s.query(Book.title, Shop.name, Sale.price, Sale.date_sale).join(Publisher).join(Stock).join(Shop).join(Sale)
    if publ.isdigit():
        q1 = q.filter(Publisher.id == publ)
    else:
        q1 = q.filter(Publisher.name == publ)
    for i in q1.all():
        print(f'{i[0]: <40} | {i[1]: <10} | {i[2]: <8} | {i[3].strftime('%d-%m-%Y')}')
        
        
if __name__ == '__main__':
    publ = input('Введите название издателя или его id :') 
    getshops(publ)   
    s.close() 