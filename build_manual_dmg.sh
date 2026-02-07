#!/bin/bash

# Configuration
APP_NAME="Vega DAS"
BUILD_DIR="../build_darwin"
APP_BUNDLE="${BUILD_DIR}/bin/${APP_NAME}.app"
# Use a distinctive name so we know it's the enhanced one
DMG_NAME="Vega-DAS-Installer-DragDrop.dmg"
OUTPUT_DMG="${BUILD_DIR}/${DMG_NAME}"
VOL_NAME="Vega DAS Installer"
STAGING_DIR="${BUILD_DIR}/dmg_staging"

# Check if App Bundle exists
if [ ! -d "$APP_BUNDLE" ]; then
    echo "Error: App bundle not found at $APP_BUNDLE"
    exit 1
fi

# Cleanup previous build artifacts
if [ -f "$OUTPUT_DMG" ]; then
    echo "Removing existing DMG..."
    rm "$OUTPUT_DMG"
fi
if [ -d "$STAGING_DIR" ]; then
    rm -rf "$STAGING_DIR"
fi

# Prepare staging area
echo "Preparing staging directory..."
mkdir -p "$STAGING_DIR"

echo "Copying App Bundle to staging..."
cp -R "$APP_BUNDLE" "$STAGING_DIR/"

# Remove quarantine attributes to prevent "App is damaged" error
echo "Removing quarantine attributes..."
xattr -cr "${STAGING_DIR}/${APP_NAME}.app"

# Ad-hoc sign the application to ensure validity
echo "Ad-hoc signing the application..."
codesign --force --deep -s - "${STAGING_DIR}/${APP_NAME}.app"

# Create /Applications symlink for Drag and Drop functionality
echo "Creating /Applications link..."
ln -s /Applications "$STAGING_DIR/Applications"

# Create DMG using hdiutil
echo "Creating DMG from $STAGING_DIR..."
hdiutil create \
    -volname "${VOL_NAME}" \
    -srcfolder "${STAGING_DIR}" \
    -ov -format UDZO \
    "${OUTPUT_DMG}"

RESULT=$?

# Cleanup staging directory to save space
echo "Cleaning up staging directory..."
rm -rf "$STAGING_DIR"

if [ $RESULT -eq 0 ]; then
    echo "-------------------------------------------------------"
    echo "Success! Production-grade, Protected DMG created:"
    echo "${OUTPUT_DMG}"
    echo "-------------------------------------------------------"
else
    echo "Error creating DMG"
    exit 1
fi
