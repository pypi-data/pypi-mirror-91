"""Main module."""
import re
import string
import pandas as pd
import importlib_resources


ocrfixr = importlib_resources.files("ocrfixr")
word_set = (ocrfixr / "data" / "SCOWL_70.txt").read_text().split()
word_set = set(word_set)

common_words = (ocrfixr / "data" / "SCOWL_10.txt").read_text().split()
common_words = set(common_words)


class unsplit:                       
    def __init__(self, text, return_fixes = "F"):
        self.text = text
        self.return_fixes = return_fixes

        
### DEFINE ALL HELPER FUNCTIONS
# ------------------------------------------------------
# Find all split words in a passage.


    def _LIST_SPLIT_WORDS(self):
        tokens = re.split(" |(?<!-)\n", self.text)
        tokens = [l.strip() for l in tokens] 
        # First, drop hyphenated words, those with apostrophes (which may be intentional slang), words that are just numbers, and words broken across lines
        # Note: This does risk missing valid misreads, but our goal is to avoid "bad" corrections
        regex = re.compile("[a-zA-Z'-]+(-\n)[a-zA-Z'-]+")
        has_newline = [x for x in tokens if regex.match(x)]
        # Pick up all words with a newline (/n) inside them
        # then, remove punct from each remaining token (such as trailing commas, periods, quotations ('' & ""), but KEEPING contractions). 
        no_punctuation = [l.strip(string.punctuation) for l in has_newline]
        split_words = no_punctuation
           
        return(split_words)

        
    # Decides whether a split word should retain its hyphen
    # To accomplish this, OCRfixr checks the hyphenated word against the accepted word list:
    # - If word IS recognized without the hyphen, and both word halves are NOT recognized, REMOVE THE HYPHEN. (ex: dis-played --> displayed)
    # - If word IS recognized without the hyphen, and both word halves ARE recognized, KEEP THE HYPHEN and add a * directly after the hyphen, to flag for the editor that OCRfixr is uncertain (ex. English-man --> English-*man)
    # - However, if that unhyphenated word is very common, then just REMOVE THE HYPHEN, even if both halves of the word are valid (ex. with-in --> within)
    # - If word is NOT recognized without the hyphen, and both word halves ARE recognized, KEEP THE HYPHEN. (ex: well-meaning --> well-meaning)
    # - If word is NOT recognized without the hyphen, and both word halves are NOT recognized, REMOVE THE HYPHEN. These are assumed to be proper nouns.(ex: McAl-ister --> McAlister)

    def __DECIDE_HYPHEN(self, text):
        
        # 3 columns: Full_Word, First_Half, Second_Half
        w = pd.DataFrame(data={"Full_Word": text})
        w = w.replace("^[[:punct:]]|[[:punct:]]$", "")
        w["No_Hyphen"] = w["Full_Word"].replace("-\n", "")
        w["First_Half"] = w["Full_Word"].replace("-\n.*", "")
        w["Second_Half"] = w["Full_Word"].replace("[A-z0-9]*-\n", "")

        # add checks
        # 1) Full_Word valid?
        # 2) First_Half valid?
        # 3) Second_Half valid?
        # 4) Full_Word common?
        w["Full_Word_Common"] = w["No_Hyphen"].lower()
        
        
                                 # Check each version of the hyphenated word to see if it is in SCOWL_50 (full word w/ hyphen removed + word halves). This will determine if the hyphen stays, goes, or is flagged
                            .[,FullWordValid:=ifelse(tolower(NoHyphen) %in% Dict$Correct, TRUE, FALSE)] %>%
                            .[,FullWordCommon:=ifelse(tolower(NoHyphen) %in% Dict[ShortList ==1]$Correct, TRUE, FALSE)] %>%
                            .[,WordHalvesValid:=ifelse(tolower(FirstHalf) %in% Dict$Correct & tolower(SecondHalf) %in% Dict$Correct , TRUE, FALSE)] %>%
                            .[,ContainsNum:=ifelse(grepl("[0-9]", FirstHalf) == TRUE | grepl("[0-9]", SecondHalf) == TRUE, TRUE, FALSE)] %>%
                            .[,ProperNoun:=ifelse(grepl("^[[:upper:]]", FirstHalf) == FALSE & grepl("^[[:upper:]]", SecondHalf) == TRUE, TRUE, FALSE)] %>%
                        
                            # Recognized full word + in SCOWL 10 (REMOVE)
                            # Recognized full word + invalid word halves (REMOVE)
                            # Recognized full word + valid word halves (KEEP + FLAG)
                            # Unrecognized full word + valid word halves (KEEP)
                            # Unrecognized full word + invalid word halves (REMOVE)
                        
                            .[,Correct:=ifelse(FullWordCommon == TRUE, sub("-\n", "", Word),
                                        ifelse(FullWordValid == TRUE & WordHalvesValid == FALSE, sub("-\n+", "", Word),
                                        ifelse(FullWordValid == TRUE & WordHalvesValid == TRUE, sub("-\n+", "-*", Word),
                                        ifelse(ContainsNum == TRUE | ProperNoun == TRUE | (FullWordValid == FALSE & WordHalvesValid == TRUE), sub("-\n+", "-", Word),
                                                                                                sub("-\n+", "", Word)))))] %>%

                                
        # add \n to end of word
        w["Correct"] = w["Correct"] + "\n"

        suggested_words = w["Correct"]
        
        return(suggested_words)
           

    
    # note that multi-replace will replace ALL instances of a split word. Hyphenation is NOT context-specific, it is rule-based
    def _MULTI_REPLACE(self, fixes):
        # if there are no fixes, just return the original text
        if len(fixes) == 0 :
            return(self.text)
        else:
        # otherwise, replace all dict entries with the approved replacement word
            fixes = dict((re.escape(k), v) for k, v in fixes.items()) 
            pattern = re.compile("|".join(fixes.keys()))
            text_corrected = pattern.sub(lambda m: fixes[re.escape(m.group(0))], self.text)
            return(text_corrected)
    
     
    def _FIND_REPLACEMENTS(self, splits):
        new_word = [] 
        # for each split word, decide how to hyphenate it, then add to a dict
        for i in splits:
            new_word.append(self.__DECIDE_HYPHEN(i))

        fixes = dict(zip(splits, new_word))
                
        return(fixes)
    
    
    # Define method for un-splitting words
    def fix(self):
        split = self._LIST_SPLIT_WORDS()
        
        # if no misreads, just return the original text, adding empty set {} if user requested return_fixes
        if len(split) == 0:
            if self.return_fixes == "T":
                unchanged_text = [self.text, {}]
            else:
                unchanged_text = self.text
            return(unchanged_text)
        
        # Based on user input, either outputs just the full corrected text, or also itemizes the changes
        else:
            fixes = self._FIND_REPLACEMENTS(split)
            correction = self._MULTI_REPLACE(fixes)
            
            if self.return_fixes == "T":
                full_results = [correction, fixes]
            else:
                full_results = correction
            return(full_results)


