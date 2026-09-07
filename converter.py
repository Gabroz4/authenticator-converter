#!/usr/bin/env python3
import json
import sys
import time
from urllib.parse import urlparse, parse_qs, unquote


def convert(proton_path, twofas_path):
    with open(proton_path, "r", encoding="utf-8") as f:
        proton = json.load(f)

    now_ms = int(time.time() * 1000)
    services = []
    skipped = []

    for idx, item in enumerate(proton.get("entries", [])):
        content = item.get("content", {})
        entry_type = content.get("entry_type")

        if entry_type != "Totp":
            skipped.append((content.get("name", "?"), entry_type))
            continue

        uri = content.get("uri", "")
        parsed = urlparse(uri)
        qs = parse_qs(parsed.query)

        issuer = qs.get("issuer", [""])[0]
        secret = qs.get("secret", [""])[0].replace(" ", "")
        algo = qs.get("algorithm", ["SHA1"])[0].upper()
        digits = int(qs.get("digits", ["6"])[0])
        period = int(qs.get("period", ["30"])[0])

        account = content.get("name") or unquote(parsed.path.lstrip("/"))

        if not secret:
            skipped.append((account, "no secret found in uri"))
            continue

        services.append(
            {
                "name": issuer or account,
                "secret": secret,
                "updatedAt": now_ms,
                "serviceTypeID": None,
                "order": {"position": idx},
                "icon": None,
                "badge": None,
                "otp": {
                    "account": account,
                    "issuer": issuer,
                    "tokenType": "TOTP",
                    "algorithm": algo,
                    "digits": digits,
                    "period": period,
                    "counter": 0,
                    "source": "link",
                    "link": uri,
                },
            }
        )

    backup = {
        "services": services,
        "groups": [],
        "schemaVersion": 4,
        "appVersionCode": 5000012,
        "appVersionName": "5.2.0",
        "appOrigin": "ios",
    }

    with open(twofas_path, "w", encoding="utf-8") as f:
        json.dump(backup, f, indent=2)

    print(f"Converted {len(services)} TOTP entries -> {twofas_path}")
    if skipped:
        print(
            f"Skipped {len(skipped)} entries (non-TOTP or unparseable):",
            file=sys.stderr,
        )
        for name, reason in skipped:
            print(f"  - {name}: {reason}", file=sys.stderr)


if __name__ == "__main__":
    if len(sys.argv) != 3:
        print(f"Usage: {sys.argv[0]} <proton_export.json> <backup.2fas>")
        sys.exit(1)
    convert(sys.argv[1], sys.argv[2])

