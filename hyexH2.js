
// Gammelt script med formler
function deflagrationPressureIgnitedJet(deflagrationVolume,jetReleaseRate,totalMassSegment){
    let c0 = 0
    let c1 = 0
    if (jetReleaseRate > 1000){
        c0 = 1
    }
    if (totalMassSegment > 1.5){
        c1 = 1
    }
    return Math.max(Math.min(20, deflagrationVolume / 10), c0 * c1 * 20)
} // Be om forklaring fra Olav på formel

//? VENTILATION

function stirredTankH2ConcAtTimeSteadyLeak(roomVolume,roomTemperature,roomVentilationACH,jetReleaseRate,time){
    let roomConcentration = 0.0 // v/v
    let t = 0 // s
    let leakVolumeRate = jetReleaseRate / molarMass * R * roomTemperature / 101300 // m3/s
    let ventVolumeRate = roomVentilationACH / 3600 * roomVolume
    while (t < time){
        t++
        roomConcentration += (leakVolumeRate - (leakVolumeRate + ventVolumeRate) * roomConcentration) / roomVolume
    }

    return roomConcentration

} 


baseSegmentPressure = 10 // bara
baseDownstreamPressure = 1 // bara
baseSegmentTemperature = 273 // Kelvin
baseSegmentVolume = 1 // m3
baseDischargeCoefficient = 0.85
baseHoleSize = 10 // mm
baseDetectionTime = 3600 // s

roomVolume = 1000 // m3
roomTemperature = 288 // Kelvin
roomVentilationACH = 5 // ACH
time = 720 // s


let compressibilityZ = compressibilityFactor(baseSegmentPressure,baseSegmentTemperature)
//console.log(compressibilityZ) 
let jetReleaseRate = initialJetReleaseRate(baseSegmentPressure,baseDownstreamPressure,baseSegmentTemperature,baseHoleSize,baseDischargeCoefficient)
//console.log(jetReleaseRate)
let massSegment = totalMassSegment(baseSegmentPressure,baseSegmentTemperature,baseSegmentVolume)
//console.log(massSegment)
let ignProbability = ignitionProbability(jetReleaseRate)
//console.log(ignProbability)
let explosionProbabilityDevelopedPlume = explosionProbDeveloped(ignProbability)
//console.log(explosionProbabilityDevelopedPlume)
let explosionProbabilityImmediateIgnition = explosionProbImmediate(ignProbability,explosionProbabilityDevelopedPlume)
//console.log(explosionProbabilityImmediateIgnition)
let defVolume = deflagrationVolume(jetReleaseRate,massSegment,baseDetectionTime)
//console.log(defVolume)
let detVolume = detonationVolume(defVolume)
//console.log(defVolume)
let defPressure = deflagrationPressureIgnitedJet(defVolume,jetReleaseRate,massSegment)
//console.log(defPressure)
let roomConcentration = stirredTankH2ConcAtTimeSteadyLeak(roomVolume,roomTemperature,roomVentilationACH,jetReleaseRate,time)
//console.log(roomConcentration)


// Neste steg:
// Plot av ventilasjon i stirred tank
// Jet dispersion distances
// Jet fire distances and radiation

