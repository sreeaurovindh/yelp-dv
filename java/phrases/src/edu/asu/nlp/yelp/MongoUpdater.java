package edu.asu.nlp.yelp;
import com.mongodb.DBCollection;
import com.mongodb.*;

import java.net.UnknownHostException;
import java.util.ArrayList;
import java.util.List;

/**
 * Created by sviswa10 on 1/25/2017.
 */
public class MongoUpdater {
    final static String MongoUri = "mongodb://localhost:27017/";
    final static String Database = "yelp_dv";
    final static String Tip = "food_tip";
    final static String Reviews = "food_reviews";
    MongoClient mongoClient;
    DB database;
    DBCollection reviewsCollection, tipCollection;

    public MongoUpdater() {
        try {
            mongoClient = new MongoClient(new MongoClientURI(MongoUri));

        } catch (Exception e) {
            e.printStackTrace();
        }
        database = mongoClient.getDB(Database);
        reviewsCollection = database.getCollection(Reviews);
        tipCollection = database.getCollection(Tip);
    }

    public static void main(String[] args) {
        MongoUpdater phrases = new MongoUpdater();
        try {
            phrases.run();
        }
        catch(Exception exception) {
            phrases.run();
        }
    }

    public void run() {
        DBCursor cursor = tipCollection.find();
        int count = cursor.count();
        Extract extractor = new Extract();
        int done = 0;
        try {
            while (cursor.hasNext()) {
                DBObject dbItem = cursor.next();
                String text = dbItem.get("Text").toString();
                String reviewId = dbItem.get("ReviewId").toString();
                String business = dbItem.get("Business").toString();
                String date = dbItem.get("date").toString();
                String likes = dbItem.get("likes").toString();



                List<Pattern> patterns = extractor.run(text);
                for (Pattern pattern : patterns) {
                   System.out.println(pattern.toAspect());


                }
                done++;
                System.out.println("Done " + done + "/" + count);
            }
        } finally {
            cursor.close();
        }
    }





}
