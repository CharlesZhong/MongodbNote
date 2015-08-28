"""
Problem:        Write a program in the language of your choice that will remove the lowest
                homework score for each student.
                Since there is a single document for each student containing an array of scores,
                you will need to update the scores array and remove the homework.

Demo:           {
                    "_id" : 137,
                    "name" : "Tamika Schildgen",
                    "scores" : [
                        {
                            "type" : "exam",
                            "score" : 4.433956226109692
                        },
                        {
                            "type" : "quiz",
                            "score" : 65.50313785402548
                        },
                        {
                            "type" : "homework",
                            "score" : 89.5950384993947
                        },
                        {
                            "type" : "homework",
                            "score" : 54.75994689226145
                        }
                    ]
                }
Hint/spoiler:   With the new schema, this problem is a lot harder and that is sort of the point.
                One way is to find the lowest homework in code and then update the scores array
                with the low homework pruned.

check:          db.students.aggregate(  { '$unwind' : '$scores' } ,
                                        { '$group' : { '_id' : '$_id' , 'average' : { $avg : '$scores.score' } } } ,
                                        { '$sort' : { 'average' : -1 } } ,
                                        { '$limit' : 1 }
                                        )
Usage:          python drop_lowest.py
"""

__author__ = 'Charles'


from pymongo import MongoClient
from sys import exc_info

def find_lowest_hw(scores):
    """
    Finds lowest hw score in the list.
    """
    print reduce(lambda x,y: min(x['score'],y['score']),[ i for i in scores if "type" in i and i["type"] == "homework"])

    return reduce(lambda x,y: x if x['score'] < y['score'] else y,[ i for i in scores if "type" in i and i["type"] == "homework"])

def remove_lowest(collection):
    """
    Drops the lowest score for each student.
    """
    cursor = collection.find()
    for student in cursor:
        _id = student["_id"]
        print "Looking at student {_id}:".format(_id=_id)
        scores = student['scores']
        lowest = find_lowest_hw(scores)
        print lowest
        if (lowest is not None):
            print ("  Removing hw grade of {score}.").format(score=lowest['score'])
            scores.remove(lowest)
            collection.update_one({'_id': _id},
                                  {'$set': {'scores': scores}})
        else:
            print "  Could not find a homework score to process"



def main():
    """
    Establishes a client and drops the lowest score for each student.
    """
    host = 'localhost'
    port = 27017
    db_name = 'school'
    collection_name = 'students'

    client = MongoClient(host=host, port=port)
    db = client[db_name]
    collection = db[collection_name]

    print ("Removing lowest score from students in the {db}.{collection} "
           "namespace.").format(db=db.name, collection=collection.name)

    remove_lowest(collection=collection)
if __name__ == "__main__":
    main()