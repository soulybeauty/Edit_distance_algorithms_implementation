import re 
import sqlite3

# Function to check if a string contains digits
def contains_digits(string):
    return any(char.isdigit() for char in string)

# Function to get plain vocabulary from a file
def get_plain_vocabluary():
    plain_vocab = []
    with open(r'words.txt', 'r', encoding='utf-8') as f:
        words = f.read()
        plain_vocab.extend(words.split())
    plain_vocab = filter(lambda x: ((not x.isdigit()) and (not re.search("\W", string=x)) and (not contains_digits(x))), plain_vocab)
    return list(set(plain_vocab))

# Function to clean a sentence by removing non-word characters
def cleaner(sentence):
    a = " ".join(re.split(pattern='\W', string=sentence))
    print(a)
    return a

# Function to insert data into a SQLite database
def insert_database(data, TABLENAME):
    conn = sqlite3.connect("outputs.db")
    cursor = conn.cursor()
    cursor.executemany(f'''
    INSERT INTO {TABLENAME} VALUES (?, ?, ?, ?, ?, ?, ?)
    ''', data)
    conn.commit()
    cursor.close()
    conn.close()

if __name__ == '__main__':
    # Read words from a file and join the first 10 words that are not digits
    with open("words.txt" ,"r", encoding="utf-8") as f:
        words = " ".join(list(filter(lambda x: not x.isdigit() and ((False) if len(x) == 0 else ()), f.read().split()[:10])))
    print(words)
