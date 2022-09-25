starting_offset = int("0048A970", base=16)

def read_hex(path):
    with open(path,mode='rb') as f:
        hex_data = f.read().hex()
    return hex_data


def reverse_four_bytes(byte_reverse: str):
    reversed = byte_reverse[6:] + byte_reverse[4:6] + byte_reverse[2:4] + byte_reverse[0:2]
    return reversed


def reverse_two_bytes(byte_reverse: str):
    reversed = byte_reverse[2:] + byte_reverse[0:2]
    return reversed


def convert_gamevariable_to_reversed_hex(value: int, bytecount=1):
    output_prep = hex(value)
    output_prep = output_prep[2:]
    # 1 Byte
    if bytecount == 1:
        output_prep = output_prep.zfill(2)
        return output_prep
    # 2 Bytes
    if bytecount == 2:
        output_prep = output_prep.zfill(4)
        output_prep = output_prep[2:] + output_prep[0:2]
        return output_prep
    if bytecount == 3:
        output_prep = output_prep.zfill(6)
        output_prep = output_prep[4:] + output_prep[2:4] + output_prep[0:2]
        return output_prep
    if bytecount == 4:
        output_prep = output_prep.zfill(8)
        output_prep = output_prep[6:] + output_prep[4:6] + output_prep[2:4] + output_prep[0:2]
        return output_prep

# '''
# Calculate INTEGER offset of custom data.bin based on the offsets in the Suikoden V bin image
# '''
# def offset(offset_hex) -> int:
#     offset_as_integer = int(offset_hex, base=16)
#     return (offset_as_integer - starting_offset) * 2



# for i, skillname in enumerate(skill_name_list):
#     output = '"' + skillname[1] + '": equip_skill_list[' + str(i) + "],"
#     print(output)