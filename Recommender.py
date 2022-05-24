import numpy as np
import matplotlib.pyplot as plt
from tkinter import messagebox
from collections import Counter
import CosineSim
from CosineSim import cosineSimilarity, text_to_vector
from Book import *
from tkinter import *
from tkinter.filedialog import askopenfilename
from tkinter import simpledialog
import tkinter
main = tkinter.Tk()
main.title("Online Book Recommendation System by using Collaborative filtering and Association Mining")
main.geometry("1000x500")

bookList = []
filterList = []
suggestList = []
recommend_list = []
global mae
global size

def uploadDataset():
    global size
    dataset = askopenfilename()
    name.config(text=dataset)
    with open(dataset, "r") as file:
      for line in file:
       line = line.strip('\n')
       arr = line.split(";")
       if len(arr) == 5:
         book = Book()
         book.setISBN(arr[0])
         book.setBook(arr[1])
         book.setAuthor(arr[2])
         book.setPublishYear(arr[3])
         book.setPublisher(arr[4])
         bookList.append(book);

    size = len(bookList)
    for book in bookList:
      text.insert(END,book.getISBN()+"\t\""+book.getBook()+"\"\t\""+book.getAuthor()+"\"\t\""+book.getPublishYear()+"\"\t\""+book.getPublisher()+"\"\n")

         
	 
def filterDataset():
        text.delete('1.0', END)
        data = ""
        for book in bookList:
          data = book.getISBN()+" "+book.getBook()+" "+book.getAuthor()+" "+book.getPublishYear()+" "+book.getPublisher()
          data = CosineSim.text_to_vector(data)
          text.insert(END,data)
          filterList.append(data)
        messagebox.showinfo("Dataset filtered successfully","Dataset filtered successfully")

	    






def getSuggestion(book):
    for books in bookList:
       if book.getAuthor() == books.getAuthor():
           title = books.getBook()
           for temp in bookList:
              if book.getAuthor != temp.getAuthor() and temp.getBook() == title:
                 if temp.getAuthor() not in recommend_list:
                    if temp.getAuthor() != books.getAuthor():
                        recommend_list.append(temp.getAuthor())
    


def suggest():
    global size
    global mae
    found = 0;
    recommend_list.clear()
    input = simpledialog.askstring("Filter", "Enter Filter String",parent=main)
    filter = CosineSim.text_to_vector(input)
    suggest = ""
    for book in bookList:
       data = book.getISBN()+" "+book.getBook()+" "+book.getAuthor()+" "+book.getPublishYear()+" "+book.getPublisher()
       data = CosineSim.text_to_vector(data)
       cosine = CosineSim.cosineSimilarity(data, filter)
       if cosine > 0.0:
          data = getSuggestion(book)
          suggest = suggest + book.getISBN()+"\t\""+book.getBook()+"\"\t\""+book.getAuthor()+"\"\t\""+book.getPublishYear()+"\"\t\""+book.getPublisher()+"\"\t\""+str(cosine)+"\"\n"
          found = found + 1
    mae = found;
    text.delete('1.0', END)
    text.insert(END,suggest);
    text.insert(END,str(size)+" "+str(mae)+" "+str((mae/size)*1000))
    text.insert(END,"\n\nYour Favourite BOOK : "+input)
    text.insert(END,"\nYou may also like : ")
    text.insert(END,recommend_list)
    
def graph():
       height = [size, mae]
       bars = ('Dataset Size', 'Recommended Books')
       y_pos = np.arange(len(bars))
       plt.bar(y_pos, height)
       plt.xticks(y_pos, bars)
       plt.show()

uploadbutton = Button(main, text="Upload Book Dataset", command=uploadDataset)
uploadbutton.grid(row=0)

name = Label(main)
name.grid(row=1)

filter = Button(main, text="Filter Dataset", command=filterDataset)
filter.grid(row=2)



suggestion = Button(main, text="Get Suggestion", command=suggest)
suggestion.grid(row=5)

graph = Button(main, text="Recommendation Graph", command=graph)
graph.grid(row=6)

text=Text(main,height=30,width=150)
scroll=Scrollbar(text)
text.configure(yscrollcommand=scroll.set)
text.grid(row=8)

main.mainloop()
