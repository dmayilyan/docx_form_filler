import os
import re
import shutil
import subprocess
import zipfile
from functools import reduce
from glob import glob
from typing import Any, List


def libreoffice_exists(timeout: int = None) -> bool:
    try:
        args = ["which", "libreoffice"]
        subprocess.run(args, text=True, stdout=subprocess.PIPE, check=True, shell=False, timeout=timeout)
    except subprocess.CalledProcessError as e:
        print("Libreoffice not found. Please install libreoffice and make sure it is visible in the $PATH.")
        raise e

    return True


def rename_pdf(final_name: str, docx_fn: str) -> None:
    initial_path = os.path.split(final_name)[0]
    docx_name = os.path.splitext(os.path.basename(docx_fn))[0]

    initial_name = os.path.join(initial_path, f"{docx_name}.pdf")
    os.rename(initial_name, final_name)


class LibreOfficeError(Exception):
    def __init__(self, output) -> None:
        self.output = output


def convert_to_pdf(output_folder: str, source: str, timeout: int = None) -> Any:
    args = [
        "libreoffice",
        "--headless",
        "--convert-to",
        "pdf",
        "--outdir",
        output_folder,
        source,
    ]

    process = subprocess.run(args, stdout=subprocess.PIPE, stderr=subprocess.PIPE, timeout=timeout)
    filename = re.search("-> (.*?) using filter", process.stdout.decode())

    if filename is None:
        raise LibreOfficeError(process.stdout.decode())
    else:
        return filename.group(1)


def convert_doc(output_path: str, source_filename: str) -> None:
    DOC_SAVE_PATH = f"./filled_docx/{os.path.basename(source_filename)}"
    convert_to_pdf(os.path.split(output_path)[0], DOC_SAVE_PATH)
    rename_pdf(output_path, source_filename)


class InputFileError(Exception):
    def __init__(self, output) -> None:
        self.output = output


def is_file(user_dict: dict) -> None:
    if not os.path.isfile(user_dict["input"]):
        raise InputFileError("Input field is not a file.")


class OutputPathError(Exception):
    def __init__(self, output):
        self.output = output


def is_path_defined(user_dict: dict):
    PATH = os.path.split(user_dict["output"])[0]

    if not os.path.isdir(PATH):
        raise OutputPathError("Path field is not defined.")


def output_exists(user_dict: dict):
    try:
        user_dict["output"]
    except KeyError as key_err:
        print("Output file is not given.")
        raise key_err


def input_exists(user_dict: dict):
    try:
        user_dict["input"]
    except KeyError as key_err:
        print("Input file is not given.")
        raise key_err


def empty_tmp_dir() -> None:
    TMP_PATH = "./filled_docx/"
    if len(os.listdir(TMP_PATH)) != 0:
        print("Temporary directory is not empty. Freeing it up...")
        shutil.rmtree(TMP_PATH)
        os.mkdir("./filled_docx")


def extract_files(user_dict: dict) -> None:
    with zipfile.ZipFile(user_dict["input"], "r") as zip_ref:
        zip_ref.extractall("./filled_docx/")


def get_xml_list() -> List[str]:
    return glob("./filled_docx/**/*.xml", recursive=True)


def fill_data(xml_list: List, user_data: dict) -> None:
    file_cont = []
    for xml_fn in xml_list:
        with open(xml_fn, "r") as f:
            file_cont = f.readlines()
            for i, _ in enumerate(file_cont):
                file_cont[i] = reduce(
                    lambda x, y: x.replace(f"&lt;{y}&gt;", str(user_data[y])), user_data, file_cont[i]
                )

        with open(xml_fn, "w") as wf:
            wf.writelines(file_cont)


def pack_docx(fn: str) -> None:
    shutil.make_archive(f"./filled_docx/{fn}", "zip", "./filled_docx/")
    os.rename(f"./filled_docx/{fn}.zip", f"./filled_docx/{fn}")


def process_docs(user_dict: dict):
    # Check if Libreoffice is installed
    libreoffice_exists()

    # Check if input and output fields are present in the payload
    input_exists(user_dict)
    output_exists(user_dict)

    # Check if output field is a file
    is_file(user_dict)

    # Check if output path is given
    is_path_defined(user_dict)

    print(f"\nConverting {user_dict['input']} ...")

    # Extract docx content
    empty_tmp_dir()
    extract_files(user_dict)

    # get docx xml list
    xml_list = get_xml_list()

    fill_data(xml_list, user_dict)

    # Pack files back to docx
    FILENAME = os.path.split(user_dict["input"])[1]
    pack_docx(FILENAME)

    # Convert docx to pdf
    OUTPUT_PATH = user_dict["output"] if user_dict["output"] != "" else "pdf_docs"
    INPUT_FILE = f"./filled_docx/{FILENAME}"
    convert_doc(OUTPUT_PATH, INPUT_FILE)

    print("-" * 80)
