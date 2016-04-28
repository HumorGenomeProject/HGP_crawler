
/*
 * To run:
 * mongo example_mongo_script.js
 */


conn = new Mongo();
db = conn.getDB("hgp_webapp");

cursor = db.jokes.find().limit(2);

while(cursor.hasNext()){
    printjson(cursor.next());
}
