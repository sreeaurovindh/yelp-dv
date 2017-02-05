package edu.asu.nlp.yelp;
import java.io.*;
import java.util.ArrayList;
import java.util.List;
import java.util.Properties;

import org.json.*;

public class SimpleRunner extends Thread {
    private String filePath;
    private static SentimentAnalyser analyser;
    private static Properties prop = new Properties();
	private static InputStream propertiesInput = null;

    public SimpleRunner(String fileInput){
        this.filePath = fileInput;
        try {
        	propertiesInput = new FileInputStream("bucket-info.properties");
			prop.load(propertiesInput);
			analyser = new SentimentAnalyser(prop.getProperty("sentiword_doc"));
			
		} catch (IOException e) {
			// TODO Auto-generated catch block
			e.printStackTrace();
		}
    }
    public void run(){
    	writeJSONToFile();
    }

    public static void main(String[] args) {
    	
        File[] files = new File("D:\\Dropbox\\dv\\review_input\\").listFiles();
        for(File file:files){
            new SimpleRunner(file.getName()).start();
        }


    }
    public ArrayList<String> getBucketKeys(String bucketName){
    	return null;
    }
    public void writeJSONToFile(){
        String csvFile = "D:\\Dropbox\\dv\\review_input\\"+filePath;
        BufferedReader br = null;
        String line = "";


        try {
            String directoryOut = "D:\\Dropbox\\dv\\review_output\\";
            directoryOut= directoryOut+filePath+"_out.json";

            PrintWriter out = new PrintWriter(directoryOut);

            br = new BufferedReader(new FileReader(csvFile));
            br.readLine(); //skip First line
            while ((line = br.readLine()) != null) {
                JSONObject obj = new JSONObject(line);
                String reviewText = obj.get("text").toString();
                String cleanedText = reviewText.replaceAll("\n"," ").replaceAll("\\s\\s+/g", " ");
                String aspect = getAspect(cleanedText);
                obj.append("Aspect",aspect);
                String output =obj.toString();
                System.out.println(output);
                out.flush();
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
    public String getAspect(String input){
        StringBuilder output = new StringBuilder();
        Extract extract = new Extract();
        List<Pattern> patterns = extract.run(input);
        for (Pattern pattern : patterns) {
        	String typeOfWord = pattern.getModifierTag();
        	String modifier = pattern.getModifier();
        	double sentiment = analyser.extract(modifier, typeOfWord);
        	if(sentiment != Integer.MIN_VALUE){
        		 System.out.println(pattern.toAspect());
        		 System.out.println("===="+pattern+"==="+sentiment);
        	}
      
        	
        	
//            output.append(pattern.toAspect());
//            output.append("|");

        }
        return output.toString();
    }
    
}
