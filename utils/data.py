from pathlib import Path

def saveDataOnFile(filename: str, data: list | set):
    try:
        file = open(filename, 'w')
        for item in data:
            file.write('{}\n'.format(item.replace("\n", "")))
        return True
    except Exception:
        return False

def readDataFromFile(filename: str):
    isFileExists = Path(filename).is_file()

    if isFileExists:
        file = open(filename, 'r')
        data = file.readlines()
        return set(data) if filename.startswith('BLACKLIST') else data

    return None
