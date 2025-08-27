# avook-qr

CLI utility to generate QR codes with an embedded logo and matching metadata.

```
python3 generate_qr.py
```

The script prompts for QR details and metadata. Press **Enter** to accept
the defaults:

- Base URL: `https://audiovook.com/qr/code/`
- QR image filename: `qrlogo.png`

The final QR encodes the base URL plus a generated unique code and writes a
JSON file alongside the image in `original/OUTPUT/`.
