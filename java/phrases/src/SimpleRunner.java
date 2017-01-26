import java.io.*;
import java.util.List;

import org.json.*;

public class SimpleRunner extends Thread {
    String filePath;
    public SimpleRunner(String fileInput){
        this.filePath = fileInput;
    }
    public void run(){
        RunAspect();
    }

    public static void main(String[] args) {
        File[] files = new File("D:\\Dropbox\\dv\\review_input\\").listFiles();
        for(File file:files){
            new SimpleRunner(file.getName()).start();
        }


    }
    public void RunAspect(){
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
    public String getAspect(String input){
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
