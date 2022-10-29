def ip_checksum(data):  # Checksum func
    pos = len(data)
    if pos & 1:  # -> In case odd
        pos -= 1
        sum = ord(data[pos])  
    else:
        sum = 0

    while pos > 0: # Summing the values
        pos -= 2
        sum += (ord(data[pos + 1]) << 8) + ord(data[pos])

    sum = (sum >> 16) + (sum & 0xffff)
    sum += (sum >> 16)

    result = (~ sum) & 0xffff  # 16bits 
    result = result >> 8 | ((result & 0xff) << 8)  # Invert the bytes
    return chr(result / 256) + chr(result % 256)