package edu.asu.nlp.yelp;
import java.io.*;
import java.util.ArrayList;
import java.util.Iterator;
import java.util.List;
import java.util.Properties;

import org.json.*;

public class SimpleRunner extends Thread {
    private String filePath;
    private static SentimentAnalyser analyser;
	private static String inputFolder;
	private static String outputFolder;

    public SimpleRunner(String fileInput){
        this.filePath = fileInput;
       
    }
    public void run(){
    	writeJSONToFile();
    }
    public static void readPreferences(){
    	 try {
    		Properties prop = new Properties();
    		 InputStream propertiesInput = new FileInputStream("bucket-info.properties");
    		 prop.load(propertiesInput);
 			analyser = new SentimentAnalyser(prop.getProperty("sentiword_doc"));
 			inputFolder = prop.getProperty("input_folder");
 			outputFolder = prop.getProperty("output_folder");
 			
 		} catch (IOException e) {
 			// TODO Auto-generated catch block
 			e.printStackTrace();
 		}
    }
    public static void main(String[] args) {
    	
    	readPreferences();
        File[] files = new File(inputFolder).listFiles();
        for(File file:files){
            new SimpleRunner(file.getName()).start();
        }


    }
    public ArrayList<String> getBucketKeys(String bucketName){
    	return null;
    }
    public void writeJSONToFile(){
        String jsonFile = inputFolder+filePath;
        BufferedReader br = null;
        String line = "";


        try {
 
            String directoryOut= outputFolder+filePath+"_out.json";

            PrintWriter out = new PrintWriter(directoryOut);

            br = new BufferedReader(new FileReader(jsonFile));
            br.readLine(); //skip First line
            int count = 0;
            while ((line = br.readLine()) != null) {
            	count += 1;
                JSONObject obj = new JSONObject(line);
                String reviewText = obj.get("text").toString();
                String businessId = obj.get("business_id").toString();
                String reviewId = obj.getString("review_id");
                double stars = obj.getDouble("stars");
                String date = obj.get("date").toString();
                int useful = obj.getInt("useful");
                int funny = obj.getInt("funny");
                
              
                
                ArrayList<AspectData> aspect = getAspect(reviewText);
                Iterator<AspectData> aspItr = aspect.iterator();
                while(aspItr.hasNext()){
                	AspectData data = aspItr.next();
                	JSONObject newObject = new JSONObject();
                	newObject.put("item", data.getItem());
                	newObject.put("value", data.getValue());
                	newObject.put("polarity",data.getPolarity());
                	newObject.put("business_id", businessId);
                	newObject.put("reviewId", reviewId);
                	newObject.put("rev_stars",stars);
                	newObject.put("date", date);
                	newObject.put("useful",useful);
                	newObject.put("funny",funny);
                	newObject.put("is_review", 1);
                	newObject.put("is_tip", 0);
//                	System.out.println(newObject);
                	out.println(newObject);
                	out.flush();
                }
//                System.out.println("Total Reveiws processed:"+count);
                 
            }



        } catch (FileNotFoundException e) {
            e.printStackTrace();
        } catch (IOException e) {
            e.printStackTrace();
        } finally {
            if (br != null) {
                try {
                    br.close();
                } catch (IOException e) {
                    e.printStackTrace();
                }
            }
        }
    }
    public ArrayList<AspectData> getAspect(String input){
    	ArrayList<AspectData> output = new ArrayList<AspectData>();
        Extract extract = new Extract();
        List<Pattern> patterns = extract.run(input);
        for (Pattern pattern : patterns) {
        	String typeOfWord = pattern.getModifierTag();
        	String modifier = pattern.getModifier();
        	double sentiment = analyser.extract(modifier, typeOfWord);
        	if(sentiment != Integer.MIN_VALUE){ 		 
//        		 System.out.println(pattern.toAspect());
//        		 System.out.println("==HEAD=="+pattern.getHead()+"==MOD="+pattern.getModifier()+"=SENTIMENT=="+sentiment);
        		 AspectData data = new AspectData(pattern.getHead(),pattern.getModifier(),sentiment);
        		 output.add(data);
        		 
        	}
      
        }
        return output;
    }
    
}
