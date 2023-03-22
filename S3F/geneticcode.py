#Import the libraries we need to use code from
import pandas as pd
import numpy as np
import requests
from itertools import zip_longest
from matplotlib import pyplot as plt
from matplotlib import table as table
#create the basics of the codon table 
master = "https://raw.githubusercontent.com/suzannastep/compbio-tutorial/master/S3F/CodonTable.txt"
codon_table = requests.get(master)
codon_table = codon_table.text
codon_table = np.array([[st.split("\t")][0][:4] for st in codon_table.split("\n")][2:-1])
codon_table = pd.DataFrame(codon_table[:,:-4:-1],index=codon_table[:,0],columns=["Amino Acid","Letter Code","3 Letter Code"])
codon_table = codon_table.drop(columns = "3 Letter Code")
colors = {
  "Aspartic_acid"   :"white",
  "Glutamic_acid"   :"orange",
  "Glycine"         :"green",
  "Isoleucine"      :"yellow",
  "Methionine"      :"darkorchid",
  "Asparagine"      :"deeppink",
  "Valine"          :"lightblue",
  "Tyrosine"        :"blue",
  "Lysine"          :"lime",
  "Threonine"       :"turquoise",
  "Arginine"        :"tomato",
  "Serine"          :"plum",
  "Glutamine"       :"lightgreen",
  "Histidine"       :"sienna",
  "Proline"         :"red",
  "Leucine"         :"hotpink",
  "Alanine"         :"aqua",
  "Stop"            :"indigo",
  "Cysteine"        :"slateblue",
  "Tryptophan"      :"teal",
  "Phenylalanine"   :"gray",
}
codon_table["Color"] = [colors[amino_acid] for amino_acid in codon_table["Amino Acid"]]

#function to show a colored codon table 
def show_codon_table(codon_table):
  text = [["","T","","C","","A","","G",""],
          ["T","TTT","Phenylalanine (F)","TCT","Serine (S)","TAT","Tyrosine (Y)","TGT","Cysteine (C)"],
          ["T","TTC","Phenylalanine (F)","TCC","Serine (S)","TAC","Tyrosine (Y)","TGC","Cysteine (C)"],
          ["T","TTA","Leucine (L)","TCA","Serine (S)","TAA","Stop (O)","TGA","Stop (O)"],
          ["T","TTG","Leucine (L)","TCG","Serine (S)","TAG","Stop (O)","TGG","Tryptophan (W)"],
          ["C","CTT","Leucine (L)","CCT","Proline (P)","CAT","Histidine (H)","CGT","Arginine (R)"],
          ["C","CTC","Leucine (L)","CCC","Proline (P)","CAC","Histidine (H)","CGC","Arginine (R)"],
          ["C","CTA","Leucine (L)","CCA","Proline (P)","CAA","Glutamine (Q)","CGA","Arginine (R)"],
          ["C","CTG","Leucine (L)","CCG","Proline (P)","CAG","Glutamine (Q)","CGG","Arginine (R)"],
          ["A","ATT","Isoleucine (I)","ACT","Threonine (T)","AAT","Asparagine (N)","AGT","Serine (S)"],
          ["A","ATC","Isoleucine (I)","ACC","Threonine (T)","AAC","Asparagine (N)","AGC","Serine (S)"],
          ["A","ATA","Isoleucine (I)","ACA","Threonine (T)","AAA","Lysine (K)","AGA","Arginine (R)"],
          ["A","ATG","Methionine (M)","ACG","Threonine (T)","AAG","Lysine (K)","AGG","Arginine (R)"],
          ["G","GTT","Valine (V)","GCT","Alanine (A)","GAT","Aspartic_acid (D)","GGT","Glycine (A)"],
          ["G","GTC","Valine (V)","GCC","Alanine (A)","GAC","Aspartic_acid (D)","GGC","Glycine (A)"],
          ["G","GTA","Valine (V)","GCA","Alanine (A)","GAA","Glutamic_acid (E)","GGA","Glycine (A)"],
          ["G","GTG","Valine (V)","GCG","Alanine (A)","GAG","Glutamic_acid (E)","GGG","Glycine (A)"]]
  colors = [["white"]*9]
  for row in text[1:]:
    rowcolors = ["white"]
    for index in row[1::2]:
      color = codon_table.loc[index,"Color"]
      rowcolors.append(color)
      rowcolors.append(color)
    colors.append(rowcolors)
  fig, ax = plt.subplots()
  # hide axes
  fig.patch.set_visible(False)
  t = table.Table(ax,loc='center')
  for rownum,row in enumerate(text):
    for colnum,item in enumerate(row):
      if colnum > 0 and colnum%2 == 0:
        width = 0.4
      else:
        width = 0.12
      c = t.add_cell(rownum,
                 colnum,
                 text=text[rownum][colnum],
                 facecolor = colors[rownum][colnum],
                 width=width,
                 height=0.12,
                 loc="center")
      c.set_alpha(0.7)
  t.auto_set_font_size(False)
  t.set_fontsize(15)
  ax.add_table(t)
  plt.axis('off')
  plt.axis('equal')
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
