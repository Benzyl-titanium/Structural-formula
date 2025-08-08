from fastapi import FastAPI
from fastapi.responses import FileResponse, HTMLResponse, Response
from fastapi.staticfiles import StaticFiles
from pathlib import Path
from rdkit import Chem
from rdkit.Chem.Draw import IPythonConsole
from rdkit.Chem import Draw
from rdkit.Chem.Draw import rdMolDraw2D
import datetime
import os
from PIL import Image
import io
import logging
import argparse
import sys
import subprocess
import urllib.parse

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

app = FastAPI()

images_dir = Path("./docs/images").resolve()
try:
    images_dir.mkdir(exist_ok=True, parents=True)
    logger.info(f"Images directory created/verified at: {images_dir}")
except Exception as e:
    logger.error(f"Error creating images directory: {str(e)}")
    raise

app.mount("/images", StaticFiles(directory=str(images_dir)), name="images")

def copy_to_clipboard(text):
    try:
        if sys.platform == 'win32':
            # Windows
            cmd = 'clip'
            p = subprocess.Popen(cmd, stdin=subprocess.PIPE, shell=True)
            p.communicate(input=text.encode('utf-8'))
        elif sys.platform == 'darwin':
            # macOS
            cmd = 'pbcopy'
            p = subprocess.Popen(cmd, stdin=subprocess.PIPE)
            p.communicate(input=text.encode('utf-8'))
        else:
            # Linux (需要xclip或xsel)
            cmd = 'xclip -selection clipboard'
            p = subprocess.Popen(cmd, stdin=subprocess.PIPE, shell=True)
            p.communicate(input=text.encode('utf-8'))
    except Exception as e:
        print(f"无法复制到剪贴板: {e}")

def smiles_to_image(smiles):
    size = 200
    format = "svg"
    if smiles == '':
        print("请输入有效的SMILES字符串")
        return
    try:
        mol = Chem.MolFromSmiles(smiles)
        if mol is None:
            print("无效的SMILES字符串")
            return
        safe_smiles = smiles.replace('/', '_').replace('\\', '_').replace(':', '_')
        filename = f"{safe_smiles}_{size}.{format}"
        path = images_dir / filename
        # 对文件名进行URL编码
        url_filename = urllib.parse.quote(filename)
        img_tag = f'<img src="images/{url_filename}">'
        if path.is_file():
            print(f"SVG图片已保存: {path}")
            print(img_tag)
            copy_to_clipboard(img_tag)
            print("已复制到剪贴板！")
            return str(path)
        path.parent.mkdir(parents=True, exist_ok=True)
        drawer = rdMolDraw2D.MolDraw2DSVG(size, size)
        drawer.drawOptions().clearBackground = True
        drawer.drawOptions().backgroundColour = None
        drawer.DrawMolecule(mol)
        drawer.FinishDrawing()
        svg = drawer.GetDrawingText()
        with open(path, 'w', encoding='utf-8') as f:
            f.write(svg)
        print(f"SVG图片已保存: {path}")
        print(img_tag)
        copy_to_clipboard(img_tag)
        print("已复制到剪贴板！")
        return str(path)
    except Exception as e:
        print(f"生成图片时出错: {str(e)}")
        return

if __name__ == "__main__":
    smiles = input("SMILES:").strip()
    if not smiles:
        print("exit")
    else:
        smiles_to_image(smiles)
