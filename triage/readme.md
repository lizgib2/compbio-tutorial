# Triage Workshop Outline

## Learning Objectives:
By the end of this class, students will be able to: 
- Describe how statistics can be used model real world events 
- Describe how computers can be used to randomly simulate events
- Create and interpret graphics of their analysis 
- Explain why statistical and computational tools are needed to model problems in medicine

## Necessary Items:

School provides:

  - Computer access for each student with Google Colab unblocked

Workshop provides:

  - The triage slides: these can be found in the “Slides” sub-directory within the “triage” folder. You may want to edit these a bit (we’ll talk more about this later).
  - The Jupyter notebook entitled “triage_exercise.ipynb” from the “triage” folder.
  - The file entitled “triage_funcs.py” from the “triage” directory. Note that you will never need to open this file but it must be in the same folder as “triage_exercise.ipynb” in order for the activity to function properly.
  - A set of index cars with at least two colors, preferably blue and orange OR yellow and red.

## Directions:
1. Open the triage slides. (Make sure you’ve looked through the slides several times before actually giving the workshop).
      - Slides 1-2: discuss what a mass casualty event is, and explain that we will be using computers to try and improve the efficacy with which casualties are given help.
      - Slides 3-5: explain what triage is, and then explain that START is one of the most common methods of triage. I would only briefly show slide 5. We’ve changed the Yellow/Red colors to Blue/Orange since a member of our team suffers from color-blindness. Feel free to change them back.
      - Slides 6-7: initiate the emergency. These slides are very Chicago specific so feel free to change them to something more local. If you have trouble altering the slides because you’re unfamiliar with LaTeX/Beamer, please feel free to reach out. Discuss how you will be creating a policy for the local trauma unit since there has just been a local mass-casualty event.
      - Slide 8: Discuss how an admission policy will need to be designed. Most of the relevant information is on the slide.
      - Slide 9: Before advancing past the first line of text “Only admit…” it is a great idea to allow students to “think, pair, share”. I.e. allow them to discuss possible policies amongst themselves and then contribute their own ideas. Once you’ve done this for a few minutes proceed to discuss the listed policies. I you feel confident enough to discuss it, talk about how an active area of research is coming up with optimal admission policies where your admission decision is dependent on the time a patient arrives, the number of available beds, and their triage status.
      - Slide 10: Begin discussing how we will build a model to help us decide which policy is best. Again ask the class what kind of information they would like to have in order to help them make a decision and have them think, pair, share before moving on and discussing each of the individual bullet points.
      - Slide 11: This slide is optional and I typically reserve it for the end. This is basically an example of a paper doing research into this exact problem.
1. Open the “triage_exercise” notebook with your class. 
1. You want to have the following general road map in your heard throughout this exercise. We are going to slowly build up a model for triage by:
1. Defining how patients arrive.
1. Defining which patients survive.
1. Putting it all together with a walkthrough (using the cards).
1. Running the model many times in the notebook.
1. First allow students to put their name into the notebook and discuss how the first box of code needs to be run in order to import the necessary packages.
1. Discuss how you will now be developing a model for how patients arrive. The first block of code in this section will create a black curve. This represents how the intensity of patient arrivals changes over time. Try an explain what this means to the students and have them try out many different values of num_pat and peak to see how it changes the shape of the curve. (HSS-ID.A.1-2, HSS-MD.A.1)
1. After this is complete start discussing how the IMMEDIATE and DELAYED patients may have different arrival patterns. An interesting thing to mention is that IMMEDIATE patients typically arrive a little bit later than DELAYED patients. This is due to several reasons (e.g. IMMEDIATE patients are more likely to be trapped under rubble, sometimes DELAYED patients can be transported to the hospital without an ambulance and don’t need to wait for one to become available, etc…).
1. Have students play with the four parameters in this code block and see how it changes the two curves. (HSS-ID.A.2)
1. The code block after this will generate samples of arrival from these intensity curves. This may be a good time to emphasize why we may want to run simulations. Just because we know the intensities of arrivals doesn’t mean we know exactly when each patient will arrive. (HSS-MD.B.7)
1. We will now discuss how we decide whether a patient survives or not. You should emphasize why we need the computer to generate random numbers for us and that humans are really bad at being truly “random”. To demonstrate open the link to the mindreader app included in the notebook. Once open have a one or two students try and beat the mind reader. The basic idea is that the students will try and alternate pressing left and right without forming any sort of pattern which the computer will be able to guess. This is really hard for humans to do. I recommend that you play with this website a bit before you actually open it in the workshop as the interface can be a bit confusing the first time you look at it. Also I recommend selecting the hardest difficulty level (a combination of the fastest and smartest algorithms). (HSS-MD.B.6, HSS-MD.A.1)
1. The next code block shows how we can generate a sequence of numbers representing which patients survive or not. Have the students play with the prob parameter and see how it changes the output. Also emphasize that even if they don’t change prob the output will change every time. Ask why this is and then explain the concept of random numbers.
1. We will now put this all together in a simulation. Lay out the index cards with some writing implements. Have each student (and each instructor except yourself) to run the first code block. It give them directions for which color to choose and tell them to write number on the front, and a 0 or 1 on the back. We will now do a walkthrough of a simulation. Each person represents a patient, with the color of their index card representing their injury severity, the number of the front representing the time they arrive at the hospital, and the 0 or 1 on the back representing whether they survive if they turned away.
1. The walkthrough:
    - First set aside some number of desks or chairs representing the hospital beds. I typically try to aim for roughly 1/3 the number of beds vs the number of people with cards.
    - Have all the people with cards line up in order. Namely have them line up so that people with lower numbers are at the front of the line and people with larger numbers are at the back of the line.
    - Now walk through the simulation doing FCFS first. For example, for FCFS, assign people in line to beds until there are not more free beds and assign everyone else to the other side of the room. Then have the everyone with a 1 raise their hands and count how many survivors there are (including those in beds).
    - Repeat this process for ORANGE ONLY. Walking through the line only assigning the ORANGES to beds until there are no more free beds. Repeat the process of counting survivors and compare with the FCFS policy. Sometime there will be free beds when using ORANGE ONLY. If this is the case make sure to point it out.
