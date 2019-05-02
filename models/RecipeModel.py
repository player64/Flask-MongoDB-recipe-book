from models.dbModel import DbModel


class RecipeModel(DbModel):
    TableName = 'recipe'

    def __init__(self, mongo):
        super().__init__(mongo, self.TableName)
        print('Recipe model')


"""
for val in response:
    new_dict.append(('method-{}'.format(k), val))
    k += 1
    
multi_dic = MultiDict(new_dict)
print(multi_dic)
MultiDict([('method-0', 'Add some'), ('method-1', 'Add some'), ('method-2', 'Add two')])
"""