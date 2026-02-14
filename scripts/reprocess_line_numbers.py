#!/usr/bin/env python3
"""
Re-run the GPT-5.2 cleanup on files with embedded line numbers.
Uses --file and --overwrite flags of clean_with_claude.py.
"""
import subprocess
import sys
import time

# Files with >40 suspected embedded numbers from the scan, ordered by severity.
# Excluding III_2_gospel_egyptians.md (already manually fixed).
FILES_TO_REPROCESS = [
    "tractates/I_5_tripartite_tractate.md",
    "tractates/VIII_1_zostrianos.md",
    "tractates/II_1_apocryphon_john.md",
    "tractates/X_1_marsanes.md",
    "tractates/XI_3_allogenes.md",
    "tractates/VII_2_second_treatise_great_seth.md",
    "tractates/II_2_gospel_thomas.md",
    "tractates/I_2_apocryphon_james.md",
    "tractates/III_5_dialogue_savior.md",
    "tractates/XI_2_valentinian_exposition.md",
    "tractates/XIII_1_trimorphic_protennoia.md",
    "tractates/V_3_first_apocalypse_james.md",
    "tractates/VI_3_authoritative_teaching.md",
    "tractates/VI_1_acts_peter_twelve.md",
    "tractates/II_6_exegesis_soul.md",
    "tractates/VII_5_three_steles_seth.md",
    "tractates/VI_2_thunder_perfect_mind.md",
    "tractates/XII_1_sentences_sextus.md",
    "tractates/BG_1_gospel_mary.md",
    "tractates/IX_1_melchizedek.md",
    "tractates/VI_5_plato_republic.md",
    "tractates/IX_3_testimony_truth.md",
    "tractates/XI_1_interpretation_knowledge.md",
    "tractates/I_1_prayer_apostle_paul.md",
    "tractates/XII_3_fragments.md",
]

def main():
    dry_run = "--dry-run" in sys.argv
    
    print(f"{'[DRY RUN] ' if dry_run else ''}Re-processing {len(FILES_TO_REPROCESS)} files with GPT-5.2...\n")
    
    for i, f in enumerate(FILES_TO_REPROCESS, 1):
        print(f"[{i}/{len(FILES_TO_REPROCESS)}] {f}")
        if dry_run:
            continue
        
        cmd = [
            sys.executable, "scripts/clean_with_claude.py",
            "--file", f,
            "--overwrite",
        ]
        result = subprocess.run(cmd, capture_output=True, text=True, cwd=r"C:\Users\mlf\source\temp\NagHammadiLIbrary")
        print(result.stdout.strip())
        if result.returncode != 0:
            print(f"  STDERR: {result.stderr.strip()}")
        
        # Pause between calls
        if i < len(FILES_TO_REPROCESS):
            time.sleep(2)
    
    print(f"\nDone. {len(FILES_TO_REPROCESS)} files {'would be ' if dry_run else ''}reprocessed.")


if __name__ == "__main__":
    main()
