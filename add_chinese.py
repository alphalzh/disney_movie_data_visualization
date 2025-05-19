#!/usr/bin/env python3
"""
Fill blank chinese_title cells in a Disney gross-income CSV by
  1) querying googletrans (online)
  2) falling back to Argos-Translate (offline)
Saves a new file with "_filled" suffix.
"""

import os
import pandas as pd

# ---------- CONFIG ----------
CSV_PATH = "disney_movies_with_cn.csv"
OUT_PATH = "disney_movies_with_cn_filled.csv"
SRC_COL = "movie_title"
CN_COL  = "chinese_title"
# ----------------------------

def _make_googletrans():
    from googletrans import Translator          # pygoogletranslation-like API
    return Translator(service_urls=[
        # multiple mirrors improve resilience
        "translate.google.com", "translate.googleapis.com"
    ])

def _make_argos():
    import argostranslate.package as pkg
    import argostranslate.translate as argo

    # ensure an en→zh model is available
    installed = argo.get_installed_languages()
    has_model = any(l.code == "en" for l in installed)\
                and any(l.code.startswith("zh") for l in installed)
    if not has_model:
        # download base model (~35 MB) once; future runs reuse it
        import tempfile, pathlib, requests, sys, shutil
        print("Downloading Argos en→zh model …")
        url = ("https://github.com/argosopentech"
               "/argos-models/raw/main/en_zh/translate-en_zh.argosmodel")
        tmp = tempfile.NamedTemporaryFile(delete=False)
        tmp.write(requests.get(url, timeout=120).content)
        tmp.close()
        pkg.install_from_path(tmp.name)
        print("Model installed.")
    return argo

def translate_text(text, gtrans=None, argo=None):
    """Best-effort Simplified-Chinese translation."""
    if not text:
        return ""
    # 1) Google free endpoint
    try:
        if gtrans is None:
            gtrans = _make_googletrans()
        return gtrans.translate(text, dest="zh-CN", src="en").text
    except Exception as e:
        print(f"[googletrans] {e} → falling back to Argos")
    # 2) offline Argos
    if argo is None:
        argo = _make_argos()
    lang_en, lang_zh = [l for l in argo.get_installed_languages()
                        if l.code in ("en", "zh", "zh_CN", "zh-CN")]
    translation = lang_en.get_translation(lang_zh)
    return translation.translate(text)

def main():
    df = pd.read_csv(CSV_PATH)
    missing = df[CN_COL].isna() | (df[CN_COL] == "")
    if missing.sum() == 0:
        print("No blanks to fill – nothing to do.")
        return

    translator = _make_googletrans()
    argos = None  # lazy init
    for idx, row in df[missing].iterrows():
        cn = translate_text(row[SRC_COL], translator, argos)
        df.at[idx, CN_COL] = cn

    df.to_csv(OUT_PATH, index=False)
    print(f"Done! {missing.sum()} rows filled → {OUT_PATH}")

if __name__ == "__main__":
    main()

