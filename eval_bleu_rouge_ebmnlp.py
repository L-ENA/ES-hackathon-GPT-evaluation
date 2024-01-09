import pandas as pd
import ast
import spacy
from rouge_score import rouge_scorer
import nltk
from nltk.translate.bleu_score import sentence_bleu, SmoothingFunction
from nltk.tokenize import word_tokenize
nltk.download('stopwords')
from nltk.corpus import stopwords
stopwords=stopwords.words('english')
stopwords.append('.')
stopwords.append(',')
stopwords.append('-')
nlp = spacy.load("en_core_web_sm")
tokenizer = spacy.blank("en")
chencherry = SmoothingFunction()


#######################setup: read csv file, create lists to save results, and decide which entity toe valuate
df=pd.read_csv(r'C:\Users\c1049033\PycharmProjects\hackathon\ebmnlp_evaluated.csv').fillna("")
#print(df.head())
ent='P'
label_col='{}_labels'.format(ent)
pred_col='{}_Prediction'.format(ent)


results=[]
bleus=[]
ro_p=[]
ro_r=[]
ro_f1=[]
unigram_overlap=[]

##############################EVAL for each row
for i,row in df.iterrows():
    if row[label_col] != "":#create lists from csv string cell contents
        label_list=ast.literal_eval(row[label_col])
    else:
        label_list=['']

    prediction=row[pred_col]
    print('--------------------')
    print("Labels: {}".format(label_list))
    print("Predictions: {}".format(prediction))
    ##########################################################BLEU see https://www.nltk.org/_modules/nltk/translate/bleu_score.html
    bleu_labels=[word_tokenize(s) for s in label_list]
    bleu_preds=word_tokenize(prediction)

    bleus.append(sentence_bleu(bleu_labels, bleu_preds, smoothing_function=chencherry.method5))#smoothing method 5 averages the adjacent n-gram results if there are no matching ngrams in one n-gram order
    print('BLEU score -> {}'.format(bleus[-1]))
    ###########################################################ROUGE


    scorer = rouge_scorer.RougeScorer(['rouge1', 'rougeL'], use_stemmer=True)
    scores = scorer.score('\n'.join(label_list),
                          prediction)

    ro_p.append(scores['rougeL'][0])
    ro_r.append(scores['rougeL'][1])
    ro_f1.append(scores['rougeL'][2])

    print('ROUGE score -> {}'.format(scores))
    ###################################################noun-chunks
    doc = nlp(prediction)
    pred_nouns=[np.text.lower() for np in doc.noun_chunks]

    label_nouns=[]
    for l in label_list:
        doc = nlp(l)
        x=[label_nouns.append(np.text.lower()) for np in doc.noun_chunks]

    pred_nouns=set(pred_nouns)
    label_nouns=set(label_nouns)
    print('-----Noun chunks overlap')
    print('     Label nouns: {}'.format(label_nouns))
    print('     Prediction nouns: {}'.format(pred_nouns))
    try:
        print('     Common nouns/all label nouns: {}/{} --> {}%'.format(len(pred_nouns.intersection(label_nouns)),len(label_nouns), (len(pred_nouns.intersection(label_nouns))/len(label_nouns))*100))
    except:
        print('     Common nouns/all label nouns: {}%'.format(0))

    ##############################################################Simple unigram oerlap
    print('----Simple terms overlap')

    doc=tokenizer(prediction)
    pred_words=[str(token).lower() for token in doc]
    pred_words = [w for w in pred_words if w not in stopwords]
    pred_words=set(pred_words)
    print('     Predicted words as set: {}'.format(pred_words))

    label_words=[]
    for l in label_list:
        doc = tokenizer(l)
        x=[label_words.append(str(token).lower()) for token in doc]
    label_words=[w for w in label_words if w not in stopwords]
    label_words=set(label_words)
    print('     Label words as set: {}'.format(label_words))
    try:
        print('     Common words/all label words: {}/{} --> {}%'.format(len(pred_words.intersection(label_words)),
                                                                        len(label_words), (len(pred_words.intersection(
                label_words)) / len(label_words)) * 100))
        unigram_overlap.append((len(pred_words.intersection(
                label_words)) / len(label_words)) * 100)
    except:
        print('     Common words/all label words: {}%'.format(0))
        unigram_overlap.append(0)
    print('     Common words were: {}'.format(pred_words.intersection(label_words)))

###########################################################create output DF
df['{} BLEU Score'.format(ent)]=bleus
df['{} ROUGE Precision Score'.format(ent)]=ro_p
df['{} ROUGE Recall Score'.format(ent)]=ro_r
df['{} ROUGE F1 Score'.format(ent)]=ro_f1
df['{} Simple Unigram Overlap Percentage'.format(ent)]=unigram_overlap
df.to_csv(r'C:\Users\c1049033\PycharmProjects\hackathon\ebmnlp_evaluated.csv', index=False)









