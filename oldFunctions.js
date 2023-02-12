
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
