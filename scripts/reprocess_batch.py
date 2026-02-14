#!/usr/bin/env python3
"""
Re-run the GPT-5.2 cleanup on files with embedded line numbers.
Imports the clean_with_claude module directly instead of using subprocess.
"""
import sys
import time
from pathlib import Path

# Add scripts dir to path
sys.path.insert(0, str(Path(__file__).parent))

from clean_with_claude import create_client, get_deployment, process_file

# Files with >40 suspected embedded numbers, excluding already-fixed ones.
# Gospel of Thomas already re-done. Tripartite Tractate already re-done.
# Gospel of Egyptians was manually fixed.
FILES_TO_REPROCESS = [
    # "tractates/I_5_tripartite_tractate.md",   # DONE
    "tractates/VIII_1_zostrianos.md",
    "tractates/II_1_apocryphon_john.md",
    "tractates/X_1_marsanes.md",
    "tractates/XI_3_allogenes.md",
    "tractates/VII_2_second_treatise_great_seth.md",
    # "tractates/II_2_gospel_thomas.md",         # DONE
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
    client = create_client()
    deployment = get_deployment()
    
    total = len(FILES_TO_REPROCESS)
    print(f"Re-processing {total} files with GPT-5.2 (updated prompt)...\n")
    
    processed = 0
    errors = 0
    start = time.time()
    
    for i, f in enumerate(FILES_TO_REPROCESS, 1):
        print(f"[{i}/{total}]", end=" ")
        try:
            result = process_file(client, deployment, Path(f), overwrite=True)
            if result:
                processed += 1
            time.sleep(1)  # Brief pause between API calls
        except Exception as e:
            print(f"  ERROR: {e}")
            errors += 1
    
    elapsed = time.time() - start
    print(f"\nDone in {elapsed:.0f}s — Processed: {processed}, Errors: {errors}")


if __name__ == "__main__":
    main()