1. Now explain that this was just one simulation and in order to truly compare the policies we would want to walk through this simulation many, many times. This can be accomplished by running simulations on the computer. The second code black will do just that. Allow the students to play with the parameters in this code block but beware if they set a number too large of num_reps then it may take a long (OR REALLY LONG) time to run.
1. Help the students analyze the data output by the simulation
    - Discuss why we might care about the percentage of patients who died in each simulation instead of just the number who did (HSS-CP.A.3)
    - Show the students how to do arithmetic using Pandas and create a new column for the percentage of patients who survive under FCFS in each simulation
    - Use “think-pair-share” to have students create a similar column for the IO policy
    - Show the students the box plot of the number of patients who survived under each policy. Ask for a few comments about what they observe in the box plot. Point out that the median in FCFS is higher than the median for IO, but that they have about the same spread. (HSS-ID.A.1-3)
    - Ask students to “think-pair-share” again to create a box plot of the percentage  of patients who survived. Once they have finished, ask students to again comment on their observations. Emphasize that this second box plot is different from the first because this one accounts for the percentages across runs, and accounts for the fact that some patients died as well.  (HSS-ID.A.1-3)
    - Show the students how to compute the mean over different runs of the variables in the table. Emphasize how long this would take to compute by hand. Have students “think-pair-share” to compute the means of the remaining columns in the data and put the results in a table. (HSS-MD.A.2,4)
1. Discuss which policy works better. Discuss which statistic the students think is the most important in deciding which policy is best, and why. (HSS-MD.B.7)
1. Discuss what the students have learned about the role of running simulations v. looking at data in the real world.
1. Challenge: instruct the students to see if they can find different combinations of parameters where each policy is better. (HSS-MD.B.7)

## Associated Common Core High School Math Standards

- HSS-ID.A. Summarize, represent, and interpret data on a single count or measurement variable 
    - HSS-ID.A.1  Represent data with plots on the real number line (dot plots, histograms, and box plots). 
    - HSS-ID.A.2  Use statistics appropriate to the shape of the data distribution to compare center (median, mean) and spread (interquartile range, standard deviation) of two or more different data sets. 
    - HSS-ID.A.3  Interpret differences in shape, center, and spread in the context of the data sets, accounting for possible effects of extreme data points (outliers). 
- HSS-CP.A. Understand independence and conditional probability and use them to interpret data 
    - HSS-CP.A.3  Understand the conditional probability of A given B as P(A and B)/P(B), and interpret independence of A and B as saying that the conditional probability of A given B is the same as the probability of A, and the conditional probability of B given A is the same as the probability of B. 
- HSS-MD.A. Calculate expected values and use them to solve problems 
    - HSS-MD.A.1 (+) Define a random variable for a quantity of interest by assigning a numerical value to each event in a sample space; graph the corresponding probability distribution using the same graphical displays as for data distributions. 
    - HSS-MD.A.2 (+) Calculate the expected value of a random variable; interpret it as the mean of the probability distribution. 
    - HSS-MD.A.4 (+) Develop a probability distribution for a random variable defined for a sample space in which probabilities are assigned empirically; find the expected value. For example, find a current data distribution on the number of TV sets per household in the United States, and calculate the expected number of sets per household. How many TV sets would you expect to find in 100 randomly selected households? 
- HSS-MD.B. Use probability to evaluate outcomes of decisions
    - HSS-MD.B.6 (+) Use probabilities to make fair decisions (e.g., drawing by lots, using a random number generator). 
    - HSS-MD.B.7 (+) Analyze decisions and strategies using probability concepts (e.g., product testing, medical testing, pulling a hockey goalie at the end of a game). 
