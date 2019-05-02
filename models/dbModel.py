from bson.objectid import ObjectId


class DbModel:
    Mongo = None
    TableName = None

    # https://docs.mongodb.com/manual/tutorial/query-arrays/

    def __init__(self, mongo, table_name):
        self.Mongo = mongo
        self.TableName = table_name

    def delete(self, table_id: ObjectId):
        return self.Mongo.db[self.TableName].remove({'_id': table_id})

    def get_one_by_id(self, table_id: ObjectId):
        return self.Mongo.db[self.TableName].find_one({'_id': table_id})

    def get_one_by_attr(self, attr_name: str, attr_value: str):
        return self.Mongo.db[self.TableName].find_one({attr_name: attr_value})
