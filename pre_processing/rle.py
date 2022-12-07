def rle_e(s):
    encoded_string = ""
    i = 0
    while i <= len(s) - 1:
        count = 1
        ch = s[i]
        j = i
        while j < len(s) - 1:
            if s[j] == s[j + 1]:
                count = count + 1
                j = j + 1
            else:
                break
        encoded_string = encoded_string + str(count) + ch
        i = j + 1
    return encoded_string


def decode_message(sq):
    decoded_message = ""
    i = 0
    j = 0
    while i <= len(sq) - 1:
        run_count = int(sq[i])
        run_word = sq[i + 1]
        for j in range(run_count):
            decoded_message = decoded_message + run_word
            j = j + 1
        i = i + 2
    return decoded_message
