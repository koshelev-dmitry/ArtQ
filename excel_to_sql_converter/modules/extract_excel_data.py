import pandas as pd

class ExtractExcelData:
    def __init__(self, excel_file_name):
        self.excel_file = excel_file_name
        self._open_excel()

    def _open_excel(self):
        # Open the database
        try:
            xl = pd.ExcelFile(self.excel_file)
        except:
            # Didn't find exception error message, 
            # but if file is not found it passes through 
            # exception block 
            raise FileNotFoundError(f"file {self.excel_file} not found") 
        else:
            self.xl_dict = {sheet_name: xl.parse(sheet_name) 
                            for sheet_name in xl.sheet_names}


    def exctract_data(self):
        self.artists = Artist(self.xl_dict['Artist'])
        self.locations = Location(self.xl_dict['Location'])
        self.techniques = Technique(self.xl_dict['Technique'])
        self.paintings = Painting(self.xl_dict['Paintings'])
        self.categories = Category(self.xl_dict['Category'])
        self.subcategories = SubCategory(self.xl_dict['SubCategory'])


class Artist:
    def __init__(self, artist):
        # artist is a panda class
        self.id = artist['id']
        self.full_name = artist['en_full_name']
        self.short_name = artist['en_short_name']
        self.wiki_link = artist['en_link']

    def present_artist(self):
        print('id = ', self.id)
        print('Full name = ', self.full_name)
        print('short_name = ', self.short_name)
        print('Wiki URL = ', self.wiki_link)


class Painting:
    def __init__(self, painting):
        self.id = painting['id']
        self.title = painting['pic_title']
        self.artist1_id = painting['artist1_id']
        self.artist2_id = painting['artist2_id']
        self.artist3_id = painting['artist3_id']
        self.artist4_id = painting['artist4_id']
        self.location_id = painting['location_id']
        self.tech_id = painting['tech_id']
        self.size = painting['size']
        self.image = painting['image']
        self.year = painting['year']
        self.description = painting['description']
        self.wiki_link = painting['wiki_link']


class Location:
    def __init__(self, artist):
        self.id = artist['id']
        self.name = artist['en_title']
        self.wiki_link = artist['en_link']


class Technique:
    def __init__(self, technique):
        self.id = technique['id']
        self.name = technique['name']


class Category:
    def __init__(self, category):
        self.id = category['id']
        self.title = category['title']
        self.description = category['description']
        self.image = category['image']
        self.subcategories_included = category['subcategories_included']


class SubCategory:
    def __init__(self, subcategory):
        self.id = subcategory['id']
        self.title = subcategory['title']
        self.description = subcategory['description']
        self.image = subcategory['image']
        self.included_paintings = subcategory['included_paintings']


