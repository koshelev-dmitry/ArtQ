import sqlite3
import os

class SQLiteDataBase:
    def __init__(self, db_name):
        self.db_name = db_name
        self._delete_sql_db() # First, remove existing DB
        self.conn = None # connection to a new DB

    def _delete_sql_db(self):
        if os.path.exists(self.db_name):
            try:
                os.remove(self.db_name)
            except:
                raise Exception(f"Error while deleting DB: {self.db_name}")
            else:
                print("Old version DB is removed")

    def open_connection(self):
        try:
            self.conn = sqlite3.connect(self.db_name)
        except:
            raise Exception(f"Error while creating connection to DB: {self.db_name}")
        else:
            print("DB is connected")

    def commit_changes(self):
        # commit changes and close the database
        if self.conn is None:
            raise Exception("No connection to DB found")
        try:
            self.conn.commit()
        except:
            raise Exception('DB commit Error')
        else: 
            print("DB changes are commited")

    def close_connection(self):
        # commit changes and close the database
        if self.conn is None:
            raise Exception("No connection to DB found")
        try:
            self.conn.close()
        except:
            raise Exception('Connection is not closed')
        else:
            print('DB Connection is closed')


    def write_data(self, exceldata, empty = False):
        cursor = self.conn.cursor()
        WriteMethods.write_artists('artist', exceldata.artists, cursor, empty)
        WriteMethods.write_locations('location', exceldata.locations, cursor, empty)
        WriteMethods.write_techniques('technique', exceldata.techniques, cursor, empty)
        WriteMethods.write_paintings('painting', exceldata.paintings, cursor, empty)
        WriteMethods.write_category_description('category', exceldata.categories, cursor, empty)
        WriteMethods.write_subcategory_description('subcategory', exceldata.subcategories, cursor, empty)
        WriteMethods.write_category_subcategory_relation('rel_category_subcategory', exceldata.categories, cursor, empty)
        WriteMethods.write_subcategory_painting_relation('rel_subcategory_painting', exceldata.subcategories, cursor, empty)
        WriteMethods.write_user_progress('user_progress', exceldata.categories, cursor, empty)
        WriteMethods.write_painting_artist_relation('rel_painting_artist', exceldata.paintings, cursor, empty)
        print("DB is written")

