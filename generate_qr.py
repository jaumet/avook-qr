#!/usr/bin/env python3
import json
import subprocess
import datetime
import pathlib
import uuid


def main():
    default_url = "https://audiovook.com/qr/code/"
    default_image = "qrlogo.png"

    base_url = (
        input(f"Base URL (ex: https://my.domain/qr/) [{default_url}]: ").strip()
        or default_url
    )
    img_name = (
        input(f"Nom d'imatge per al QR (ex: product1.png) [{default_image}]: ").strip()
        or default_image
    )

    product_id = input("ID de producte: ").strip()
    in_shop = input("És en una botiga? (s/n): ").lower().startswith("s")
    shop_id = input("ID de botiga (en blanc si no): ").strip()

    unique_code = uuid.uuid4().hex[:12]
    final_url = f"{base_url}{unique_code}"
    print(f"Generating QR code for: {final_url}")

    subprocess.run(
        ["./QR-generate.sh", "--url", final_url, "-o", img_name],
        cwd="original",
        check=True,
    )

    metadata = {
        "qr_image_name": img_name,
        "product_id": product_id,
        "date_generation": datetime.datetime.now(datetime.timezone.utc).isoformat(),
        "is_in_shop": in_shop,
        "shop_id": shop_id or None,
        "unique_code": unique_code,
        "final_url": final_url,
    }

    out_dir = pathlib.Path("original/OUTPUT")
    out_dir.mkdir(exist_ok=True)
    json_path = out_dir / f"{pathlib.Path(img_name).stem}.json"
    json_path.write_text(json.dumps(metadata, indent=2))
    print("QR i metadades creats.")


if __name__ == "__main__":
    main()
