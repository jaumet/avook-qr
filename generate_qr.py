+57-0
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
    out_dir = pathlib.Path("OUTPUT")
    out_dir.mkdir(exist_ok=True)
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
