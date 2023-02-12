import math


def calculateCompressibility(segT, segP):
    #T in K and P in bar
    leachmanA = [
        0.588846e-1,
        -0.6136111e-1,
        -0.2650473e-2,
        0.2731125e-2,
        0.1802374e-2,
        -0.1150707e-2,
        0.958853e-4,
        -0.110904e-6,
        0.12644E-9
    ]
    
    leachmanB = [
        1.325,
        1.87,
        2.5,
        2.8,
        2.938,
        3.14,
        3.37,
        3.75,
        4.0
    ]
    
    leachmanC = [
        1.0,
        1.0,
        2.0,
        2.0,
        2.42,
        2.63,
        3.0,
        4.0,
        5.0
    ]
    
    exp = 0.0
    C = 1.0
    for i in range(9):
        exp = leachmanA[i]*math.pow((100.0/segT),leachmanB[i])*math.pow((segP/10),leachmanC[i])
        C += exp

    return C
    
def calculateSonicReleaseRate(segP,downstreamP,segT,holeSize,dischargeC,compressibility):
    jetA1 = 0.094 ; jetB1 = 0.0491 ; jetB2 = 0.0039 ; jetB3 = 0.055 ; jetC1 = 0.052 ; T0 = 293
    
    px = (segP-downstreamP)/downstreamP
    rate = 0.0
    
    if px > 0.0 and px < 0.16 : 
        rate = jetA1 * math.sqrt(segP * (segP - downstreamP))
    elif px >= 0.16 and px < 16 :
        rate = (jetB1 * segP + jetB2 * downstreamP) * (1 - jetB3 / (segP - downstreamP) * downstreamP)
    elif px >= 16 :
        rate = jetC1 * (segP-downstreamP)
    
    rate = rate * math.sqrt(T0 / segT / compressibility) * (holeSize * math.sqrt(dischargeC)) ** 2
    return rate

def calculateMassSegment(segP,segT,segV):
    
    R = 8.314
    molarMass = 2.02 #g/mol
    C = calculateCompressibility(segP,segT)

    n = segP * 100000 * segV / C / R / segT

    return n * molarMass / 1000 #kg

def calculateDeflagrationVolume(sonicReleaseRate,massSegment,esdTime):
    halfTime = massSegment / sonicReleaseRate * 0.7 * 1000.0
    #Sjekk at dette er samme som formel for Q9
    return math.min(0.25 / 0.025 * sonicReleaseRate * esdTime / 1000.0 + sonicReleaseRate * halfTime * 0.75 / 1000.0,math.pow(sonicReleaseRate / 1000.0, 1.5))

def calculateDetonationVolume(deflagrationVolume):
    return deflagrationVolume * 1.5

def calculateEarlyIgnitionProbability(sonicReleaseRate):
    return math.min(0.55 * math.pow(sonicReleaseRate / 1000.0,0.87), 0.267 * math.pow(sonicReleaseRate / 1000.0,0.52),1.0) / 3 * 2

def calculateDelayedIgnitionProbability(sonicReleaseRate):
    x = calculateEarlyIgnitionProbability(sonicReleaseRate)
    return x / 2

def calculateTotalIgnitionProbability(sonicReleaseRate):
    x = calculateEarlyIgnitionProbability(sonicReleaseRate)
    return x / 2 * 3

def calculateStirredTankConcentrationAtTimeSteadyLeak(roomVolume,roomTemperature,roomVentilationACH,sonicReleaseRate,time):
    
    roomConcentration = 0.0 # m3
    t = 0 # s
    molarMass = 2.02 # g/mol
    R = 8.314
    
    leakVolumeRate = sonicReleaseRate / molarMass * R * roomTemperature / 101300 # m3/s
    ventVolumeRate = roomVentilationACH / 3600 * roomVolume
    while t < time:
        t += 1
        roomConcentration += (leakVolumeRate - (leakVolumeRate + ventVolumeRate) * roomConcentration) / roomVolume

    return roomConcentration




