import numpy as np
from scipy.special import gamma
# Import poisson process package
from tick.base import TimeFunction
from tick.hawkes import SimuInhomogeneousPoisson

# Define patient arrival rate function


def arr_int(time, num_pats, peak_time):
    # num_pats determines the magnitude of the event (i.e. the number of patients)
    # peak_time controls when the peak arrival time will be
    t = time/60
    out = num_pats / 60 * (t)**(peak_time-1)*np.exp(-t)/(gamma(peak_time))
    return out


def simulate(reps, numBeds, numPatients, ratio, peakI, peakD, probI, probD):

    # Compute parameters for functions"
    cI = numPatients / (1+ratio)
    cD = numPatients - cI
    tp = np.linspace(0, 720, num=1000)
    yI = arr_int(tp, cI, peakI)
    yD = arr_int(tp, cD, peakD)
    tfI = TimeFunction((tp, yI))
    tfD = TimeFunction((tp, yD))
    died_FCFS = np.zeros(reps)
    survived_FCFS = np.zeros(reps)
    final_beds_FCFS = np.zeros(reps)
    died_IO = np.zeros(reps)
    survived_IO = np.zeros(reps)
    final_beds_IO = np.zeros(reps)

    for i in range(reps):
        ppI = SimuInhomogeneousPoisson([tfI], end_time=720, verbose=False)
        ppD = SimuInhomogeneousPoisson([tfD], end_time=720, verbose=False)
        ppI.simulate()
        ppD.simulate()
        timesI = ppI.timestamps[0]
        timesD = ppD.timestamps[0]
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
    return [died_FCFS, died_IO, survived_FCFS, survived_IO, final_beds_FCFS, final_beds_IO]
