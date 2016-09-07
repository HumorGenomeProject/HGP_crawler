
/*
 * For use when you first setup the crawler
 * creates a collection called "counters" to be used as auto-increment values
 * To run:
 * mongo init_hgp_crawler_counters.js
 */

var dbname = "hgp_crawler";

conn = new Mongo();
db = conn.getDB(dbname);

db.counters.insert({
    "_id": "jokeId",
    "value": 3571  // Start with some prime number
});

db.counters.insert({
    "_id": "userId",
    "value": 7919  // Start with some prime number
});
