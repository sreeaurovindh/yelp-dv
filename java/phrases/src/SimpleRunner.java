import java.io.*;
import java.util.List;

import org.json.*;

public class SimpleRunner {

    public static void main(String[] args) {
        String csvFile = "D:\\Dropbox\\dv\\yelp_dataset_challenge_academic_dataset\\yelp_academic_dataset_review.json";
        BufferedReader br = null;
        String line = "";


        try {
            PrintWriter out = new PrintWriter("D:\\Dropbox\\dv\\yelp_cleaned\\review.json");

            br = new BufferedReader(new FileReader(csvFile));
            br.readLine(); //skip First line
            while ((line = br.readLine()) != null) {
              JSONObject obj = new JSONObject(line);
              String reviewText = obj.get("text").toString();
              String cleanedText = reviewText.replaceAll("\n"," ").replaceAll("\\s\\s+/g", " ");
              String aspect = getAspect(cleanedText);
              obj.append("Aspect",aspect);
              String output =obj.toString();
              out.println(output);
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
    public static String getAspect(String input){
        StringBuilder output = new StringBuilder();
        Extract extract = new Extract();
        List<Pattern> patterns = extract.run(input);
        for (Pattern pattern : patterns) {
            output.append(pattern.toAspect());
            output.append("|");

        }
        return output.toString();
    }
}