class WriteMethods:
    @staticmethod
    def write_artists(table_name, artist, cursor, empty=False):
        # create table and insert data
        cursor.execute(
            'CREATE TABLE IF NOT EXISTS ' + table_name
            + ' (id INTEGER, full_name TEXT, short_name TEXT, link TEXT, PRIMARY KEY(`id`))'
        )
        if not empty:
            for i in range(len(artist.id)):
                cursor.execute(
                    "INSERT INTO " + table_name + " VALUES (?, ?, ?, ?)",
                    (int(artist.id[i]), artist.full_name[i], artist.short_name[i], artist.wiki_link[i])
                )
            print('Write progress:', table_name, 'is printed')
        return None

    @staticmethod
    def write_locations(table_name, location, cursor, empty=False):
        cursor.execute(
            'CREATE TABLE IF NOT EXISTS ' + table_name
            + ' (id INTEGER, title TEXT, link TEXT, PRIMARY KEY(`id`))'
        )
        if not empty:
            for i in range(len(location.id)):
                cursor.execute(
                    "INSERT INTO " + table_name + " VALUES (?, ?, ?)",
                    (int(location.id[i]), location.name[i], location.wiki_link[i])
                )
            print('Write progress:', table_name, 'is printed')
        return None

    @staticmethod
    def write_techniques(table_name, technique, cursor, empty=False):
        cursor.execute(
            'CREATE TABLE IF NOT EXISTS ' + table_name
            + ' (id INTEGER, title TEXT, PRIMARY KEY(`id`))'
        )
        if not empty:
            for i in range(len(technique.id)):
                cursor.execute(
                    "INSERT INTO " + table_name + " VALUES (?, ?)",
                    (int(technique.id[i]), technique.name[i])
                )
            print('Write progress:', table_name, 'is printed')
        return None

    @staticmethod
    def write_paintings(table_name, painting, cursor, empty=False):
        cursor.execute(
            'CREATE TABLE IF NOT EXISTS ' + table_name + ' ('
            + 'id INTEGER, '
            + 'title TEXT,'
            + 'artist_id INTEGER,'
            + 'year TEXT,'
            + 'technique_id INTEGER,'
            + 'location_id INTEGER,'
            + 'size TEXT,'
            + 'description TEXT,'
            + 'wiki_link TEXT,'
            + 'image TEXT,'
            + 'FOREIGN KEY(`artist_id`) REFERENCES `artist`(`id`),'
            + 'FOREIGN KEY(`location_id`) REFERENCES `location`(`id`),'
            + 'FOREIGN KEY(`technique_id`) REFERENCES `technique`(`id`),'
            + 'PRIMARY KEY(`id`)'
            + ')'
        )
        if not empty:
            for i in range(len(painting.id)):
                cursor.execute(
                    "INSERT INTO " + table_name + " VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?)",
                    (
                        int(painting.id[i]),
                        painting.title[i],
                        int(painting.artist1_id[i]),
                        painting.year[i],
                        int(painting.tech_id[i]),
                        int(painting.location_id[i]),
                        str(float(painting.size[i].split('*')[0])) + ' cm x '
                        + str(float(painting.size[i].split('*')[1])) + ' cm',
                        painting.description[i],
                        painting.wiki_link[i],
                        painting.image[i]
                    )
                )
            print('Write progress:', table_name, 'is printed')
        return None

    @staticmethod
    def write_category_description(table_name, category, cursor, empty=False):
        cursor.execute(
            'CREATE TABLE IF NOT EXISTS ' + table_name
            + ' (id INTEGER, title TEXT, description TEXT, image TEXT, PRIMARY KEY(`id`))'
        )
        if not empty:
            for i in range(len(category.id)):
                cursor.execute(
                    "INSERT INTO " + table_name + " VALUES (?, ?, ?, ?)",
                    (
                        int(category.id[i]),
                        category.title[i],
                        category.description[i],
                        category.image[i]
                    )
                )
            print('Write progress: Category description is printed')
        return None

    @staticmethod
    def write_subcategory_description(table_name, subcategory, cursor, empty=False):
        cursor.execute(
            'CREATE TABLE IF NOT EXISTS ' + table_name
            + ' (id INTEGER, title TEXT, description TEXT, image TEXT, PRIMARY KEY(`id`))'
        )
        if not empty:
            for i in range(len(subcategory.id)):
                cursor.execute(
                    "INSERT INTO " + table_name + " VALUES (?, ?, ?, ?)",
                    (
                        int(subcategory.id[i]),
                        subcategory.title[i],
                        subcategory.description[i],
                        subcategory.image[i]
                    )
                )
            print('Write progress:', table_name, 'is printed')


    @staticmethod
    def write_category_subcategory_relation(table_name, category, cursor, empty=False):
        cursor.execute(
            'CREATE TABLE IF NOT EXISTS ' + table_name + ' ('
            + 'cat_id INTEGER, subcat_id INTEGER,'
            + 'FOREIGN KEY(`cat_id`) REFERENCES `category`(`id`),'
            + 'FOREIGN KEY(`subcat_id`) REFERENCES `subcategory`(`id`),'
            + 'PRIMARY KEY(`cat_id`, `subcat_id`)'
            + ')'
        )
        if not empty:
            for i in range(len(category.id)):
                arr_subcategory = []
                for element in str(category.subcategories_included[i]).split(','):
                    if len(element.split('-')) == 2:
                        first_num = int(element.split('-')[0])
                        second_num = int(element.split('-')[1])
                        for x in range(first_num, second_num+1):
                            arr_subcategory.append(x)
                    else:
                        arr_subcategory.append(int(element))

                for ii in arr_subcategory:
                    cursor.execute("INSERT INTO " + table_name + " VALUES (?, ?)", (int(category.id[i]), ii))
            print('Write progress:', table_name, 'is printed')


    @staticmethod
    def write_subcategory_painting_relation(table_name, subcategory, cursor, empty=False):
        cursor.execute(
            'CREATE TABLE IF NOT EXISTS ' + table_name + ' ('
            + 'subcat_id INTEGER, painting_id INTEGER, '
            + 'FOREIGN KEY(`subcat_id`) REFERENCES `category`(`id`), '
            + 'FOREIGN KEY(`painting_id`) REFERENCES `painting`(`id`), '
            + 'PRIMARY KEY(`subcat_id`, `painting_id`)'
            + ')'
        )
        if not empty:
            for i in range(len(subcategory.id)):
                arr_subcategory = []
                for element in str(subcategory.included_paintings[i]).split(','):
                    if len(element.split('-')) == 2:
                        first_num = int(element.split('-')[0])
                        second_num = int(element.split('-')[1])
                        for x in range(first_num, second_num+1):
                            arr_subcategory.append(x)
                    else:
                        arr_subcategory.append(int(element))

                for ii in arr_subcategory:
                    cursor.execute("INSERT INTO " + table_name + " VALUES (?, ?)", (int(subcategory.id[i]), ii))
            print('Write progress:', table_name, 'is printed')


    @staticmethod
    def write_user_progress(table_name, category, cursor, empty=False):
        cursor.execute(
            'CREATE TABLE IF NOT EXISTS ' + table_name + ' ('
            + 'cat_id INTEGER, subcat_id INTEGER, score INTEGER, '
            + 'FOREIGN KEY(`cat_id`) REFERENCES `category`(`id`), '
            + 'FOREIGN KEY(`subcat_id`) REFERENCES `subcategory`(`id`),'
            + 'PRIMARY KEY(`cat_id`, `subcat_id`)'
            + ')'
        )
        if not empty:
            for i in range(len(category.id)):
                arr_subcategory = []
                for element in str(category.subcategories_included[i]).split(','):
                    if len(element.split('-')) == 2:
                        first_num = int(element.split('-')[0])
                        second_num = int(element.split('-')[1])
                        for x in range(first_num, second_num+1):
                            arr_subcategory.append(x)
                    else:
                        arr_subcategory.append(int(element))

                for ii in arr_subcategory:
                    cursor.execute("INSERT INTO " + table_name + " VALUES (?, ?, ?)", (int(category.id[i]), ii, 0))
            print('Write progress:', table_name, 'is printed')

    @staticmethod
    def write_painting_artist_relation(table_name, paintings, cursor, empty=False):
        cursor.execute(
            'CREATE TABLE IF NOT EXISTS ' + table_name + ' ('
            + 'painting_id INTEGER, artist_id INTEGER, '
            + 'FOREIGN KEY(`painting_id`) REFERENCES `painting`(`id`), '
            + 'FOREIGN KEY(`artist_id`) REFERENCES `artist`(`id`), '
            + 'PRIMARY KEY(`painting_id`, `artist_id`)'
            + ')'
        )
        if not empty:
            for i in range(len(paintings.id)):
                for artist in [int(paintings.artist2_id[i]), 
                                int(paintings.artist3_id[i]),
                                int(paintings.artist4_id[i])]:
                    cursor.execute(
                        "INSERT INTO " + table_name + " VALUES (?, ?)",
                        (int(paintings.id[i]), artist)
                    )

            print('Write progress:', table_name, 'is printed')
