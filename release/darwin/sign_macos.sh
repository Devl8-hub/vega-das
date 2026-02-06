#!/bin/bash

# macOS Code Signing and Notarization Script for Vega DAS
# Usage: ./sign_macos.sh "Developer ID Application: Your Name (ID)" [AppBundlePath]

IDENTITY="$1"
APP_BUNDLE="${2:-Vega DAS.app}"
ENTITLEMENTS="entitlements.plist"

if [ -z "$IDENTITY" ]; then
    echo "Usage: $0 \"Developer ID Application: Your Name (ID)\" [AppBundlePath]"
    exit 1
fi

if [ ! -d "$APP_BUNDLE" ]; then
    echo "Error: App bundle not found at $APP_BUNDLE"
    exit 1
fi

echo "Signing Vega DAS with identity: $IDENTITY"

# 1. Sign internal libraries, helpers, and sub-bundles
echo "Signing internal libraries and sub-bundles..."
find "$APP_BUNDLE/Contents" -type f \( -name "*.dylib" -o -name "*.so" -o -name "Python" -o -name "vega-das-thumbnailer" \) -print0 | xargs -0 codesign --force --sign "$IDENTITY" --timestamp --options runtime

# Sign sub-bundles (extensions, etc)
find "$APP_BUNDLE/Contents/PlugIns" -name "*.appex" -type d -print0 | xargs -0 codesign --force --sign "$IDENTITY" --timestamp --options runtime
find "$APP_BUNDLE/Contents/PlugIns" -name "*.app" -type d -print0 | xargs -0 codesign --force --sign "$IDENTITY" --timestamp --options runtime

# 2. Sign the app bundle itself
echo "Signing the application bundle..."
codesign --force --sign "$IDENTITY" --entitlements "$ENTITLEMENTS" --timestamp --options runtime "$APP_BUNDLE"

# 3. Verify the signature
echo "Verifying signature..."
codesign --verify --deep --strict --verbose=2 "$APP_BUNDLE"
spctl --assess --type execute --verbose "$APP_BUNDLE"

echo "Signing complete."

# Notarization reminder
echo "----------------------------------------------------"
echo "To notarize, create a zip and submit:"
echo "/usr/bin/ditto -c -k --keepParent \"$APP_BUNDLE\" \"VegaDAS_to_notarize.zip\""
echo "xcrun notarytool submit VegaDAS_to_notarize.zip --apple-id \"your@email.com\" --password \"app-specific-password\" --team-id \"TEAMID\" --wait"
echo "----------------------------------------------------"
echo "After notarization, staple the result:"
echo "xcrun stapler staple \"$APP_BUNDLE\""
