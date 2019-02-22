import numpy as np
from scipy.special import gamma
import matplotlib.pyplot as plt

# Define patient arrival rate function


def arr_int(time, num_pats, peak_time):
    # num_pats determines the magnitude of the event (i.e. the number of patients)
    # peak_time controls when the peak arrival time will be
    t = time/60
    out = num_pats / 60 * (t)**(peak_time-1)*np.exp(-t)/(gamma(peak_time))
    return out


def generate_times_opt(rate_function, max_t, delta):
    t = np.arange(delta, max_t, delta)
    avg_rate = (rate_function(t) + rate_function(t + delta)) / 2.0
    avg_prob = 1 - np.exp(-avg_rate * delta)
    rand_throws = np.random.uniform(size=t.shape[0])

    return t[avg_prob >= rand_throws]


def sim_walkthrough():
    numPatients = 30  # Total number of patients on average
    ratio = 1/3  # Ratio of IMMEDIATE patients to DELAYED patients
    peakI = 4.5  # This parameter controls when the peak of arrivals is for IMMEDIATE patients
    peakD = 2.5  # This parameter controls when the peak of arrivals is for DELAYED patients

    # Probabilities of surviving the trip to another hospital
    probI = .4
    probD = .8

    # Compute parameters for functions"
    cI = numPatients / (1+ratio)
    cD = numPatients - cI

    tp = np.linspace(0, 720, num=1000)

    def yI(t): return arr_int(t, cI, peakI)

    def yD(t): return arr_int(t, cD, peakD)
    red_ind = np.random.binomial(1, ratio/(1+ratio))
    ppI_times = generate_times_opt(yI, 720, .1)
    ppD_times = generate_times_opt(yD, 720, .1)
    imm_ind = np.random.binomial(1, ratio/(1+ratio))
    if imm_ind == 1:
        time = np.random.choice(ppI_times)/720 * 120
        col = 'ORANGE'
        survive = np.random.binomial(1, probI)
    else:
        time = np.random.choice(ppD_times)/720 * 120
        col = 'BLUE'
        survive = np.random.binomial(1, probD)
    print('Grab a ' + col + ' index card from the front and write '
          + str(np.round(time, 1)) + ' on the front and ' + str(survive) + ' on the back.')


def plot_arr_int(num_pat, peak):
    # Lets plot a sample of the arrival rate function
    tp = np.linspace(0, 720, num=1000)
    plt.plot(tp, arr_int(tp, num_pat, peak), color='black')
    plt.ylim(0, np.maximum(.5, np.ndarray.max(arr_int(tp, num_pat, peak))))
    plt.xlabel('Elapsed Time (min)')
    plt.ylabel('Intensity of Arrivals (patients/min)')
    plt.show()


def plot_arr_ints(numReps, numPatients, ratio, peakI, peakD):
    # Compute parameters for functions
    cI = numPatients / (1+ratio)
    cD = numPatients - cI

    # Lets plot the arrival rate functions for both classes of patients
    tp = np.linspace(0, 720, num=1000)
    plt.plot(tp, arr_int(tp, cI, peakI), label='IMMEDIATE Patients',
             color='orange')  # First plot for IMMEDIATE patients
    plt.plot(tp, arr_int(tp, cD, peakD), label='DELAYED Patients',
             color='blue')  # First plot for DELAYED patients
    plt.ylim(0, np.maximum(.3, np.ndarray.max(
        np.array([arr_int(tp, cI, peakI), arr_int(tp, cD, peakD)], dtype=float))))
    plt.xlabel('Elapsed Time (min)')
    plt.ylabel('Intensity of Arrivals (patients/min)')
    plt.legend()
    plt.show()


