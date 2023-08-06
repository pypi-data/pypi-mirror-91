# Double write this as pandas and Spark engine!
# annotator class approach based feature exraction
# annotators are categorized into groups. Based on their group and output_level, features will be extreacted

# Classifiers are categorized into
# Classification_levels:
# 1. (One-To-One-Token)  (POS, DEP, Lemm, Stemm, Token Embeds)                // Token level
# 2. (One-To-Less)  (NER/Chunk/Spell) Drop Tokens, results <=(len(input))     // Chunk
# 3  (One-To-One-Sent/Doc) (ClassifierDl, Sentiment, Sentence Embed,          //Input Dependent  (could be sentence/doc/even token)
# 4. (One-To-Many) i.e. (MulticlassiferDL, YAKE, ...?)                       // special_case, never explode on this?

#yake??
# 1. (Document/Sentence  to N?) (Yake)
# 2. (Document/Sentence to C class) (ClassifierDL,MultiClassifierDL/Sentiment/SentimentDl)

#1 to N token mappers
# Normalize, Stemm,

# Normalize maps 1 to N-K because it removes tokens and we get Nones

# Spark Based Feature extractors, one per Annotator class
import pyspark
def extract_ner_dl(sdf:pyspark.sql.DataFrame, ner_cols:List[str], meta:bool, is_at_pipe_output_level:bool):
    '''
    Ner has 3 types of features, NER-TAGs(merged), NER-IOB-TAGS, NER-Confidence,  and (?)
    :param sdf:
    :param ner_cols:
    :param meta:
    :param is_at_pipe_output_level:
    :return:
    '''
    for field in ner_cols:
        pass
