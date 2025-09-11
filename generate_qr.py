#!/usr/bin/env python3
import json
import subprocess
import datetime
import pathlib
import uuid
import shutil
import random


def _parse_pvp(value: str):
    try:
        num = float(value)
    except ValueError:
        return 0
    return int(num) if num.is_integer() else num

def check_dependencies():
    required = ["qrencode", "convert", "identify", "composite"]
    missing = [cmd for cmd in required if shutil.which(cmd) is None]
    if missing:
        print(
            "Falten eines necessàries: " + ", ".join(missing)
            + ". Si us plau, instal·la 'qrencode' i 'ImageMagick'."
        )
        raise SystemExit(1)


def main():
    check_dependencies()
    default_url = "https://audiovook.com/qr/code/"

    base_url = (
        input(f"Base URL (ex: https://my.domain/qr/) [{default_url}]: ").strip()
        or default_url
    )
    folder = input("Carpeta dins OUTPUT (en blanc per defecte): ").strip()
    out_dir = pathlib.Path("OUTPUT") / folder if folder else pathlib.Path("OUTPUT")
    out_dir.mkdir(parents=True, exist_ok=True)

    count_str = input("Nombre de QR a generar [1]: ").strip()
    num_qr = int(count_str) if count_str else 1

    same_meta = True
    if num_qr > 1:
        same_meta = input(
            "Aplicar les mateixes dades de producte i botiga a tots els QR? (s/n): "
        ).lower().startswith("s")

    if same_meta:
        common_product_id = input("ID de producte: ").strip()
        common_shop_id = input("ID de botiga (en blanc si no): ").strip()
        common_pvp = _parse_pvp(input("PVP: ").strip())
        common_currency = input("Moneda del PVP [euro]: ").strip() or "euro"

    for i in range(num_qr):
        print(f"\n-- QR {i + 1} de {num_qr} --")
        if same_meta:
            product_id = common_product_id
            shop_id = common_shop_id
            pvp = common_pvp
            currency = common_currency
        else:
            product_id = input("ID de producte: ").strip()
            shop_id = input("ID de botiga (en blanc si no): ").strip()
            pvp = _parse_pvp(input("PVP: ").strip())
            currency = input("Moneda del PVP [euro]: ").strip() or "euro"

        pin = f"{random.randint(0, 999999):06d}"

        qr_code = uuid.uuid4().hex[:12]
        avook_url = f"{base_url}{qr_code}"
        now = datetime.datetime.now(datetime.timezone.utc)
        date_part = now.date().isoformat()
        file_stem = f"{date_part}--{qr_code}"
        img_name = f"{file_stem}.png"
        json_name = f"{file_stem}.json"
        print(f"Generating QR code for: {avook_url}")

        subprocess.run(
            ["./QR-generate.sh", "--url", avook_url, "-o", img_name],
            cwd="original",
            check=True,
        )

        src_png = pathlib.Path("original/OUTPUT") / img_name
        dst_png = out_dir / img_name
        shutil.move(src_png, dst_png)

        metadata = {
            "qr_image_name": img_name,
            "product_id": product_id,
            "date_generation": now.isoformat(),
            "pvp": pvp,
            "pvp_currentcy": currency,
            "status": "ready",
            "shop_id": shop_id or None,
            "pin": pin,
            "qr_code": qr_code,
            "avook_url": avook_url,
        }

        (out_dir / json_name).write_text(json.dumps(metadata, indent=2))
        print("QR i metadades creats.")


if __name__ == "__main__":
    main()
