import os
import hashlib
import argparse
from pathlib import Path
from rich.progress import Progress


DEFAULT_ALGORITHM = "sha1"
DEFAULT_BUFFER_SIZE = 4096


def list_available_algorithms() -> None:
    print("\nAvailable algorithms:\n=====================")
    for algorithm in hashlib.algorithms_available:
        print(f" - {algorithm}")
    print()    


def generate_checksum(filepath: Path, algorithm: str, buffer_size: int) -> None:
    file_sum = hashlib.new(algorithm)

    with Progress() as progress:
        task = progress.add_task(
            "[cyan]Calculating...",
            total=os.stat(filepath).st_size
        )
        
        while not progress.finished:
            with open(filepath, "rb") as file:
                while (buffer := file.read(buffer_size)):
                    file_sum.update(buffer)
                    progress.update(task, advance=len(buffer))
    
    return file_sum.hexdigest()


def output_result(name: Path, checksum: str) -> None:
    print(f"\x1b[1A\x1b[2K{checksum} : {name}")


def main(filepath: Path, algorithm: str, buffer_size: int) -> None:
    if algorithm not in hashlib.algorithms_available:
        raise NameError(f"invalid algorithm: {algorithm}")
    
    if not filepath.exists():
        raise FileNotFoundError(f"path does not exist: {filepath}")

    print(f"\nAlgorithm: {algorithm}\n")
    if filepath.is_file():
        checksum = generate_checksum(
            filepath,
            algorithm,
            buffer_size
        )
        
        output_result(filepath.name, checksum)

    elif filepath.is_dir():
        for sub in os.listdir(filepath):
            sub_path = Path(filepath, sub)
            if sub_path.is_file():
                checksum = generate_checksum(
                    sub_path,
                    algorithm,
                    buffer_size
                )
                
                output_result(Path(*sub_path.parts[-2:]), checksum)
    print()

if __name__ == "__main__":
    parser = argparse.ArgumentParser("checksum calculator", exit_on_error=False)
    
    parser.add_argument("filepath", type=str, help="paths to files or folders to checksum", nargs="?")
    parser.add_argument("-a", dest="algorithm", type=str, default=DEFAULT_ALGORITHM, help=f"hash algorithm, default: {DEFAULT_ALGORITHM}")
    parser.add_argument("-b", dest="buffersize", type=int, default=DEFAULT_BUFFER_SIZE,  help=f"buffer size, default: {DEFAULT_BUFFER_SIZE}")
    parser.add_argument("-l", dest="list_algorithms", action="store_true", help="list all available algorithms")
    
    args = parser.parse_args()
    
    if args.list_algorithms:
        list_available_algorithms()
    else:
        if args.filepath is None:
            parser.error("filepath was not provided")
        
        try:
            filepath = Path(args.filepath)
            algorithm = args.algorithm.lower()
            buffersize = args.buffersize
            
            main(filepath, algorithm, buffersize)
        
        except Exception as e:
            parser.error(e)