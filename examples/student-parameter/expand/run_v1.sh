#!/bin/bash

# ============================================================
#  Settings
# ============================================================

A="H"                                           # Central element (A–X pairs will be generated)
ELEMENTS="C V"                                  # List of partner elements (B)
#ELEMENTS=$(cat elements.txt)                   # Alternative: read element list from file
SKGEN="/home/ubuntu/skprogs-v.0.2.1/sktools/src/sktools/scripts/skgen.py"
SKDEF="./skdef.hsd"                             # Main skdef file
SKDEF_TMP="./skdef_expand_tmp.hsd"                     # Template skdef file (contains # NEW CASE placeholder)
ELEMENTS_Z="elements_z.txt"                     # Mapping: element → atomic number

USE_DUMMY=1                                     # 1 = use dummy mode (-d), 0 = normal mode

# ============================================================
#  Functions
# ============================================================

# Reset skdef.hsd from template before modifications
cp "$SKDEF_TMP" "$SKDEF"

# Return atomic number (Z) for a given element symbol
function get_Z() {
    awk -v el="$1" '$1 == el {print $2}' "$ELEMENTS_Z"
}

# Check if an element exists in skdef (A-A block must exist)
function element_exists_in_skdef() {
    grep -q "^[[:space:]]*$1-$1[[:space:]]*{" "$SKDEF"
}

# Check if a pair A-B already exists in skdef
function pair_exists_in_skdef() {
    grep -q "^[[:space:]]*$1-$2[[:space:]]*{" "$SKDEF"
}

# Automatically choose Grid and Calculator parameters
# based on the heavier atomic number of the pair
function select_params() {
    Z1=$(get_Z $1)
    Z2=$(get_Z $2)
    Z=$(( Z1 > Z2 ? Z1 : Z2 ))   # Use the heavier element

    if (( Z <= 20 )); then
        GRID="\$EqGridCutoff10"
        CALC="\$SkTwocnt_300_150"
    elif (( Z <= 56 )); then
        GRID="\$EqGrid"
        CALC="\$SkTwocnt_400_200"
    else
        GRID="\$EqGridCutoff12"
        CALC="\$SkTwocnt_400_200"
    fi

    echo "$GRID;$CALC"
}

# Insert a new A-B pair block into skdef.hsd
# by replacing the placeholder "# NEW CASE" in the template
function add_pair_to_skdef() {
    A=$1
    B=$2

    PARAMS=$(select_params $A $B)
    GRID=$(echo $PARAMS | cut -d';' -f1)
    CALC=$(echo $PARAMS | cut -d';' -f2)

    NEWLINE="  $A-$B { Grid = $GRID ; Calculator = $CALC }"

    echo ">>> Adding new pair $A-$B to skdef.hsd"
    sed -i "s|# NEW CASE|$NEWLINE|" "$SKDEF"
}

# Output directory for generated SK files
mkdir -p "${A}-X"

# ============================================================
#  Main Loop
# ============================================================

for B in $ELEMENTS; do

    # Skip if element B is not defined in skdef
    if ! element_exists_in_skdef "$B"; then
      echo "Skip $B (not in skdef.hsd)"
      continue
    fi

    # Add A-B pair if missing
    if ! pair_exists_in_skdef "$A" "$B"; then
      add_pair_to_skdef "$A" "$B"
    fi

    echo ">>> Generating SK table for $A-$B"

    # Run SKGEN (dummy mode optional)
    if [[ $USE_DUMMY -eq 1 ]]; then
        python3 $SKGEN -o slateratom -t sktwocnt sktable -d $A,$B $A,$B
    else
        python3 $SKGEN -o slateratom -t sktwocnt sktable $A,$B $A,$B
    fi

    # Move generated .skf files into A-X directory
    for f in "${A}-${A}.skf" "${A}-${B}.skf" "${B}-${A}.skf" "${B}-${B}.skf"; do
        if [ -f "$f" ]; then
            mv "$f" "${A}-X/"
        fi
    done

done

# End of script

