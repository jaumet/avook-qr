#!/bin/bash

# Default values
QR_COLOR="000033"  # Dark blue QR color
BACKGROUND="FFFFFF"  # White background
LOGO="./qrlogo.png"  # Logo file (in the same folder as the script)
URL=""
QR_OUTPUT=""

# Directories
TEMP_DIR="tools"
OUTPUT_DIR="OUTPUT"
mkdir -p "$TEMP_DIR" "$OUTPUT_DIR"

# Parse arguments
while [[ $# -gt 0 ]]; do
    case $1 in
        --url)
            URL="$2"
            shift; shift
            ;;
        -o|--output)
            QR_OUTPUT="$2"
            shift; shift
            ;;
        *)
            echo "Unknown parameter: $1"
            exit 1
            ;;
    esac
done

# Check required parameters
if [ -z "$URL" ] || [ -z "$QR_OUTPUT" ]; then
    echo "Usage: $0 --url \"https://your-url.com\" -o output.png"
    exit 1
fi

# Ensure the output file is saved in the OUTPUT directory
QR_OUTPUT="$OUTPUT_DIR/$QR_OUTPUT"

# Step 1: Generate the QR code with high error correction (-l H)
echo "Generating QR code for: $URL"
qrencode -s 20 -m 2 -l H -o "$TEMP_DIR/qr_base.png" "$URL"

# Step 2: Apply colors using ImageMagick
convert "$TEMP_DIR/qr_base.png" -fill "#$QR_COLOR" -opaque black -fill "#$BACKGROUND" -opaque white "$TEMP_DIR/qr_colored.png"

# Step 3: Get QR size
QR_SIZE=$(identify -format "%w" "$TEMP_DIR/qr_colored.png")
echo "QR Code size: $QR_SIZE x $QR_SIZE"

# Step 4: Reduce the hole size to 15% instead of 25%
HOLE_SIZE=$((QR_SIZE / 6))
HALF_HOLE=$((HOLE_SIZE / 2))

# Step 5: Calculate center
CENTER_X=$((QR_SIZE / 2))
CENTER_Y=$((QR_SIZE / 2))

TOP_LEFT_X=$((CENTER_X - HALF_HOLE))
TOP_LEFT_Y=$((CENTER_Y - HALF_HOLE))
BOTTOM_RIGHT_X=$((CENTER_X + HALF_HOLE))
BOTTOM_RIGHT_Y=$((CENTER_Y + HALF_HOLE))

echo "Creating hole from ($TOP_LEFT_X, $TOP_LEFT_Y) to ($BOTTOM_RIGHT_X, $BOTTOM_RIGHT_Y)"

# Step 6: Cut a transparent hole in the QR center
convert "$TEMP_DIR/qr_colored.png" -alpha set -channel RGBA -fill none -draw "rectangle $TOP_LEFT_X,$TOP_LEFT_Y $BOTTOM_RIGHT_X,$BOTTOM_RIGHT_Y" "$TEMP_DIR/qr_with_hole.png"

# Step 7: Resize the logo and save it inside the tools directory
echo "Resizing logo..."
convert "$LOGO" -background none -resize "${HOLE_SIZE}x${HOLE_SIZE}" "$TEMP_DIR/qrlogo_resized.png"

# Step 8: Overlay the logo on the QR
echo "Inserting logo..."
composite -gravity center "$TEMP_DIR/qrlogo_resized.png" "$TEMP_DIR/qr_with_hole.png" "$QR_OUTPUT"

# Step 9: Cleanup temporary files
rm -rf "$TEMP_DIR"

echo "QR code with logo created: $QR_OUTPUT"

