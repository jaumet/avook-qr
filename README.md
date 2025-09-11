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

The generated JSON now follows this structure:

```json
{
  "qr_image_name": "2025-08-29--b0393c8ed803.png",
  "product_id": "11",
  "date_generation": "2025-08-29T09:33:38.598153+00:00",
  "pvp": 10,
  "pvp_currentcy": "euro",
  "status": "ready",
  "shop_id": null,
  "pin": "123456",
  "qr_code": "b0393c8ed803",
  "avook_url": "https://audiovook.com/qr/code/b0393c8ed803"
}
```

The `pin` value is automatically generated for each QR as a random six-digit number.

Additional prompts let you choose a subfolder inside `OUTPUT/` and the
number of QR codes to generate in one run. If no subfolder is specified,
files land directly in `OUTPUT/`. When generating more than one QR, the
script asks whether the product and shop information should be reused for
all codes or entered separately for each one.
