from datetime import datetime
from models.dbModel import DbModel
from models.CategoryModel import CategoryModel


class RecipeModel(DbModel):
    TableName = 'recipes'

    def __init__(self, mongo):
        super().__init__(mongo, self.TableName)
        self.Categories = CategoryModel(mongo, 'categories')
        self.Cuisines = CategoryModel(mongo, 'cuisines')

    def add(self, data, author):
        recipe = self.create_save_data(data, author, True)
        id = self.db.insert_one(recipe)
        print(data.categories.data)
        self.Categories.add(data.categories.data)
        self.Cuisines.add(data.cuisines.data)
        return id.inserted_id

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