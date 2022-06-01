import csv
import praw
import pandas as pd
import os
import tkinter as tk
from tkinter import *
from tkinter import ttk
from tkinter.ttk import *
import tkinter as tk
from tkinter import ttk
from tkinter.ttk import Combobox
root = tk.Tk()

praw_ini = """[DEFAULT]
# A boolean to indicate whether or not to check for package updates.
check_for_updates=True

# Object to kind mappings
comment_kind=t1
message_kind=t4
redditor_kind=t2
submission_kind=t3
subreddit_kind=t5
trophy_kind=t6

# The URL prefix for OAuth-related requests.
oauth_url=https://oauth.reddit.com

# The URL prefix for regular requests.
reddit_url=https://www.reddit.com

# The URL prefix for short URLs.
short_url=https://redd.it
"""

if not os.path.exists("praw.ini"):
    with open("praw.ini", "w") as f:
        f.write(praw_ini)
reddit = praw.Reddit(
    client_id="JZLKX7E8o33kQg",
    client_secret="JIMYG_JYO_Ii1zZPcoh-9NCTLNY",
    user_agent="PSOSM")


try:
    os.remove('data_type_1.csv')
except BaseException:
    pass
try:
    os.remove('Final_Score.csv')
except BaseException:
    pass


def find_spam(search_query):

    authors = []
    comments = []
    upvotes = []
    text = []

    for submission in reddit.subreddit("all").search(
            search_query, sort="new", limit=10000):

        text.append(submission.title)
        upvotes.append(submission.score)
        comments.append(submission.num_comments)
        authors.append(submission.author)

    with open("data_type_1.csv", 'a', encoding='utf-8') as file:
        writer = csv.writer(file)
        for i in range(len(authors)):
            writer.writerow([authors[i], text[i], upvotes[i],
                            comments[i], search_query])


def process_data():
    df = pd.read_csv('data_type_1.csv')
    authors = []
    st = []
    upvotes = []
    comments = []
    u = []
    e = []
    s = []
    d = []
    for i in range(len(df)):

        auth = df.iloc[i][0]
        if auth not in authors:
            authors.append(auth)
            st.append(df.iloc[i][1])
            upvotes.append(df.iloc[i][2])
            comments.append(df.iloc[i][3])
            plat = df.iloc[i][4]
            if (plat == 'udemy'):
                u.append(1)
            else:
                u.append(0)
            if (plat == 'eduonix'):
                e.append(1)
            else:
                e.append(0)
            if (plat == 'skillshare'):
                s.append(1)
            else:
                s.append(0)
            if (plat == 'edx'):
                d.append(1)
            else:
                d.append(0)

        else:
            ind = authors.index(auth)
            st[ind] = st[ind] + " " + df.iloc[i][1]
            upvotes[ind] += df.iloc[i][2]
            comments[ind] += df.iloc[i][3]
            plat = df.iloc[i][4]
            if (plat == 'udemy'):
                u[ind] += 1
            elif (plat == 'eduonix'):
                e[ind] += 1
            elif (plat == 'skillshare'):
                s[ind] += 1
            else:
                e[ind] += 1

    df2 = pd.DataFrame({'Authors': authors,
                        'Total text': st,
                        'Total Upvotes': upvotes,
                        'Total Comments': comments,
                        'Udemy posts': u,
                        'Eduonix posts': e,
                        'Skillshare posts': s,
                        'Edx posts': d,
                        })

    scores = []
    dity_words = pd.read_csv('dirty.csv')
    print('Computing Scores!!')
    for i in range(len(df2)):
        s = 0
        for j, row in dity_words.iterrows():
            s += df2.iloc[i]['Total text'].count(row[0])
        scores.append(s)

    m = max(scores)
    scores_l = [s / float(m) for s in scores]
    df2['score'] = pd.Series(scores_l)
    df2 = (
        df2.sort_values(
            by=['score'],
            ascending=False)).reset_index(
        drop=True)
    df2.to_csv('Final_Score.csv', index=False)


LARGE_FONT = ("Verdana", 12)
NORM_FONT = ("Helvetica", 10)
SMALL_FONT = ("Helvetica", 8)


def popupmsg():
    popup = tk.Tk()
    popup.wm_title("!")
    label = ttk.Label(popup, text='Please Load New Data', font=NORM_FONT)
    label.pack(side="top", fill="x", pady=10)
    B1 = ttk.Button(popup, text="Okay", command=popup.destroy)
    B1.pack()
    popup.mainloop()


def get_spam_authors_by_platform(platform):
    ind = 0
    if(platform == 'udemy'):
        ind = 4
    elif(platform == 'eduonix'):
        ind = 5
    elif(platform == 'skillshare'):
        ind = 6
    else:
        ind = 7
    auth_score = []
    try:
        df = pd.read_csv('Final_Score.csv')

        for i in range(len(df)):
            if (df.iloc[i][ind] != 0):
                temp = df.iloc[i][8]
                if temp > 0.0:
                    temp = 'Spammer'
                else:
                    temp = 'Not a Spammer'
                auth_score.append([i + 1, df.iloc[i][0], temp])

        return auth_score
    except BaseException:
        popupmsg()
        return auth_score


