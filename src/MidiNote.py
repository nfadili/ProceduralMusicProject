import midi
from constants import *

# Add self to param list if you end up making a class/API
# Returns tuple of (onEvent, offEvent)
def newNote(pitch, duration, vel):
    noteVal = parsePitch(pitch)
    ticks = parseDuration(duration)
    on = midi.NoteOnEvent(tick=ticks[0], velocity=vel, pitch=noteVal)
    off = midi.NoteOffEvent(tick=ticks[1], pitch=noteVal)
    return (on, off)

def newRest(duration):
    ticks = parseDuration(duration)
    on = midi.NoteOnEvent(tick=ticks[1])
    off = midi.NoteOffEvent(tick=ticks[1])
    return (on, off)

# Format must follow -> LETTER(ACCIDENTAL)_OCTAVE
# Returns MIDI value (int) associated with the note or -1 if a rest
def parsePitch(pitch):
    if pitch == 'R': return -1
    note, octave = pitch.split('_')
    if int(octave) > MAX_OCTAVE or int(octave) < MIN_OCTAVE: raise PitchError('Octave out of range: [0, 8].')
    if len(note) is 2: note, acc = note
    else: acc = 0
    case = {
         0 : 0,
        '#': 1,
        'C': 0,
        'D': 2,
        'E': 4,
        'F': 5,
        'G': 7,
        'A': 9,
        'B': 11
    }
    return ((int(octave) * NOTES_IN_OCTAVE) + case.get(note) + case.get(acc))

# Takes in a standard note duration with resolution 16:
#   whole = 1
#   half = 2
#   quarter = 4
#   eighth = 8
#   sixteenth = 16
#   thirty-second = 32
#   sixty-fourth = 64
# Returns tuple (startTick, endTick) for parsing in the newNote function
def parseDuration(duration):
    case= {
        WHOLE : MIDI_WHOLE,
        HALF : MIDI_HALF,
        QUARTER : MIDI_QUARTER,
        EIGHTH : MIDI_EIGHTH,
        SIXTEENTH: MIDI_SIXTEENTH,
        THIRTY_SECOND: MIDI_THIRTY_SECOND,
        SIXTY_FOURTH: MIDI_SIXTY_FOURTH
    }
    startTick = 0
    endTick = case.get(duration)
    return (startTick, endTick)

################################################################################
# Exception definitions
################################################################################
class MidiNoteError(Exception):
    # Base class for MidiNote errors.
    pass

class PitchError(MidiNoteError):
    def __init__(self, msg):
        self.msg = msg
