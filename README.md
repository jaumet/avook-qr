# avook-qr

CLI utility to generate QR codes with an embedded logo and matching metadata.

```
python3 generate_qr.py
```

The script prompts for QR details and metadata. Press **Enter** to accept
the default base URL:

- Base URL: `https://audiovook.com/qr/code/`

The final QR encodes the base URL plus a generated unique code. The PNG and
its matching JSON metadata are saved in `OUTPUT/` using the naming pattern
`YYYY-MM-DD--CODE.*`.

Additional prompts let you choose a subfolder inside `OUTPUT/` and the
number of QR codes to generate in one run. If no subfolder is specified,
files land directly in `OUTPUT/`.
