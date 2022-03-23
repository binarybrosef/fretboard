# Fretboard
A GUI-based Python application for visualizing scales across a guitar fretboard.

## Description
Fretboard is a GUI-based application written in Python that displays a wide range of scales, in any key or mode, across a guitar fretboard. Fretboard is extremely useful for learning scales in any/all positions, understanding the correspondence of scales/modes, and identifying desirable patterns within scales. Jazz musicians and others learning to improvise may especially benefit from using Fretboard.

I initially created Fretboard in 2013 as part of learning Python, and to produce something helpful and relevant to my passion and hobby that is playing guitar, or more generally, playing music. Prior versions were command prompt-based, lacked a GUI, and produced symbolic output representative of a guitar fretboard. 

This version provides a GUI built with PyQt 5. 

## How to use Fretboard
Fretboard can be launched by executing fretboard.py, which contains all code for Fretboard.

A scale to be visualized must first be selected. In Fretboard, scales consist of, and are specified by, three parameters: (1) a key, (2) a family to which the scale belongs, and (3) a mode.  

All twelve keys of the standard western 12-tone octave are supported (C,Db,D,Eb,E,F,Gb,G,Ab,A,Bb,B). 

Supported scale families consist of the following: major/minor, melodic minor, harmonic minor, harmonic major, half-whole diminished/octatonic, whole-tone, and pentatonic. While some modes of these families may be unfamiliar to some users, other modes are likely to be familiar. As examples: 

- the major, minor, and dorian modes can be found in the major/minor family (first, sixth, and second modes, respectively); 
- melodic minor and the altered scale can be found in the melodic minor family (first and seventh modes, respectively); 
- harmonic minor can be found in the harmonic minor family (first mode); and
- the pentatonic scale can be found in the pentatonic family (first mode).

The selection of a key, provided family and mode are selected, results in the display of a corresponding scale. Likewise, the selection of a mode, provided key and family are selected, results in the display of a corresponding scale.

The fretboard can be cleared of a displayed scale by setting key to the first item of the key combobox, whose value is empty.

## Future Development
The current version of Fretboard provides a framework that is easily extensible to provide many more desirable and creative features. Among the highest priorities for additional features are:
- color-coding notes according to their interval,
- labeling notes with their letter representation,
- enabling user specification and display of custom scales,
- visualizing arpeggios and other non-scale patterns, 
- displaying, in letter and/or interval form, each note of a given scale,
- support for alternative tunings (e.g., open tunings, drop D, etc.), 
- support for alternative temperaments/tuning systems (e.g., 31-ET), and
- programmatic generation of substitute scales (e.g., scales 1/2/3/etc. note(s) different from a selected scale).
