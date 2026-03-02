#!/bin/bash

# ============================================================
#  Settings
# ============================================================

A_LIST="H"                                # Multiple central elements
#ELEMENTS="C V"                                   # Partner elements (B)
ELEMENTS=$(cat elements.txt)                   # Alternative: read element list from file
SKGEN="/home/ubuntu/skprogs-v.0.2.1/sktools/src/sktools/scripts/skgen.py"
SKDEF="./skdef.hsd"
SKDEF_TMP="./skdef_tmp.hsd"                      # Template containing "# NEW CASE"
ELEMENTS_Z="elements_z.txt"                      # Element → atomic number

USE_DUMMY=1                                      # 1 = use dummy mode (-d), 0 = normal mode

# ============================================================
#  Functions
# ============================================================

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
function add_pair_to_skdef() {
    A=$1
    B=$2

    PARAMS=$(select_params $A $B)
    GRID=$(echo $PARAMS | cut -d';' -f1)
    CALC=$(echo $PARAMS | cut -d';' -f2)

    NEWLINE="  $A-$B { Grid = $GRID ; Calculator = $CALC }"

    echo ">>> Adding new pair $A-$B to skdef.hsd"
    sed -i "0,/^# NEW CASE/s|# NEW CASE|$NEWLINE\n# NEW CASE|" "$SKDEF"
}

# ============================================================
#  Main Loop (loop over each A)
# ============================================================

for A in $A_LIST; do

    echo "=============================="
    echo " Processing element A = $A"
    echo "=============================="

    # Reset skdef.hsd from template for each A
    cp "$SKDEF_TMP" "$SKDEF"

    # Create output directory for this A
    mkdir -p "${A}-X"

    for B in $ELEMENTS; do

        # Skip A == B (avoid generating A-A pairs)
        if [[ "$A" == "$B" ]]; then
           echo "Skip $A-$B (same element)"
           continue
        fi

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

done

# End of script