def get_spammer_by_name(name):
    try:
        df = pd.read_csv('Final_Score.csv')
        score = 0
        f = 0
        rank = 0
        for i in range(len(df)):
            if (df.iloc[i][0] == name):
                score = df.iloc[i][8]
                u = df.iloc[i][4]
                ed = df.iloc[i][5]
                s = df.iloc[i][6]
                e = df.iloc[i][7]
                if score > 0.0:
                    score = 'Spammer'
                else:
                    score = 'Not a Spammer'
                f = 1
                rank = i + 1
                break
        if (f == 1):
            return rank, name, score, u, ed, s, e
        else:
            return -1, -1, -1, -1, -1, -1, -1
    except BaseException:
        popupmsg()
        return -2, -2, -2, -2, -2, -2, -2


# This button will initialize
# the progress bar


def get_data():
    progress = Progressbar(root, orient=HORIZONTAL,
                           length=100, mode='determinate')

    progress.pack(expand=True, fill=tk.BOTH, side=tk.TOP)

    try:
        os.remove('data_type_1.csv')
        os.remove('Final_Score.csv')
    except BaseException:
        pass

    import time
    progress['value'] = 20
    root.update_idletasks()

    with open("data_type_1.csv", 'a') as file:
        writer = csv.writer(file)
        writer.writerow(["Author", "Text", "Upvotes", "Comments", "Platform"])

    progress['value'] = 40
    root.update_idletasks()
    print('Collecting Data!!')
    find_spam('udemy')
    find_spam('eduonix')
    find_spam('skillshare')
    find_spam('edx')
    progress['value'] = 80
    root.update_idletasks()
    print("Data Collected, now processing")
    process_data()
    progress['value'] = 100
    root.update_idletasks()
    print("Score Computed Successfully!!")
    progress.destroy()


v = ['udemy', 'eduonix', 'skillshare', 'edx']
canvas1 = tk.Canvas(root, width=400, height=300, relief='raised')
canvas1.pack()


label1 = tk.Label(root, text='Reddit Educational Spam Analyser')
label1.config(font=('helvetica', 15))
canvas1.create_window(200, 25, window=label1)

label2 = tk.Label(root, text='Author')
label2.config(font=('helvetica', 10))
canvas1.create_window(80, 100, window=label2)


entry1 = tk.Entry(root)
canvas1.create_window(80, 130, window=entry1)
label4 = tk.Label(root, text=' Platform')
label4.config(font=('helvetica', 10))
canvas1.create_window(280, 100, window=label4)

b = StringVar()
entry3 = Combobox(root, textvariable=b, state="readonly", values=v)
canvas1.create_window(280, 130, window=entry3)


def author():
    def show():
        rank, name, rating, udemy, edu, ski, ed = get_spammer_by_name(
            entry1.get())
        if name == -1:
            name = '                  Author Not Found'
            rank = ''
            rating = ''
        res = ''
        if udemy > 0:
            res = res + 'Udemy'
        if edu > 0:
            res = res + ' Eduonix'
        if ski > 0:
            res = res + ' Skillshare'
        if ed > 0:
            res = res + ' EDX'
        listBox.insert("", "end", values=(rank, name, rating, res))
    table = tk.Tk()
    label = tk.Label(
        table,
        text="Table",
        font=(
            "Arial",
            30)).grid(
        row=0,
        columnspan=3)
    cols = ("Rank", "Author", "Classified as", "Platforms")
    listBox = ttk.Treeview(table, columns=cols, show='headings')
    for col in cols:
        listBox.heading(col, text=col)
    listBox.grid(row=1, column=0, columnspan=2)
    showScores = tk.Button(
        table,
        text="Show scores",
        width=15,
        command=show).grid(
        row=4,
        column=0)
    closeButton = tk.Button(
        table,
        text="Close",
        width=15,
        command=table.destroy).grid(
        row=4,
        column=1)
    table.mainloop()


button1 = tk.Button(
    text='Check Author',
    command=author,
    bg='brown',
    fg='white',
    font=(
        'helvetica',
        9,
         'bold'))
canvas1.create_window(60, 280, window=button1)

buttonx = tk.Button(
    text='Load New Data',
    command=get_data,
    bg='brown',
    fg='white',
    font=(
        'helvetica',
        9,
         'bold'))
canvas1.create_window(190, 280, window=buttonx)


def platform():
    def show():
        x = get_spam_authors_by_platform(entry3.get())

        for i, (Ranking, Author, Rating) in enumerate(x, start=1):
            listBox.insert("", "end", values=(Ranking, Author, Rating))
    table = tk.Tk()
    label = tk.Label(
        table,
        text="Table",
        font=(
            "Arial",
            30)).grid(
        row=0,
        columnspan=3)
    cols = ("Rank", "Author", "Classified as")
    listBox = ttk.Treeview(table, columns=cols, show='headings')
    for col in cols:
        listBox.heading(col, text=col)
    listBox.grid(row=1, column=0, columnspan=2)
    showScores = tk.Button(
        table,
        text="Show scores",
        width=15,
        command=show).grid(
        row=4,
        column=0)
    closeButton = tk.Button(
        table,
        text="Close",
        width=15,
        command=table.destroy).grid(
        row=4,
        column=1)
    table.mainloop()


button2 = tk.Button(
    text='Check Platform',
    command=platform,
    bg='brown',
    fg='white',
    font=(
        'helvetica',
        9,
         'bold'))
canvas1.create_window(340, 280, window=button2)

root.mainloop()
