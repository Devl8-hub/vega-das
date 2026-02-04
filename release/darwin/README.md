# macOS Distribution Configuration

This directory contains files used for packaging and distributing Vega DAS on macOS.

## Code Signing and Notarization

To prevent the "Application can't be opened" or "Damaged" errors on other Macs, the application must be signed with an Apple Developer certificate and notarized by Apple.

### Automating with `sign_macos.sh`

1.  Open Terminal in this directory.
2.  Run the signing script:
    ```bash
    ./sign_macos.sh "Developer ID Application: Your Name (ID)" "/path/to/Vega DAS.app"
    ```
3.  Follow the notarization steps printed at the end of the script.

## Workaround for Recipients (Unsigned Apps)

If you are distributing an unsigned version (e.g., for testing), recipients will see a security warning. They can bypass it by:

1.  **Right-click** (or Control-click) the application icon.
2.  Select **Open** from the menu.
3.  In the dialog that follows, click **Open** again.
4.  The application will now open normally.
