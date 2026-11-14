#!/usr/bin/env python3
"""Build the self-contained explorer from the three module JSON payloads.

Runs each module to (re)generate its JSON, embeds all three into
tourney_template.html, and writes tourney_explorer.html + index.html.
"""
import json

import doubling_up
import icm
import strategy


def main() -> None:
    # Build the data straight from each module so the artifact matches the code.
    payload = {
        "doubling": doubling_up.build_artifact_data(),
        "icm": icm.build_artifact_data(),
        "strategy": strategy.build_artifact_data(),
    }
    blob = json.dumps(payload, separators=(",", ":"))
    tpl = open("tourney_template.html").read()
    out = tpl.replace("/*__DATA__*/null", blob)
    with open("tourney_explorer.html", "w") as f:
        f.write(out)
    print(f"wrote tourney_explorer.html ({len(out)/1e3:.0f} KB)")
    with open("index.html", "w") as f:
        f.write('<!doctype html>\n<html lang="en">\n' + out + "\n</html>\n")
    print("wrote index.html")


if __name__ == "__main__":
    main()
