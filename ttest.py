import time
import matplotlib.pyplot as plt

def lzw_compress(uncompressed):
    dict_size = 256
    dictionary = {chr(i): i for i in range(dict_size)}
    current_string = ""
    compressed = []

    for symbol in uncompressed:
        new_string = current_string + symbol
        if new_string in dictionary:
            current_string = new_string
        else:
            compressed.append(dictionary[current_string])
            dictionary[new_string] = dict_size
            dict_size += 1
            current_string = symbol

    if current_string:
        compressed.append(dictionary[current_string])

    return compressed

def lzw_decompress(compressed):
    dict_size = 256
    dictionary = {i: chr(i) for i in range(dict_size)}
    current_code = compressed[0]
    current_string = dictionary[current_code]
    decompressed = current_string

    for code in compressed[1:]:
        if code in dictionary:
            entry = dictionary[code]
        elif code == dict_size:
            entry = current_string + current_string[0]
        else:
            raise ValueError("Invalid compressed code")

        decompressed += entry

        dictionary[dict_size] = current_string + entry[0]
        dict_size += 1

        current_string = entry

    return decompressed

if __name__ == "__main__":
    compression_times = []
    decompression_times = []
    lengths = []

    for length in range(1000, 9001, 2000):
        input_data = "abbvavbvva" * length

        start_time = time.time()
        compressed_data = lzw_compress(input_data)
        compression_time = time.time() - start_time
        compression_times.append(compression_time)

        start_time = time.time()
        decompressed_data = lzw_decompress(compressed_data)
        decompression_time = time.time() - start_time
        decompression_times.append(decompression_time)

        lengths.append(length)

        assert input_data == decompressed_data, "Error: Decompressed data does not match the original!"

    plt.figure(figsize=(12, 6))

    plt.subplot(1, 2, 1)
    plt.plot(lengths, compression_times, marker='o', color='blue')
    plt.title("Compression Time vs Input Length")
    plt.xlabel("Input Length")
    plt.ylabel("Compression Time (seconds)")
    plt.grid()

    plt.subplot(1, 2, 2)
    plt.plot(lengths, decompression_times, marker='o', color='green')
    plt.title("Decompression Time vs Compressed Codes Length")
    plt.xlabel("Compressed Codes Length")
    plt.ylabel("Decompression Time (seconds)")
    plt.grid()

    plt.tight_layout()
    plt.show()