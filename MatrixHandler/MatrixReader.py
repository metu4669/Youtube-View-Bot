def txt_2_matrix(path):
    matrix = []
    matrix_available_1d = []
    with open(path, "r") as the_file:
        i = 0
        for line in the_file.readlines():
            line = line.strip()
            if not line:
                continue

            j = 0
            matrix.append(line.split(" "))
            for t in line.split(" "):
                if str(t) == "0":
                    matrix_available_1d.append(str(i)+"-"+str(j))
                j = j+1
            i = i+1

    return matrix, matrix_available_1d
