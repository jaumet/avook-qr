#!/usr/bin/env python3
import json
import subprocess
import datetime
import pathlib
import uuid
import shutil


def main():
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

    # --- PR PROPOSAL: permet reutilitzar metadades per a múltiples QR ---
    same_meta = True
    if num_qr > 1:
        same_meta = input(
            "Aplicar les mateixes dades de producte i botiga a tots els QR? (s/n): "
        ).lower().startswith("s")

    if same_meta:
        common_product_id = input("ID de producte: ").strip()
        common_in_shop = input("És en una botiga? (s/n): ").lower().startswith("s")
        common_shop_id = input("ID de botiga (en blanc si no): ").strip()

    for i in range(num_qr):
        print(f"\n-- QR {i + 1} de {num_qr} --")
        if same_meta:
            product_id = common_product_id
            in_shop = common_in_shop
            shop_id = common_shop_id
        else:
            product_id = input("ID de producte: ").strip()
            in_shop = input("És en una botiga? (s/n): ").lower().startswith("s")
            shop_id = input("ID de botiga (en blanc si no): ").strip()

        unique_code = uuid.uuid4().hex[:12]
        final_url = f"{base_url}{unique_code}"
        now = datetime.datetime.now(datetime.timezone.utc)
        date_part = now.date().isoformat()
        file_stem = f"{date_part}--{unique_code}"
        img_name = f"{file_stem}.png"
        json_name = f"{file_stem}.json"
        print(f"Generating QR code for: {final_url}")

        subprocess.run(
            ["./QR-generate.sh", "--url", final_url, "-o", img_name],
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
            "is_in_shop": in_shop,
            "shop_id": shop_id or None,
            "unique_code": unique_code,
            "final_url": final_url,
        }

        (out_dir / json_name).write_text(json.dumps(metadata, indent=2))
        print("QR i metadades creats.")


if __name__ == "__main__":
    main()
