def read_file(filename, skip_empty=True):
    with open(filename, "r") as file:
        while line := file.readline():
            line = line.replace("\n", "")
            if line or not skip_empty:
                yield line
