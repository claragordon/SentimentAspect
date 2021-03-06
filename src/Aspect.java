/**
 * @author Clara Gordon
 */
class Aspect {
	private String text;
	private int start;
	private int end;

	private String polarity;

	public Aspect(String text, int start, int end, String polarity) {
		this.text = text;
		this.start = start;
		this.end = end;
		this.polarity = polarity;
	}


	public String getText() {
		return this.text;
	}

	public int getStart() {
		return this.start;
	}

	public int getEnd() {
		return this.end;
	}

	public String getPolarity() {
		return this.polarity;
	}

	public String toString() {
		return ("Aspect: \"" + text + "\" Start: " + start + " End: " + end);
	}

}

