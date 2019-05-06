from datetime import datetime
from models.dbModel import DbModel
from models.CategoryModel import CategoryModel
import math


class RecipeModel(DbModel):
    TableName = 'recipes'
    RecipeNoArchive = 3

    def __init__(self, mongo):
        super().__init__(mongo, self.TableName)
        self.Categories = CategoryModel(mongo, 'categories')
        self.Cuisines = CategoryModel(mongo, 'cuisines')

    def add(self, data, author):
        # recipe = self.create_save_data(data, author, True)
        # categories = self.Categories.add(data.categories.data)
        # cuisines = self.Cuisines.add(data.cuisines.data)
        recipe = {
            'title': data.title.data,
            'introduction': data.introduction.data,
            'method': data.method.data,
            'ingredients': data.ingredients.data,
            'allergens': self.list_to_lower(data.allergens.data),
            'categories': self.list_to_lower(data.categories.data),
            'cuisines': self.list_to_lower(data.cuisines.data),
            'author': author,
            'views': 0,
            'likes': 0,
            'edited': datetime.now(),
            'created': datetime.now()
        }

        id = self.db.insert_one(recipe)
        return id.inserted_id

    def get_archive(self, query, page_no, order_by):
        skip_posts = 0 if page_no == 1 else page_no

        return self.db.find({'$query': query, '$orderby': {order_by: -1}}).skip(self.RecipeNoArchive * skip_posts).limit(
                self.RecipeNoArchive)

    def archive_pagination(self, query):
        return math.floor(self.db.find(query).count() / self.RecipeNoArchive)


    @staticmethod
    def list_to_lower(data):
        return [x.lower() for x in data]

    @staticmethod
    def create_save_data(data, author, new_data):
        """
        :param data: wtforms data
        :param author: session['user']['username']
        :param new_data: boolean new recipe or edir
        :return: Object
        """

        recipe = {}
        keys = ['title',
                'introduction',
                'method',
                'ingredients',
                'categories',
                'cuisines',
                'allergens']
        for key in keys:
            recipe[key] = data[key].data

        """
        If new_data create init data
        """

        if new_data:
            recipe.update({
                'author': author,
                'views': 0,
                'likes': 0,
                'edited': datetime.now(),
                'created': datetime.now()
            })
        else:
            recipe['edited']: datetime.now()

        return recipe

    @staticmethod
    def add_key_if_exists(data, key, obj):
        if key in data and data[key].data:
            obj[key] = data[key].data
        return obj


"""
for val in response:
    new_dict.append(('method-{}'.format(k), val))
    k += 1
    
multi_dic = MultiDict(new_dict)
print(multi_dic)
MultiDict([('method-0', 'Add some'), ('method-1', 'Add some'), ('method-2', 'Add two')])
"""