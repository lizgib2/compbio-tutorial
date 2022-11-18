#Import the libraries we need to use code from
import pandas as pd
import numpy as np
import requests
from itertools import zip_longest
from matplotlib import pyplot as plt

#create the basics of the codon table 
master = "https://raw.githubusercontent.com/suzannastep/compbio-tutorial/master/S3F/CodonTable.txt"
codon_table = requests.get(master)
codon_table = codon_table.text
codon_table = np.array([[st.split("\t")][0][:4] for st in codon_table.split("\n")][2:-1])
codon_table = pd.DataFrame(codon_table[:,:-4:-1],index=codon_table[:,0],columns=["Amino Acid","Letter Code","3 Letter Code"])
codon_table = codon_table.drop(columns = "3 Letter Code")

def decode_sequence(sequence):
  #figure out how many codons are in the sequence
  how_many_codons = len(sequence)//3
  print("How many codons are there?")
  print(how_many_codons)
  
  #set up lists to keep track of what we find
  amino_acid_list= []
  letter_code_list= []
  
  #For each codon in the sequence...
  for codon_number in range(how_many_codons):
    
    #pick out the codon from the sequence
    codon = sequence[3*codon_number:3*codon_number+3]
    
    #look up which amino acid it is
    amino_acid = codon_table.loc[codon,"Amino Acid"]
    amino_acid_list.append(amino_acid)
    
    #look up which letter code it is
    letter_code = codon_table.loc[codon,"Letter Code"]
    letter_code_list.append(letter_code)
    
    #make the computer tell us what it's doing
    print("Codon:",codon)
    print("Amino Acid:",amino_acid)
    print("Letter Code:",letter_code)
    print()
    
    return amino_acid_list
  
def make_picture(sequence):
  #set up figure
  fig, ax = plt.subplots(figsize=(15,1)) 
  
  #iterate through codons
  how_many_codons = len(sequence)//3
  for codon_number in range(how_many_codons):
    codon = sequence[3*codon_number:3*codon_number+3]
    
    #look up amino acid letter and color
    amino_acid_color = codon_table.loc[codon.upper(),"Color"]
    letter_code = codon_table.loc[codon.upper(),"Letter Code"]
    
    #draw a circle
    circle = plt.Circle((codon_number, 0),#x,y position of center of circle
                        0.5, #radius
                        facecolor=amino_acid_color.lower().replace(" ",""),#color
                        edgecolor="black",#black line around it
                        alpha=0.7)#make the circle a little transparent
    ax.add_patch(circle)#actually draw the circle
    
    #write the letter code on the circle
    ax.text(codon_number,0,#x,y position of the text
            amino_acid,#variable containing the text
            fontsize=20,#size of the text 
            color="black",#color of the text 
            horizontalalignment='center',#center the text horizontally
            verticalalignment='center')#center the text vertically
            
  plt.axis("equal")
  plt.axis("off")
  plt.show()
