from models.dbModel import DbModel


class CategoryModel(DbModel):
    """
    class used for cuisines and category
    """

    def __init__(self, mongo, table_name):
        super().__init__(mongo, table_name)

    def add(self, categories: list):
        existing_categories = self.get_names()

        new_categories = []

        for category in categories:
            cat_name = category.lower()
            if cat_name in existing_categories:
                get_cat = self.get_one_by_attr('name', cat_name)
                self.update_counter('recipes_no', get_cat['recipes_no'] + 1, get_cat['_id'])
            elif cat_name:
                new_categories.append({
                    'name': cat_name,
                    'recipes_no': 1
                })

        if len(new_categories):
            self.db.insert_many(new_categories)

    def get_names(self):
        collection = self.get_all()
        return [item['name'] for item in collection]
