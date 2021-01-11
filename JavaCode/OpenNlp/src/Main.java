import java.io.FileInputStream;
import java.io.IOException;
import java.io.InputStream;
import java.nio.charset.StandardCharsets;
import java.nio.file.Files;
import java.nio.file.Path;
import java.util.HashSet;
import java.util.Set;

import opennlp.tools.cmdline.PerformanceMonitor;
import opennlp.tools.cmdline.parser.ParserTool;
import opennlp.tools.parser.Parse;
import opennlp.tools.parser.Parser;
import opennlp.tools.parser.ParserFactory;
import opennlp.tools.parser.ParserModel;

//extract noun phrases from a single sentence using OpenNLP

/*
public class Main {

	static String sentence = "Due to the highly volatile and competitive nature of the industries in which the Company competes, the Company must continually introduce new products, services and technologies, enhance existing products and services, and effectively stimulate customer demand for new and upgraded products.";

	static Set<String> nounPhrases = new HashSet<>();

	public static void main(String[] args) {

		InputStream modelInParse = null;
		try {
			// load chunking model
			modelInParse = new FileInputStream(
					"C:\\Users\\Claudiu\\Desktop\\apache-opennlp-1.9.3\\en-parser-chunking.bin"); // from
																									// http://opennlp.sourceforge.net/models-1.5/
			ParserModel model = new ParserModel(modelInParse);

			// create parse tree
			Parser parser = ParserFactory.create(model);
			Parse topParses[] = ParserTool.parseLine(sentence, parser, 1);

			// call subroutine to extract noun phrases
			for (Parse p : topParses)
				getNounPhrases(p,0);

			// print noun phrases
			for (String s : nounPhrases)
				System.out.println(s);

			// The Call
			// the Wild?
			// The Call of the Wild? //punctuation remains on the end of sentence
			// the author of The Call of the Wild?
			// the author
		} catch (IOException e) {
			e.printStackTrace();
		} finally {
			if (modelInParse != null) {
				try {
					modelInParse.close();
				} catch (IOException e) {
				}
			}
		}
	}

	// recursively loop through tree, extracting noun phrases
	public static void getNounPhrases(Parse p, int count) {

		if (p.getType().equals("NP")) { // NP=noun phrase
			if(count>7) {
			nounPhrases.add(p.getCoveredText());}
		}
		for (Parse child : p.getChildren())
			getNounPhrases(child, count++);
		
	}
}*/

import java.io.BufferedWriter;
import java.io.File;
import java.io.FileWriter;
import java.util.ArrayList;
import java.util.Arrays;
import java.util.HashMap;
import java.util.List;
import java.util.Map;
import java.util.Scanner;

import opennlp.tools.chunker.ChunkerME;
import opennlp.tools.chunker.ChunkerModel;
import opennlp.tools.postag.POSModel;
import opennlp.tools.postag.POSTaggerME;
import opennlp.tools.tokenize.TokenizerME;
import opennlp.tools.tokenize.TokenizerModel;
import opennlp.tools.tokenize.WhitespaceTokenizer;
import opennlp.tools.util.Span;

/**
 *
 * Extracts noun phrases from a sentence. To create sentences using OpenNLP use
 * the SentenceDetector classes.
 */
public class Main {

	private static void countFrequencies(String[] chunkStrings) {
		// hashmap to store the frequency of element
		Map<String, Integer> hm = new HashMap<String, Integer>();

		for (String i : chunkStrings) {
			Integer j = hm.get(i);
			hm.put(i, (j == null) ? 1 : j + 1);
		}

		// displaying the occurrence of elements in the arraylist
		for (Map.Entry<String, Integer> val : hm.entrySet()) {
			System.out.println("Element " + val.getKey() + " " + "occurs" + ": " + val.getValue() + " times");
		}
	}

	private static void outputToCsv(Map<String, Integer> hm) {
		try {
			File myObj = new File("C:\\Users\\Claudiu\\Desktop\\Programming\\NLPProgramming\\Counts\\JavaVP.csv");
			myObj.createNewFile();
			FileWriter fw = new FileWriter(myObj.getAbsoluteFile());
			BufferedWriter bw = new BufferedWriter(fw);
			bw.write("word, count\n");

			for (Map.Entry<String, Integer> val : hm.entrySet()) {
				bw.write(val.getKey() + ", " + val.getValue() + "\n");
			}
			bw.close();
		} catch (IOException e) {
		}
	}

	public static void main(String[] args) {

		try {
			String modelPath = "C:\\\\Users\\\\Claudiu\\\\Desktop\\\\apache-opennlp-1.9.3\\\\";
			WhitespaceTokenizer wordBreaker = WhitespaceTokenizer.INSTANCE;
			POSModel pm = new POSModel(new FileInputStream(new File(modelPath + "en-pos-maxent.bin")));
			POSTaggerME posme = new POSTaggerME(pm);
			InputStream modelIn = new FileInputStream(modelPath + "en-chunker.bin");
			ChunkerModel chunkerModel = new ChunkerModel(modelIn);
			ChunkerME chunkerME = new ChunkerME(chunkerModel);
			Map<String, Integer> hm = new HashMap<String, Integer>();
			File directoryPath = new File("C:\\Users\\Claudiu\\Desktop\\Programming\\NLPProgramming\\TextFiles");
			// List of all files and directories
			String contents[] = directoryPath.list();
			System.out.println("List of files and directories in the specified directory:");
			for (int k = 0; k < contents.length; k++) {
				System.out.println(contents[k]);
				FileInputStream fis= new FileInputStream("C:\\Users\\Claudiu\\Desktop\\Programming\\NLPProgramming\\TextFiles\\"+contents[k]);       
				Scanner sc = new Scanner(fis,StandardCharsets.UTF_8);
				while(sc.hasNextLine())  
				{  
				String sentence = sc.nextLine();      //returns the line that was skipped  
				
				// this is your sentence
				// String sentence = "Due to the highly volatile and competitive nature of the
				// industries in which the Company competes, the Company must continually
				// introduce new products, services and technologies, enhance existing products
				// and services, and effectively stimulate customer demand for new and upgraded
				// products.";
				sentence = sentence.toLowerCase();
				sentence = sentence.replaceAll("[^A-Za-z—\\-\\'\\’\\ ]", " ").replaceAll("\s+", " ");
				// words is the tokenized sentence
				String[] words = wordBreaker.tokenize(sentence);
				
				/*
				 * use this for tokenization for (int i = 0; i < words.length; i++) {
				 * System.out.println(words[i]); }
				 */
				// posTags are the parts of speech of every word in the sentence (The chunker
				// needs this info of course)
				String[] posTags = posme.tag(words);
				// chunks are the start end "spans" indices to the chunks in the words array
				Span[] chunks = chunkerME.chunkAsSpans(words, posTags);
				// chunkStrings are the actual chunks
				String[] chunkStrings = Span.spansToStrings(chunks, words);
				
				for (int i = 0; i < chunks.length; i++) {
					if (chunks[i].getType().equals("VP")) {
						Integer j = hm.get(chunkStrings[i]);
						hm.put(chunkStrings[i], (j == null) ? 1 : j + 1);
					}
				}
				}
				sc.close();
			}
			
			outputToCsv(hm);
		} catch (IOException e) {
		}
	}

}