import pandas as pd


class ExtractExcelData:
    def __init__(self, excel_file_name):
        self.excel_file = excel_file_name
        self.xl_dict = {}
        self.artists = None
        self.locations = None
        self.techniques = None
        self.paintings = None
        self.categories = None
        self.subcategories = None

    def read_excel_data(self):
        """read data from excel to pandas table
        excel file has few sheets,
        Each sheet is converted into dict
        to store values with key = sheet_name
        """
        try:
            xl = pd.ExcelFile(self.excel_file)
        except IOError:
            raise FileNotFoundError(f"file {self.excel_file} not found, or no data") 
        else:
            # parse pandas sheets into dict:
            # {sheet_name: data stored in the sheet}
            self.xl_dict = {sheet_name: xl.parse(sheet_name) 
                            for sheet_name in xl.sheet_names}

    def structure_data(self):
        """Extract data from pandas as instances of corresponding classes"""
        self.artists = Artist(self.xl_dict['Artist'])
        self.locations = Location(self.xl_dict['Location'])
        self.techniques = Technique(self.xl_dict['Technique'])
        self.paintings = Painting(self.xl_dict['Paintings'])
        self.categories = Category(self.xl_dict['Category'])
        self.subcategories = SubCategory(self.xl_dict['SubCategory'])


class Artist:
    """
    Converts artist table into instance of class Artist 
    Attributes:
        id         - id of each artist, used as a Primary Key in SQL, e.g. [1, 2]
        full_name  - list of names, e.g. ['Vincent van Gogh', 'Leonardo da Vinci']
        short_name - list of short names e.g. ['van Gogh', 'da Vinci']
        wiki_link  - list of links targeting to Wikipeadia articles about each artist
    Ordering of each list is presumed from excel table
    """
    def __init__(self, artist):
        self.id = artist['id']
        self.full_name = artist['en_full_name']
        self.short_name = artist['en_short_name']
        self.wiki_link = artist['en_link']

    # def present_artist(self):
    #     """"""
    #     print('id = ', self.id)
    #     print('Full name = ', self.full_name)
    #     print('short_name = ', self.short_name)
    #     print('Wiki URL = ', self.wiki_link)


class Painting:
    """
    Converts painting table into instance of class Painting 
    Attributes:
        id          - id of each painting (SQL Primary Key), e.g. [1, 2]
        title       - full title of each painting ["Self portrait", "Madonna"]
        artist1_id  - id of artist, (SQL Foreign Key)
        artist2_id  - id of artist, (SQL Foreign Key)
        artist3_id  - id of artist, (SQL Foreign Key)
        artist4_id  - id of artist, (SQL Foreign Key)
        location_id - current location of the painting, (SQL Foreign Key)
        tech_id     - technique used by artist, (SQL Foreign Key) 
        size        - painting's sizes, e.g. ['123*65', '230.1 * 90']
        image       - name of the picture file, e.g. ['pic1.jpg', 'pic2.jpg']
        year        - creation year, e.g. [1910, 1670]
        description - short description of the painting
        wiki_link   - links to wikipedia about each painting
    Ordering of each list is presumed from excel table
    """

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
    """
    Converts location table into instance of class Location 
    Attributes:
        id          - id of each location (SQL Primary Key), e.g. [1, 2]
        title       - title of location, e.g. ["Louvre, France", "National Gallery, UK"]
        wiki_link   - links to wikipedia about each location/museum
    Ordering of each list is presumed from excel table
    """
    def __init__(self, artist):
        self.id = artist['id']
        self.name = artist['en_title']
        self.wiki_link = artist['en_link']


class Technique:
    """
    Converts location table into instance of class Location 
    Attributes:
        id          - id of each location (SQL Primary Key), e.g. [1, 2]
        name        - title of technique, e.g. ["Oil on canvas"]
    Ordering of each list is presumed from excel table
    """
    def __init__(self, technique):
        self.id = technique['id']
        self.name = technique['name']


class Category:
    """
    Converts location table into instance of class Location
    Attributes:
        id          - id of each location (SQL Primary Key), e.g. [1, 2]
        name        - title of techniqu, e.g. ["Oil on canvas"]
    Ordering of each list is presumed from excel table
    """
    def __init__(self, category):
        self.id = category['id']
        self.title = category['title']
        self.description = category['description']
        self.image = category['image']
        self.subcategories_included = category['subcategories_included']


class SubCategory:
    """exctract data from subcategory sheet"""
    def __init__(self, subcategory):
        self.id = subcategory['id']
        self.title = subcategory['title']
        self.description = subcategory['description']
        self.image = subcategory['image']
        self.included_paintings = subcategory['included_paintings']


