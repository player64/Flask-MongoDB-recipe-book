from datetime import datetime
from models.dbModel import DbModel
import math
from werkzeug.datastructures import MultiDict


class RecipeModel(DbModel):
    TableName = 'recipes'
    RecipeNoArchive = 24

    def __init__(self, mongo):
        super().__init__(mongo, self.TableName)

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
        page_no -= 1

        return self.db.find({'$query': query, '$orderby': {order_by: -1}}) \
            .skip(self.RecipeNoArchive * page_no) \
            .limit(self.RecipeNoArchive)

    def archive_pagination(self, query):
        return math.ceil(self.db.find(query).count() / self.RecipeNoArchive)

    def view(self, recipe_id):
        return self.get_one_by_id(recipe_id)

    def update_view_counter(self, recipe_id):
        self.db.update(
            {'_id': recipe_id},
            {'$inc': {
                'views': +1,
            }}
        )

    def edit_get(self, recipe_id, username):
        recipe = self.get_one_by_id(recipe_id)
        if recipe:
            if recipe['author'] != username:
                return False

            editable_keys = [
                'title',
                'introduction',
                'method',
                'ingredients',
                'categories',
                'cuisines',
                'allergens'
            ]

            editable = []
            for key in recipe.keys():
                if key in editable_keys:
                    if isinstance(recipe[key], list):
                        c = 0
                        for item in recipe[key]:
                            editable.append(('{}-{}'.format(key, c), item))
                            c += 1
                    else:
                        editable.append((key, recipe[key]))
            return MultiDict(editable)

    def related(self, exclude, categories):
        limit = 6
        related = []
        for category in categories:
            recipes = list(self.db.find(
                {'$query': {
                    'categories': {'$in': [category]}},
                    '$orderby': {'views': -1}}).limit(limit))

            limit -= len(related)
            for recipe in recipes:
                if len(related) == 6:
                    return related
                if exclude != recipe['_id']:
                    related.append(recipe)
            return related

    def vote(self, recipe_id, username):
        recipe = self.get_one_by_id(recipe_id)
        if recipe and recipe['author'] != username:
            likes = int(recipe['likes'])
            if 'liked_by' in recipe and recipe['liked_by'] is not None:
                if username in recipe['liked_by']:
                    likes -= 1
                    liked_by = recipe['liked_by'].remove(username)
                else:
                    likes += 1
                    liked_by = recipe['liked_by'].append(username)

            else:
                likes += 1
                liked_by = [username]

            self.db.update_one(
                {'_id': recipe_id},
                {'$set': {
                    'likes': likes,
                    'liked_by': liked_by
                }}
            )

            return likes
        return False

    def fakestatistic(self):
        for recipe in self.db.find():
            views = self.random_key_list(150)

            max_likes = 30 if views > 40 else views - 5

            likes = self.random_key_list(max_likes)
            self.db.update_one(
                {'_id': recipe['_id']},
                {'$set': {
                    'views': views,
                    'likes': likes
                }}
            )

    @staticmethod
    def random_key_list(max):
        import random
        max = max if max > 0 else 1
        return random.randint(0, max)

    @staticmethod
    def list_to_lower(data):
        return [x.lower() for x in data]
