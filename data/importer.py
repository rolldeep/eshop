import csv
import sys
import os
from typing import List, AnyStr
sys.path.append(os.path.abspath(os.path.join('..')))
from models import Category, db, Meal


def import_csv():

    with open('delivery_categories.csv', encoding='utf-8') as f:
        cat = list(csv.reader(f, delimiter=','))
        for row in cat:
            if row[1] != 'title':    
                cat = Category(id=row[0], title=row[1])
                db.session.add(cat)
    db.session.commit()
    with open('delivery_items.csv', encoding='utf-8') as f:
        table = csv.reader(f, delimiter=',')
        for row in table:
            if row[0] != 'id':
                item = Meal(id=row[0],
                            title=row[1],
                            price=row[2],
                            description=row[3],
                            picture=row[4],
                            category_id=row[5])
                db.session.add(item)

    db.session.commit()


if __name__ == "__main__":
    from app import app
    with app.app_context():
        import_csv()
