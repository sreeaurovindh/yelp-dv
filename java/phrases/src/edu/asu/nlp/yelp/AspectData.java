package edu.asu.nlp.yelp;

public class AspectData {
	private String item;

	private String value;
	private double polarity;
	
	public AspectData(String item,String value,double polarity){
		this.item = item;
		this.value = value;
		this.polarity = polarity;
	}
	public String getItem() {
		return item;
	}

	public void setItem(String item) {
		this.item = item;
	}

	public String getValue() {
		return value;
	}

	public void setValue(String value) {
		this.value = value;
	}

	public double getPolarity() {
		return polarity;
	}

	public void setPolarity(double polarity) {
		this.polarity = polarity;
	}

}
