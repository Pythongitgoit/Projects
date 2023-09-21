import os
import sys
import shutil
import gzip
import tarfile
from pathlib import Path


def main_sorting_function(main_directory):
    CYRILLIC_SYMBOLS = "абвгдеёжзийклмнопрстуфхцчшщъыьэюяєіїґ "
    TRANSLATION = (
        "a",
        "b",
        "v",
        "h",
        "d",
        "e",
        "e",
        "zh",
        "z",
        "y",
        "j",
        "k",
        "l",
        "m",
        "n",
        "o",
        "p",
        "r",
        "s",
        "t",
        "u",
        "f",
        "kh",
        "ts",
        "ch",
        "sh",
        "sch",
        "",
        "y",
        "",
        "e",
        "iu",
        "ia",
        "je",
        "i",
        "ji",
        "g",
        " ",
    )
    NUMBERS = "1234567890"

    TRANS = {}
    for cyrillic_symbol, translation in zip(CYRILLIC_SYMBOLS, TRANSLATION):
        TRANS[ord(cyrillic_symbol)] = translation
        TRANS[ord(cyrillic_symbol.upper())] = translation.upper()

    def normalize_file_name(file):
        base_name_without_extension = file.stem.translate(TRANS)
        for char in base_name_without_extension:
            if not ("a" <= char <= "z" or "A" <= char <= "Z" or char in NUMBERS):
                base_name_without_extension = base_name_without_extension.replace(
                    char, "_"
                )
        normalized_name = base_name_without_extension + file.suffix
        return normalized_name

    def create_directory(directory_name):
        directory_path = main_directory / directory_name
        return directory_path

    def move_file_to_directory(item, directory_name):
        destination_directory = create_directory(directory_name)
        if not destination_directory.exists():
            os.mkdir(destination_directory)
        destination_file = destination_directory / item.name
        if not destination_file.exists():
            shutil.move(item, destination_directory)
            return destination_file
        return None

    sorted_files_dict = {
        "images": [],
        "videos": [],
        "documents": [],
        "music": [],
        "archives": [],
        "unknown": [],
    }
    known_file_extensions = []
    unknown_file_extensions = []

    def sort_file(item, file_type):
        sorted_files_dict[file_type].append(item.name)
        if item.suffix not in known_file_extensions:
            known_file_extensions.append(item.suffix)

    def sort_files(folder_path):
        for item in folder_path.iterdir():
            if item.is_dir():
                sort_files(item)
            elif item.is_file():
                file_extension = item.suffix.removeprefix(".").upper()
                if file_extension in ["JPEG", "PNG", "JPG", "SVG", "WEBP"]:
                    file_type = "images"
                elif file_extension in ["AVI", "MP4", "MOV", "MKV"]:
                    file_type = "videos"
                elif file_extension in [
                    "DOC",
                    "DOCX",
                    "TXT",
                    "PDF",
                    "XLS",
                    "XLSX",
                    "PPTX",
                    "XML",
                ]:
                    file_type = "documents"
                elif file_extension in ["MP3", "OGG", "WAV", "AMR", "M4A"]:
                    file_type = "music"
                elif file_extension in ["ZIP", "GZ", "TAR"]:
                    file_type = "archives"
                else:
                    file_type = "unknown"

                destination_file = move_file_to_directory(item, file_type)
                if destination_file:
                    sort_file(destination_file, file_type)
                else:
                    os.remove(item)

    sort_files(main_directory)

    if (main_directory / "archives").is_dir():

        def extract_archives(folder_path):
            archives_folder = folder_path / "archives"
            for archive_file in archives_folder.iterdir():
                if archive_file.is_file():
                    output_folder = archive_file.with_suffix("")
                    if archive_file.suffix == ".gz":
                        with gzip.open(archive_file, "rb") as gz_file:
                            with tarfile.open(fileobj=gz_file, mode="r") as tar:
                                tar.extractall(path=output_folder)
                    elif archive_file.suffix == ".tar":
                        with tarfile.open(archive_file, "r") as tar:
                            tar.extractall(path=output_folder)
                    elif archive_file.suffix == ".zip":
                        shutil.unpack_archive(str(archive_file), str(output_folder))

        extract_archives(main_directory)

        def delete_archives(folder_path):
            for archive_file in folder_path.iterdir():
                if archive_file.is_file():
                    os.remove(archive_file)

        delete_archives(create_directory("archives"))

        def rename_files_in_archives(folder_path):
            for archive_file in folder_path.iterdir():
                if archive_file.is_dir():
                    rename_files_in_archives(archive_file)
                else:
                    try:
                        os.rename(
                            archive_file,
                            folder_path / normalize_file_name(archive_file),
                        )
                    except Exception:
                        os.remove(archive_file)

        rename_files_in_archives(main_directory / "archives")

    def rename_files(folder_path):
        for folder in folder_path.iterdir():
            if folder.name in ["images", "videos", "documents", "music"]:
                for item in folder.iterdir():
                    try:
                        os.rename(item, folder / normalize_file_name(item))
                    except Exception:
                        if item.is_dir():
                            shutil.rmtree(item)
                        else:
                            os.remove(item)

    rename_files(main_directory)

    def delete_empty_directories(directory_path):
        for item in directory_path.iterdir():
            if item.is_dir():
                delete_empty_directories(item)
                if not list(item.iterdir()):
                    item.rmdir()

    delete_empty_directories(main_directory)


try:
    main_sorting_function(Path(sys.argv[1]))
except IndexError:
    print("Вкажіть шлях до папки із файлами!")