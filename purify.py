def get_file_word_data(filename, threshold):
    f = open(filename, "r")
    data = []
    for line in f.readlines():
        words = line.split()
        if (len(words)>threshold): data.append(words)
    return data

if __name__ == '__main__':
    print("This module does not produce any"
          " useful output. Use main.py")