def plot_arrivals(numPatients, ratio, peakI, peakD):
    tp = np.linspace(0, 720, num=1000)
    cI = numPatients / (1+ratio)
    cD = numPatients - cI

    def yI(t): return arr_int(t, cI, peakI)

    def yD(t): return arr_int(t, cD, peakD)
    red_ind = np.random.binomial(1, ratio/(1+ratio))
    ppI_times = generate_times_opt(yI, 720, .1)
    ppD_times = generate_times_opt(yD, 720, .1)

    plt.plot(tp, arr_int(tp, cI, peakI), label='IMMEDIATE Patients',
             color='orange')  # First plot for red patients
    plt.plot(tp, arr_int(tp, cD, peakD), label='DELAYED Patients',
             color='blue')  # First plot for green patients
    plt.plot(ppI_times, arr_int(ppI_times, cI, peakI), color='orange', marker='x', linestyle='none')
    plt.plot(ppD_times, arr_int(ppD_times, cD, peakD), color='blue', marker='x', linestyle='none')
    plt.ylim(0, np.maximum(.3, np.ndarray.max(
        np.array([arr_int(tp, cI, peakI), arr_int(tp, cD, peakD)], dtype=float))))
    plt.xlabel('Elapsed Time (min)')
    plt.ylabel('Intensity of Arrivals (patients/min)')
    plt.legend()
    plt.show()


def simulate(reps, numBeds, numPatients, ratio, peakI, peakD, probI, probD):

    # Compute parameters for functions"
    cI = numPatients / (1+ratio)
    cD = numPatients - cI
    tp = np.linspace(0, 720, num=1000)

    def yI(t): return arr_int(t, cI, peakI)

    def yD(t): return arr_int(t, cD, peakD)
    died_FCFS = np.zeros(reps)
    survived_FCFS = np.zeros(reps)
    final_beds_FCFS = np.zeros(reps)
    died_IO = np.zeros(reps)
    survived_IO = np.zeros(reps)
    final_beds_IO = np.zeros(reps)

    for i in range(reps):
        timesI = generate_times_opt(yI, 720, .1)
        timesD = generate_times_opt(yD, 720, .1)
        total_patients = len(timesI) + len(timesD)
        bedsRemaining_FCFS = numBeds
        bedsRemaining_IO = numBeds
        while len(timesI) + len(timesD) > 0:
            if len(timesI) == 0:
                t = timesD[0]
                timesD = timesD[1:]
                is_I = 0
            elif len(timesD) == 0:
                t = timesI[0]
                timesI = timesI[1:]
                is_I = 1
            else:
                t = np.minimum(timesI[0], timesD[0])
                if t == timesI[0]:
                    timesI = timesI[1:]
                    is_I = 1
                else:
                    timesD = timesD[1:]
                    is_I = 0

            # Handle FCFS
            if bedsRemaining_FCFS > 0:
                bedsRemaining_FCFS += -1
                survived_FCFS[i] += 1
            else:
                if is_I == 1:
                    survived_FCFS[i] += np.random.binomial(1, probI)
                else:
                    survived_FCFS[i] += np.random.binomial(1, probD)

           # Handle Immediate only
            if bedsRemaining_IO > 0 and is_I == 1:
                bedsRemaining_IO += -1
                survived_IO[i] += 1
            else:
                if is_I == 1:
                    survived_IO[i] += np.random.binomial(1, probI)
                else:
                    survived_IO[i] += np.random.binomial(1, probD)

        died_FCFS[i] = total_patients - survived_FCFS[i]
        died_IO[i] = total_patients - survived_IO[i]
        final_beds_FCFS[i] = bedsRemaining_FCFS
        final_beds_IO[i] = bedsRemaining_IO
    output = [died_FCFS, died_IO, survived_FCFS, survived_IO, final_beds_FCFS, final_beds_IO]
    if reps == 1:
        print('FCFS resulted in ' + str(output[0][0]) + ' deaths and ' + str(output[2][0])
              + ' survivers with ' + str(output[4][0]) + ' beds remaining.')
        print('IMMEDIATE ONLY resulted in ' + str(output[1][0]) + ' deaths and ' + str(output[3][0])
              + ' survivers with ' + str(output[5][0]) + ' beds remaining.')
    elif reps > 1:
        print('FCFS resulted in an average of ' + str(np.mean(output[0])) + ' deaths and ' + str(np.mean(output[2]))
              + ' survivers with ' + str(np.mean(output[4])) + ' beds remaining.')
        print('IMMEDIATE ONLY resulted in an average of ' + str(np.mean(output[1])) + ' deaths and ' + str(np.mean(output[3]))
              + ' survivers with ' + str(np.mean(output[5])) + ' beds remaining.')
    else:
        raise Exception('Please input number of repetitions which is greater than 0.')
    return output
