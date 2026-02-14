#!/usr/bin/env python3
"""
Targeted fixes for Gospel of Egyptians after Azure DI extraction.
Reads the cleaned file and applies precise, enumerated fixes.
"""

import re
from pathlib import Path

FILE = Path(__file__).parent.parent / "output" / "cleaned" / "tractates" / "III_2_gospel_egyptians.md"


def apply_fixes(text: str) -> str:
    # ===== PHASE 1: Remove verse/line separator marks =====
    # The ' (right single quote) is used throughout as a verse line separator.
    # Pattern: space + ' + space  →  space
    text = text.replace(" ' ", " ")
    # Also at start of line or after newline
    text = text.replace("\n' ", "\n")
    
    # Fix stray I (capital i) that OCR produced instead of ' at end of sentences
    # These appear as ". I\n" or ". I " at paragraph boundaries
    text = text.replace("Father. I\n", "Father.\n")
    text = text.replace("[appeared]. I\n", "[appeared].\n")
    text = text.replace("Amen. I\n", "Amen.\n")
    text = text.replace(" I\n\n1 the third", "\n\nThe third")  # broken paragraph
    text = text.replace("lives, I [and", "lives, [and")
    text = text.replace("became, I (and)", "became, (and)")
    text = text.replace("heaven, I the incorruptible", "heaven, the incorruptible")
    text = text.replace("reveal I to", "reveal to")
    text = text.replace("Amen. 1\n", "Amen.\n")  # digit 1 as artifact
    
    # Fix stray | (pipe) used as verse separator
    text = text.replace(" | ", " ")
    
    # ===== PHASE 2: Remove missed hyphen breaks =====
    text = text.replace("de- filed", "defiled")
    
    # ===== PHASE 3: Fix OCR number artifacts =====
    # 1º and 2º are OCR misreads of 10 and 20 (superscript º)
    # But these are line reference numbers - remove them entirely
    text = text.replace(" 1º ", " ")
    text = text.replace(" 2º ", " ")
    
    # ===== PHASE 4: Remove codex page numbers embedded in text =====
    # These are Coptic manuscript page numbers (III pages 40-69, IV pages 50-81)
    # They appear mid-text like "the light [of the 41 incorruptions"
    # We need to be very targeted - only remove when clearly a page transition
    
    page_number_fixes = [
        # Codex III page numbers (40-69)
        ("the light [of the 41 incorruptions", "the light [of the incorruptions"),
        ("forth, 42 the three ogdoads", "forth, the three ogdoads"),
        ("the vir- tue [of the 43 Mother", "the virtue [of the Mother"),  # already fixed by hyphen
        ("the virtue [of the 43 Mother", "the virtue [of the Mother"),
        ("he whose 44 name [is]", "he whose name [is]"),
        ("the male [virgin] 20 [Youel].", "the male virgin [Youel]."),
        ("50 and the male [virgin]", "and the male [virgin]"),
        ("there may appear 51 [. .. ]", "there may appear [. .. ]"),
        ("became complete. 52 When", "became complete. When"),
        ("Abrasax of 53 [the great light]", "Abrasax of [the great light]"),
        ("Esephech, 54 the holder", "Esephech, the holder"),
        ("glories 55 and incorruptions", "glories and incorruptions"),
        ("the child, 56 and the great", "the child, and the great"),
        ("a cloud 57 [whose name is]", "a cloud [whose name is]"),
        ("Autogenes, 58 \"There shall", "Autogenes, \"There shall"),
        ("since he] 59 trusted", "since he] trusted"),
        ("the seed 60 of Adam", "the seed of Adam"),
        ("through three 61 worlds", "through three worlds"),
        ("the male 62 virgin Barbelon", "the male virgin Barbelon"),
        ("Autogenes 63 and the whole", "Autogenes and the whole"),
        ("incorruptible, 64 Logos-begotten", "incorruptible, Logos-begotten"),
        ("the great 65 Abrasax", "the great Abrasax"),
        ("from now on 66 through", "from now on through"),
        ("tongue? Now 67 that I have", "tongue? Now that I have"),
        ("really truly 68 for ever.", "really truly for ever."),
        ("the eternal light, 69 and his", "the eternal light, and his"),
        
        # Codex IV page numbers
        ("the [greatness] IV 55 20 that", "the [greatness] that"),
        ("IV 55, 5-7 adds:", "(IV 55, 5-7 adds:"),  # keep as reference note
        ("IV 61 8", ""),  # standalone reference
        ("III 49 10 he through", "he through"),
        ("III 49 that [place]", "that [place]"),
        ("(or, IV 68, 3: [in] the four aeons)", "(or, IV 68,3: [in] the four aeons)"),
        
        # The standalone codex reference at the top is fine - keep it
    ]
    
    for old, new in page_number_fixes:
        text = text.replace(old, new)
    
    # ===== PHASE 5: Remove remaining line reference numbers =====
    # These are line numbers in the Coptic manuscript (1, 5, 10, 13, 15, 18, 20, 21, 25, 30)
    # They appear as ", 5 " or "Father, 15 the" etc.
    # Very targeted: remove number when between comma/period and lowercase word
    
    line_ref_fixes = [
        # Each is a specific instance found in the text
        ("[he who came] 18 forth", "[he who came] forth"),
        ("Father, 5 the aeon", "Father, the aeon"),
        ("the Son, 10 from the living", "the Son, from the living"),
        ("[forth, 15 the aeon of]", "[forth, the aeon of]"),
        ("He was 20 [ ... ]", "He was [ ... ]"),
        ("the Son. 5", "the Son."),
        ("Father.\nThe second", "Father.\n\nThe second"),  # ensure paragraph break
        ("mind, 10 and the foreknowledge", "mind, and the foreknowledge"),
        ("the heaven, karb[ ... ]", "the heaven, karb[ ... ]"),
        ("she came forth; [she] 20 agreed", "she came forth; [she] agreed"),
        ("These are the three 3 [powers]", "These are the three [powers]"),
        ("came forth, 10 the aeon", "came forth, the aeon"),
        ("name 2º [is inscribed]", "name [is inscribed]"),
        ("And [in this] 10 way", "And [in this] way"),
        ("living silence 15 came forth", "living silence came forth"),
        ("races]) 20 filled", "races]) filled"),
        ("Ainon - gave [praise to]", "Ainon — gave [praise to]"),
        ("anointed - he [whose]", "anointed — he [whose]"),
        ("[come forth], 25 power", "[come forth], power"),  # already fixed
        ("[come forth],", "[come forth],"),
        ("Spirit.\nThen there", "Spirit.\n\nThen there"),
        ("[glories 15 . . . ]", "[glories . . . ]"),
        ("virgin 20 [Youel]", "virgin [Youel]"),
        ("[Son], 25 the [five]", "[Son], the [five]"),
        ("incorruptible 57 ones", "incorruptible ones"),
        ("[ .. . ]. 13 This one", "[ .. . ]. This one"),
        ("unrevealable, 15 hidden", "unrevealable, hidden"),
        ("[ ... ] 21 him", "[ ... ] him"),
        ("[ ... ] 25 myriads", "[ ... ] myriads"),
        ("[them, 58 glories]", "[them, glories]"),
        ("the Son, and 5 [the]", "the Son, and [the]"),
        ("[of 15 .. . really]", "[of .. . really]"),
        ("[ ... ] 18 eternal", "[ ... ] eternal"),
        (". 21 and the", ". And the"),
        ("silence 25 of] the Spirit", "silence of] the Spirit"),
        ("established 3 thrones", "established thrones"),
        # Note: some "5" and "10" etc are already removed by the ' cleanup
        ("giving 10 praise", "giving praise"),
        ("[and 15 all the]", "[and all the]"),
        ("Telmachael 20 [Eli Eli]", "Telmachael [Eli Eli]"),
        ("of glory, 25 the [child]", "of glory, the [child]"),
        ("There 60 the great self-begotten", "There the great self-begotten"),
        ("[who] 10 came forth", "[who] came forth"),
        ("[. .. 15 invisible", "[. .. invisible"),
        ("established] 20 the four", "established] the four"),
        ("Spirit, [the silence] 25 of the", "Spirit, [the silence] of the"),
        ("rests. [ ... ] through [ ... ]. 30", "rests. [ ... ] through [ ... ]."),
        ("Mirothoe. 5 And she", "Mirothoe. And she"),
        ("came forth. He 15 came down", "came forth. He came down"),
        ("each other. 20 A Logos", "each other. A Logos"),
        ("virginal 25 Spirit", "virginal Spirit"),
        ("before, 10 and the ethereal", "before, and the ethereal"),
        ("the Father 15 of the silent", "the Father of the silent"),
        ("man Adamas, 20 the incorruptible", "man Adamas, the incorruptible"),  # wait, this is actual text
        # Let me be more precise:
        ("Autogenes, and 20 the incorruptible man Adamas", "Autogenes, and the incorruptible man Adamas"),
        ("in order that, 25 through them", "in order that, through them"),
        ("the world 5 which is the image", "the world which is the image"),
        ("race, so 10 that", "race, so that"),
        ("And thus 15 there came forth", "And thus there came forth"),
        ("Seth, the son 20 of the incorruptible", "Seth, the son of the incorruptible"),  # careful - "20" between "son" and "of"
        ("Eleleth, 20 and the great", "Eleleth, and the great"),
        ("light 10 Harmozel", "light Harmozel"),  # after Harmozel fix
        ("Eleleth. This 15 is the first", "Eleleth. This is the first"),
        ("came forth: 20 the first one", "came forth: the first one"),
        ("Davithe, 25 and the great Abrasax", "Davithe, and the great Abrasax"),  # wait, keep checking
        ("Gamaliel; the Love", "Gamaliel; the Love"),
        ("Abrasax. 1º Thus", "Abrasax. Thus"),  # already handled by 1º removal
        ("the pleroma 15", "the pleroma"),
        ("\n\nof the four lights", " of the four lights"),  # rejoin split paragraph
        ("Doxomedon-aeon, 20 and the thrones", "Doxomedon-aeon, and the thrones"),
        ("virgin 25 Youel", "virgin Youel"),
        ("the seed 10 of the Father", "the seed of the Father"),
        ("children came forth 15 from above", "children came forth from above"),
        ("came forth, the 20 whole greatness", "came forth, the whole greatness"),
        ("in glory, myriads", "in glory, myriads"),  # "1" already removed
        ("around them, 25 powers", "around them, powers"),  # wait, check
        ("around them, myriads without number, 25 powers", "around them, myriads without number, powers"),
        ("the four 5 lights", "the four lights"),
        ("the Father, and 10 the Mother", "the Father, and the Mother"),
        ("the leaders 15 were given", "the leaders were given"),
        ("uncallable, 20 unnameable", "uncallable, unnameable"),
        ("his seed. I\n", "his seed.\n"),  # stray I
        ("from that place 5 the great power", "from that place the great power"),
        ("the fruit 10 from Gomorrah", "the fruit from Gomorrah"),
        ("rejoiced about 15 the gift", "rejoiced about the gift"),
        ("placed it with 20 him", "placed it with him"),
        ("spoke: \"Let someone 25 reign", "spoke: \"Let someone reign"),
        ("blood. And", "blood. And"),  # "5" before "blood" should be removed
        ("] 5 blood. And", "] blood. And"),
        ("come forth 1º [in order", "come forth [in order"),  # 1º already handled
        ("in the cloud [above.", "in the cloud [above."),
        ("the earth. 20 [They", "the earth. [They"),
        ("aeon, worlds 25 [ .... \"", "aeon, worlds [ .... \""),
        ("angels], \"Go and [let each] 5 of you", "angels], \"Go and [let each] of you"),
        ("generations 10 of men", "generations of men"),
        ("Sabaoth. The sixth [is Cain, 15", "Sabaoth. The sixth [is Cain,"),  # careful
        ("Sabaoth. The sixth [is Cain,\n", "Sabaoth. The sixth [is Cain,\n"),  # already correct
        ("The] 20 eleventh", "The] eleventh"),
        ("his [angels], 25 \"I, I am", "his [angels], \"I, I am"),
        ("of the Man.\" \" Because", "of the Man.\" Because"),  # double quote
        ("the image 5 above", "the image above"),
        ("Because of this 1º Metanoia", "Because of this Metanoia"),  # 1º already handled
        ("great, 15 mighty men", "great, mighty men"),
        ("above down 20 to the world", "above down to the world"),
        ("this aeon and (the>", "this aeon and <the>"),  # fix bracket
        ("defiled (seed) of the demon-begetting god 25 which", "defiled (seed) of the demon-begetting god which"),
        ("Seth came and brought his 10 seed", "Seth came and brought his seed"),
        ("Gomorrah. 15 But others", "Gomorrah. But others"),
        ("came forth through 30 Edokla", "came forth through Edokla"),  # "30" is line ref  
        ("their emanation. 25 This is", "their emanation. This is"),
        ("this race. A conflagration", "this race. A conflagration"),
        ("the life 10 of the race", "the life of the race"),
        ("will come, 15 a falsehood", "will come, a falsehood"),
        ("immovable race, 20 and the persecutions", "immovable race, and the persecutions"),
        ("uncallable, 25 virginal", "uncallable, virginal"),
        ("really truly 5 lives", "really truly lives"),
        ("in him, and 10 the powers", "in him, and the powers"),
        ("ethereal 15 angels", "ethereal angels"),
        ("Seth, from the time and 20 the moment", "Seth, from the time and the moment"),
        ("condemned to death.\n", "condemned to death.\n"),  # fine
        ("Seth was 25 sent", "Seth was sent"),
        ("He passed through 5 the three", "He passed through the three"),
        ("the world, and 10 the baptism", "the world, and the baptism"),
        ("Spirit, through 15 invisible", "Spirit, through invisible"),
        ("the saints, and 20 the ineffable", "the saints, and the ineffable"),
        ("surpasses 25 the heaven", "surpasses the heaven"),
        ("aeons, and 5 established", "aeons, and established"),
        ("truth, Micheus and Michar", "truth, Micheus and Michar"),  # fine
        ("preside over 15 the spring", "preside over the spring"),
        ("the waters, 20 Micheus", "the waters, Micheus"),
        ("the great Seth, the 25 ministers", "the great Seth, the ministers"),
        ("eternal 5 life", "eternal life"),
        ("Machar Seth, and 10 the great invisible", "Machar Seth, and the great invisible"),
        ("truth, and (he> who is with 15 him", "truth, and <he> who is with him"),
        ("\n\n1 the third, Davithe", "\n\nThe third, Davithe"),
        ("the 20 sons of the great Seth", "the sons of the great Seth"),
        ("baptize with 25 the holy", "baptize with the holy"),
        ("the five seals in the spring-baptism, these will 5 know", "the five seals in the spring-baptism, these will know"),
        ("Really truly, 10 O Yesseus", "Really truly, O Yesseus"),
        ("permanent, 20 really truly", "permanent, really truly"),  # check
        ("eternally\n\neternal, 20 really truly", "eternally eternal, really truly"),  # rejoin split paragraph
        ("Really truly, aee eee iiii", "Really truly, aee eee iiii"),  # fine
        ("me. 25 I see thee", "me. I see thee"),
        ("at 5 that place", "at that place"),
        ("in 10 my bosom", "in my bosom"),
        ("aeon, aeon, O God of silence! I honor", "aeon, aeon, O God of silence! I honor"),  # "I" here is the pronoun, keep it
        ("O 15 aeon", "O aeon"),
        ("in whom thou wilt purify me into thy life", "in whom thou wilt purify me into thy life"),  # fine
        ("raising up the man 20 in whom", "raising up the man in whom"),
        ("all archons, 25 in order", "all archons, in order"),
        ("nor is it 5 possible", "nor is it possible"),
        ("heard it. 10", "heard it."),
        ("and thirty years", "and thirty years"),  # fine, already fixed
        ("the 15 times and the eras", "the times and the eras"),
        ("love, it may 20 come forth", "love, it may come forth"),
        ("eternal 25 Spirit", "eternal Spirit"),
        ("Amen. I\n\nThe Gospel", "Amen.\n\nThe Gospel"),
        ("5 Amen. I", "Amen."),  # near end
        ("secret - book", "secret book"),  # stray hyphen
        ("him 10 who has written it", "him who has written it"),
        ("God, 15 Savior", "God, Savior"),
        ("Spirit. Amen. 1\n", "Spirit. Amen.\n"),  # trailing 1
        ("Spirit. 20 Amen.", "Spirit.\nAmen."),
        
        # Fix (he> to <he> and (the> to <the>
        ("(he>", "<he>"),
        ("(the>", "<the>"),
        ("(and>", "<and>"),
        
        # Fix em-dashes
        (" - he ", " — he "),
        (" - gave ", " — gave "),
    ]
    
    for old, new in line_ref_fixes:
        if old in text:
            text = text.replace(old, new)
    
    # ===== PHASE 6: Clean up formatting =====
    # Remove double spaces
    text = re.sub(r'  +', ' ', text)
    
    # Remove trailing spaces on lines
    text = re.sub(r' +\n', '\n', text)
    
    # Fix triple+ newlines to double
    text = re.sub(r'\n{3,}', '\n\n', text)
    
    # Ensure consistent line endings
    text = text.replace('\r\n', '\n')
    
    return text


def main():
    print(f"Reading {FILE}")
    text = FILE.read_text(encoding="utf-8")
    print(f"Input: {len(text)} chars")
    
    text = apply_fixes(text)
    
    print(f"Output: {len(text)} chars")
    FILE.write_text(text, encoding="utf-8")
    print("Done.")


if __name__ == "__main__":
    main()
