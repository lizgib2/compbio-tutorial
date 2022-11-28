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

#function to show a colored codon table 
def show_codon_table(codon_table):
  text = [["","T","","C","","A","","G",""],
          ["T","TTT","Phenylalanine","TCT","Serine","TAT","Tyrosine","TGT","Cysteine"],
          ["T","TTC","Phenylalanine","TCC","Serine","TAC","Tyrosine","TGC","Cysteine"],
          ["T","TTA","Leucine","TCA","Serine","TAA","Stop","TGA","Stop"],
          ["T","TTG","Leucine","TCG","Serine","TAG","Stop","TGG","Tryptophan"],
          ["C","CTT","Leucine","CCT","Proline","CAT","Histidine","CGT","Arginine"],
          ["C","CTC","Leucine","CCC","Proline","CAC","Histidine","CGC","Arginine"],
          ["C","CTA","Leucine","CCA","Proline","CAA","Glutamine","CGA","Arginine"],
          ["C","CTG","Leucine","CCG","Proline","CAG","Glutamine","CGG","Arginine"],
          ["A","ATT","Isoleucine","ACT","Threonine","AAT","Asparagine","AGT","Serine"],
          ["A","ATC","Isoleucine","ACC","Threonine","AAC","Asparagine","AGC","Serine"],
          ["A","ATA","Isoleucine","ACA","Threonine","AAA","Lysine","AGA","Arginine"],
          ["A","ATG","Methionine","ACG","Threonine","AAG","Lysine","AGG","Arginine"],
          ["G","GTT","Valine","GCT","Alanine","GAT","Aspartic_acid","GGT","Alanine"],
          ["G","GTC","Valine","GCC","Alanine","GAC","Aspartic_acid","GGC","Alanine"],
          ["G","GTA","Valine","GCA","Alanine","GAA","Glutamic_acid","GGA","Alanine"],
          ["G","GTG","Valine","GCG","Alanine","GAG","Glutamic_acid","GGG","Alanine"]]
  colors = [["white"]*9]
  for row in text:
    rowcolors = ["white"]
    for index in row[1::2]:
      color = codon_table["Color"][index]
      rowcolors.append(color)
    colors.append(rowcolors)
  plt.table(cellText=text,cellColours=colors)
  plt.ylabel("First Base")
  plt.xlabel("Second Base")
  plt.show()

def decode_sequence(sequence):
  #figure out how many codons are in the sequence
  how_many_codons = len(sequence)//3
#   print("How many codons are there?")
#   print(how_many_codons)
  
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
            letter_code,#variable containing the text
            fontsize=20,#size of the text 
            color="black",#color of the text 
            horizontalalignment='center',#center the text horizontally
            verticalalignment='center')#center the text vertically
            
  plt.axis("equal")
  plt.axis("off")
  plt.show()
