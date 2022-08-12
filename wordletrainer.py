import streamlit as st # this is for web app
import nltk # nltk for english words
from nltk.corpus import words
import pandas as pd
from nltk import FreqDist  # nltk words is to get five letter words

st.title("Wordle Optimizer") # this is the title of the app

st.image("https://www.washingtonpost.com/wp-apps/imrs.php?src=https://arc-anglerfish-washpost-prod-washpost.s3.amazonaws.com/public/LIXZHNDGMFENHEQSE6XR2YBURY.jpg&w=916")

# download the english words dictionary

@st.cache # cache the download process
def download():
    nltk.download('words')
download()


def check_string(string):
    alpha = 'abcdefghijklmnopqrstuvwxyz'
    if all(l in alpha for l in string) and string != '':
        return False
    else:
        return True

def letter_count(word_list):
    letter_dict = {'a': 0,'b': 0,'c': 0,'d': 0,'e': 0,'f': 0,'g': 0,'h': 0,'i': 0,'j': 0,'k': 0,'l': 0,'m': 0,'n': 0,'o': 0,'p': 0,'q': 0,'r': 0,'s': 0,'t': 0,'u': 0,'v': 0,'w': 0,'x': 0,'y': 0,'z': 0}
    for word in word_list:
        for w in word:
            for key in letter_dict:
                if w == key:
                    letter_dict[w] = letter_dict[w] + 1

    return letter_dict

def word_score(word,letter_dict):
    score = 0
    for l in ''.join(set(word)):
        score = score + letter_dict[l]

    return score


# create a new list with only five letter words
wordlist_lowercased = set(i.lower() for i in words.words())

five_letters = [word for word in wordlist_lowercased if len(word)==5]

# create a five column grid
st.markdown("### Green Letters")

[a,b,c,d,e] = st.columns(5)

# get user input currently doesnt handle number of characters

with a:
    fig = st.text_input(label="1st")
with b:
    sg = st.text_input(label="2nd")
with c:
    tg = st.text_input(label="3rd")
with d:
    fg = st.text_input(label="4th")
with e:
    ffg = st.text_input(label="5th")

st.markdown("### Yellow Letters")

[u,v,w,x,y] = st.columns(5)


with u:
    fiy = st.text_input(label="1st (can be multiple, no commas)")
with v:
    sy = st.text_input(label="2nd (can be multiple, no commas)")
with w:
    ty = st.text_input(label="3rd (can be multiple, no commas)")
with x:
    fy = st.text_input(label="4th (can be multiple, no commas)")
with y:
    ffy = st.text_input(label="5th (can be multiple, no commas)")

yellow = fiy + sy + ty + fy + ffy

st.markdown("### Eliminated Letters")

# exclusion letters where the grey grids are

exclusions = st.text_input(label="Input all letters (no commas) that are eliminated")

st.markdown("# What to Guess")


# this is an empty list to show all the clue words

clue_result = []


for word in five_letters:
 if (((word[0] == fig or check_string(fig))
     and (word[1] == sg or check_string(sg))
     and (word[2] == tg or check_string(tg))
     and (word[3] == fg or check_string(fg))
     and (word[4] == ffg or check_string(ffg)))
     and all( ye in word for ye in yellow)
     and not any(i == word[0] for i in fiy)
     and not any(i == word[1] for i in sy)
     and not any(i == word[2] for i in ty)
     and not any(i == word[3] for i in fy)
     and not any(i == word[4] for i in ffy)
     and not any(no in word for no in exclusions)):

    clue_result.append(word)


# print the output list of clues
letter_dict = letter_count(clue_result)

final_dict = {}

for word in clue_result:
    final_dict[word] = word_score(word,letter_dict)

final_df = pd.DataFrame.from_dict(final_dict, orient='index')

final_df = final_df.rename(columns={0: 'Word Probability Score'})


end_df = final_df.sort_values(by=['Word Probability Score'], ascending=False)

st.table(end_df)
