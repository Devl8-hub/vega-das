#!/bin/bash

# Ad-hoc Code Signing Script for Vega DAS (Local Testing Only)
# This signs the app for local use to avoid Gatekeeper warnings
# NOT suitable for distribution - use sign_macos.sh with Developer ID for that

APP_BUNDLE="${1:-../../build/bin/Vega DAS.app}"

if [ ! -d "$APP_BUNDLE" ]; then
    echo "Error: App bundle not found at $APP_BUNDLE"
    echo "Usage: $0 [AppBundlePath]"
    exit 1
fi

echo "=================================================="
echo "Ad-hoc Signing Vega DAS for Local Testing"
echo "=================================================="
echo "App Bundle: $APP_BUNDLE"
echo ""

# Remove any existing signatures
echo "Removing existing signatures..."
xattr -cr "$APP_BUNDLE"
codesign --remove-signature "$APP_BUNDLE" 2>/dev/null || true

# Sign all dylibs and .so files
echo "Signing libraries..."
find "$APP_BUNDLE/Contents" -type f \( -name "*.dylib" -o -name "*.so" \) -print0 | while IFS= read -r -d '' file; do
    codesign --force --deep --sign - "$file" 2>/dev/null
done

# Sign Python executable if exists
if [ -f "$APP_BUNDLE/Contents/Resources/5.1/python/bin/python3.11" ]; then
    echo "Signing Python..."
    codesign --force --deep --sign - "$APP_BUNDLE/Contents/Resources/5.1/python/bin/python3.11" 2>/dev/null
fi

# Sign thumbnailer extension if exists
if [ -d "$APP_BUNDLE/Contents/PlugIns" ]; then
    echo "Signing plugins..."
    find "$APP_BUNDLE/Contents/PlugIns" -name "*.appex" -type d -print0 | while IFS= read -r -d '' plugin; do
        codesign --force --deep --sign - "$plugin" 2>/dev/null
    done
fi

# Sign the main app bundle
echo "Signing main application..."
codesign --force --deep --sign - "$APP_BUNDLE"

# Verify
echo ""
echo "Verifying signature..."
if codesign --verify --deep "$APP_BUNDLE" 2>/dev/null; then
    echo "✓ Signature verified successfully"
else
    echo "✗ Signature verification failed"
    exit 1
fi

echo ""
echo "=================================================="
echo "✓ Ad-hoc signing complete!"
echo "=================================================="
echo ""
echo "The app should now open without warnings on this Mac."
echo ""
echo "NOTE: This is LOCAL ONLY signing."
echo "For distribution, use sign_macos.sh with an Apple Developer ID."
