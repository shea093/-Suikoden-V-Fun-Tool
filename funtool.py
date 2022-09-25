"""
First statement
"""
import copy

from services import *
import codecs
import numpy
import random
import hashlib
from copy import deepcopy


'''
Initialization Variables
'''
starting_offset = int("0048A970", base=16)
skill_name_path = "Data/equip_skill_names.txt"
test = ""




######################################################
#Initialization Functions
######################################################

'''
Get the offsets of characters from txt file
'''
def get_character_stat_offsets():
    name_list = []
    with open("Data/character_stat_offsets.txt", "r") as f:
        for line in f.readlines():
            line_split = line.split(sep="-")
            name_list.append([line_split[0].strip(), line_split[1].strip()])
    return name_list

def get_rune_affinity_offsets():
    rune_affinity_list = []
    with open("Data/rune_affinity_offsets.txt", "r") as f:
        for line in f.readlines():
            line_split = line.split(sep="-")
            rune_affinity_list.append([line_split[0].strip(), line_split[1].strip()])
    return rune_affinity_list

def get_monster_offsets():
    monster_offset_list = []
    with open("Data/monster_offsets.txt", "r") as f:
        for line in f.readlines():
            offset = line[0:8]
            mon_name = line[9:].strip()
            monster_offset_list.append([offset, mon_name])
    return monster_offset_list


def get_skill_names():
    skill_name_list = []
    with open(skill_name_path,'r') as f:
        for line in f.readlines():
            line_split = line.split(sep=":")
            skill_name_list.append([line_split[0].strip(), line_split[1].strip()])
    return skill_name_list

def get_equip_skill_offsets():
    equip_skill_offset_list = []
    with open("Data/equip_skill_offsets.txt", "r") as f:
        for line in f.readlines():
            line_split = line.split(sep="-")
            equip_skill_offset_list.append([line_split[0].strip(), line_split[1].strip()])
    return equip_skill_offset_list


######################################################
######################################################




'''
File paths
'''
data_bin_path = "Data/data.bin"


'''
Global data
'''
character_offset_list = get_character_stat_offsets()
data_bin_hex = read_hex(data_bin_path)
data_bin_hex_output = copy.deepcopy(data_bin_hex)
rune_affinity_offset_list = get_rune_affinity_offsets()
equip_skill_offset_list = get_equip_skill_offsets()
skill_name_list = get_skill_names()
monster_offsets_and_names = get_monster_offsets()
global_stats_names = ["HP", "ATK", "TECH", "MAG", "EVA", "PDF", "MDF", "SPD",
                   "LUK"]
global_growth_names = ["HP GROWTH", "ATK GROWTH", "TECH GROWTH", "MAG GROWTH", "EVA GROWTH",
                    "PDF GROWTH", "MDF GROWTH", "SPD GROWTH", "LUK GROWTH"]
rune_affinity_names = ["Sun", "Fire", "Lightning", "Wind",
                                "Water", "Earth", "Star", "Sound",
                                "Holy", "Dark", "Slash", "Thrust",
                                "Punch", "Shot"]

######################################################
# HELPER FUNCTIONS
######################################################


'''
Calculate INTEGER offset of custom data.bin based on the offsets in the Suikoden V bin image
'''
def offset(offset_hex) -> int:
    offset_as_integer = int(offset_hex, base=16)
    return (offset_as_integer - starting_offset) * 2


def get_data_chunk(offset_input, bytes):
    return data_bin_hex[offset(offset_input):offset(offset_input)+(bytes*2)]


def initialize_hex_list(data_list, byte_each, type="Generic"):
    hex_list_return = []
    for data_inp in data_list:
        if type == "Generic":
            hex_chunk = get_data_chunk(data_inp[1],int(byte_each,base=16))
            hex_list_return.append([data_inp[0],hex_chunk])
        if type == "Monsters":
            hex_chunk = get_data_chunk(data_inp[0], int(byte_each, base=16))
            hex_list_return.append([data_inp[1], hex_chunk])
    return hex_list_return

def translate_rune_affinity(affinity_hex, reverse = False):
    if reverse == False:
        if affinity_hex == "01":
            return "E"
        elif affinity_hex == "02":
            return "D"
        elif affinity_hex == "03":
            return "C"
        elif affinity_hex == "04":
            return "B"
        elif affinity_hex == "05":
            return "A"
        elif affinity_hex == "06":
            return "S"
        elif affinity_hex == "07":
            return "SS"
        elif affinity_hex == "00":
            return "None"
    elif reverse == True:
        if affinity_hex == "E":
            return "01"
        elif affinity_hex == "D":
            return "02"
        elif affinity_hex == "C":
            return "03"
        elif affinity_hex == "B":
            return "04"
        elif affinity_hex == "A":
            return "05"
        elif affinity_hex == "S":
            return "06"
        elif affinity_hex == "SS":
            return "07"
        elif affinity_hex == "None":
            return "00"

######################################################
######################################################



######################################################
# COMPREHENSIVE DATA
######################################################

class Character:

    def __init__(self, name_input, start_offset):
        self.char_name = codecs.encode(name_input, 'rot_13')
        self.__real_char_name = name_input
        self.battle_char = False
        self.start_stat_offset = start_offset
        self.start_rune_affinity_offset = None
        self.start_skill_equip_offset = None
        self.start_stats = {"HP","ATK","TECH","MAG","EVA","PDF","MDF","SPD","LUK"} # type: dict
        self.growths = {"HP GROWTH","ATK GROWTH","TECH GROWTH","MAG GROWTH","EVA GROWTH",
                        "PDF GROWTH","MDF GROWTH","SPD GROWTH","LUK GROWTH"} # type: dict
        # self.rune_affinities = {"Sun": "E", "Fire": "E", "Lightning": "E", "Wind": "E",
        #                         "Water": "E", "Earth": "E", "Star": "E", "Sound": "E",
        #                         "Holy": "E", "Dark": "E", "Slash": "E", "Thrust": "E",
        #                         "Punch": "E", "Shot": "E"}
        self.rune_affinities = {}
        self.equip_skills = {}

    def output_stat_and_growths_hex(self):
        hex_output = ""
        for stat_name in global_stats_names:
            hex_output = hex_output + convert_gamevariable_to_reversed_hex(self.start_stats[stat_name])
        for growth_name in global_growth_names:
            hex_output = hex_output + convert_gamevariable_to_reversed_hex(self.growths[growth_name])
        return hex_output

    def output_rune_affinity_hex(self):
        hex_output = ""
        for rune_name in rune_affinity_names:
            hex_output = hex_output + translate_rune_affinity(self.rune_affinities[rune_name],reverse=True)
        return hex_output

    def output_skill_equip_hex(self):
        hex_output = ""
        elf_names = ["ReMiFa", "MiFaSo", "FaSoLa", "SoLaTi", "LaTiDo"]
        for skill_name in skill_name_list:
            skill_name_look = skill_name[1]
            if self.__real_char_name in elf_names:
                return "Elf!"
            hex_output = hex_output + translate_rune_affinity(self.equip_skills[skill_name_look],reverse=True)
        return hex_output


    def initialize_stats(self, stat_list):
        self.start_stats = {
            "HP": stat_list[0],
            "ATK": stat_list[1],
            "TECH": stat_list[2],
            "MAG": stat_list[3],
            "EVA": stat_list[4],
            "PDF": stat_list[5],
            "MDF": stat_list[6],
            "SPD": stat_list[7],
            "LUK": stat_list[8]
        }

        self.growths = {
            "HP GROWTH": stat_list[9],
            "ATK GROWTH": stat_list[10],
            "TECH GROWTH": stat_list[11],
            "MAG GROWTH": stat_list[12],
            "EVA GROWTH": stat_list[13],
            "PDF GROWTH": stat_list[14],
            "MDF GROWTH": stat_list[15],
            "SPD GROWTH": stat_list[16],
            "LUK GROWTH": stat_list[17],
        }
        if (self.start_stats["ATK"] + self.start_stats["MAG"]) > 1:
            self.battle_char = True

    def initialize_rune_affinities(self, affinity_list):
        self.rune_affinities = {
            "Sun": affinity_list[0],
            "Fire": affinity_list[1],
            "Lightning": affinity_list[2],
            "Wind": affinity_list[3],
            "Water": affinity_list[4],
            "Earth": affinity_list[5],
            "Star": affinity_list[6],
            "Sound": affinity_list[7],
            "Holy": affinity_list[8],
            "Dark": affinity_list[9],
            "Slash": affinity_list[10],
            "Thrust": affinity_list[11],
            "Punch": affinity_list[12],
            "Shot": affinity_list[13]
        }

    def initialize_equip_skills(self, equip_skill_list):
        self.equip_skills = {
            "Stamina": equip_skill_list[0],
            "Attack": equip_skill_list[1],
            "Defense": equip_skill_list[2],
            "Technique": equip_skill_list[3],
            "Vitality": equip_skill_list[4],
            "Agility": equip_skill_list[5],
            "Magic": equip_skill_list[6],
            "Magic Defense": equip_skill_list[7],
            "Incantation": equip_skill_list[8],
            "Sword Magic": equip_skill_list[9],
            "Raging Lion": equip_skill_list[10],
            "Fate Control": equip_skill_list[11],
            "Karmic Effect": equip_skill_list[12],
            "Armor of Gods": equip_skill_list[13],
            "Swift Foot": equip_skill_list[14],
            "Triple Harmony": equip_skill_list[15],
            "All-out Strike": equip_skill_list[16],
            "Untold Clarity": equip_skill_list[17],
            "Divine Right": equip_skill_list[18],
            "Zen Sword": equip_skill_list[19],
            "Sacred Oath": equip_skill_list[20],
            "Royal Paradise": equip_skill_list[21],
            "Thief": equip_skill_list[22],
            "Mow Down": equip_skill_list[23],
            "Pierce": equip_skill_list[24],
            "Freeze": equip_skill_list[25],
            "???????": equip_skill_list[26],
            "Barrage": equip_skill_list[27],
            "Long Throw": equip_skill_list[28],
            "Dragon Special": equip_skill_list[29],
            "Forge": equip_skill_list[30],
            "Combat Teacher": equip_skill_list[31],
            "Chain Magic": equip_skill_list[32],
            "Analyze": equip_skill_list[33],
            "Potch Finder": equip_skill_list[34],
            "Treasure Hunt": equip_skill_list[35],
            "Escape Route": equip_skill_list[36],
            "Healing": equip_skill_list[37],
            "Treatment": equip_skill_list[38],
            "Haggle": equip_skill_list[39],
            "Trade In": equip_skill_list[40],
            "Cook": equip_skill_list[41],
            "Rune Sage": equip_skill_list[42],
            "Bard": equip_skill_list[43],
            "Perfect Pitch": equip_skill_list[44],
            "Appraisal": equip_skill_list[45],
            "Bath": equip_skill_list[46],
            "Tutor": equip_skill_list[47]
        }

class Monster:
    def __init__(self, name_input, start_offset):
        self.mon_name = codecs.encode(name_input, 'rot_13')
        self.__real_mon_name = name_input
        self.start_offset = start_offset
        self.start_stat_offset = str("00" + hex(((int(start_offset,16))) + 3)[2:]).upper()
        test
        self.mon_stats = {}

    def initialize_stats(self, stat_list):
        self.mon_stats = {
            "HP": stat_list[0],
            "ATK": stat_list[1],
            "TECH": stat_list[2],
            "ACC": stat_list[3],
            "MAG": stat_list[4],
            "EVA": stat_list[5],
            "PDF": stat_list[6],
            "MDF": stat_list[7],
            "SPD": stat_list[8],
            "LUK": stat_list[9]
        }

    def output_stat_hex(self):
        hex_output = ""
        monster_stat_names = [
            "HP","ATK",
        "TECH",
        "ACC",
        "MAG",
        "EVA",
        "PDF",
        "MDF",
        "SPD",
        "LUK"
        ]
        for stat_name in monster_stat_names:
            hex_output = hex_output + convert_gamevariable_to_reversed_hex(self.mon_stats[stat_name],2)
        return hex_output




'''
Initialization of object lists
'''

characters = []
for c in character_offset_list:
    characters.append(Character(c[0],c[1]))

character_index = {}
for i in range (0,len(characters)):
    character_index[character_offset_list[i][0]] = i

for r in rune_affinity_offset_list:
    for c in character_index:
        if r[0] == c:
            characters[character_index[c]].start_rune_affinity_offset = r[1]

for s in equip_skill_offset_list:
    for c in character_index:
        if s[0] == c:
            characters[character_index[c]].start_skill_equip_offset = s[1]

monsters = []
for m in monster_offsets_and_names:
    monsters.append(Monster(m[1],m[0]))

def initialize_c_character_stats(character_object_list):
    character_stat_chunks = initialize_hex_list(character_offset_list,"12")
    rune_affinity_chunks = initialize_hex_list(rune_affinity_offset_list,"0E")
    equip_skill_chunks = initialize_hex_list(equip_skill_offset_list,"31")
    #ORDER
    #HP - ATK - TECH - MAG - EVA - PDF - MDF - SPD - LUK
    for ind, data in enumerate(character_stat_chunks):
        n = 2
        split_data = [int(data[1][i:i+n],base=16) for i in range(0, len(data[1]), n)]
        character_object_list[ind].initialize_stats(split_data)
    for data in rune_affinity_chunks:
        n = 2
        split_data = [translate_rune_affinity(data[1][i:i+n]) for i in range(0, len(data[1]), n)]
        character_object_list[character_index[data[0]]].initialize_rune_affinities(split_data)
    for data in equip_skill_chunks:
        n = 2
        split_data = [translate_rune_affinity(data[1][i:i + n]) for i in range(0, len(data[1]), n)]
        test
        character_object_list[character_index[data[0]]].initialize_equip_skills(split_data)
    return character_object_list

def initialize_monster_stats(monster_object_list):
    monster_chunks = initialize_hex_list(monster_offsets_and_names,"7C",type="Monsters")
    for ind, data in enumerate(monster_chunks):
        n = 4
        split_data = [int(reverse_two_bytes(data[1][i:i+n]),base=16) for i in range(6,46,n)]
        monster_object_list[ind].initialize_stats(split_data)
    test



c_character_stats = initialize_c_character_stats(characters)
monster_stats = initialize_monster_stats(monsters)

######################################################
######################################################



'''
Get statistics of character stats
'''
def character_stat_statistics():
    averages = {}
    mins = {}
    maxs = {}
    percentile_75 = {}
    percentile_20 = {}
    stats_names = ["HP", "ATK", "TECH", "MAG", "EVA", "PDF", "MDF", "SPD",
                   "LUK"]
    growth_names = ["HP GROWTH", "ATK GROWTH", "TECH GROWTH", "MAG GROWTH", "EVA GROWTH",
                    "PDF GROWTH", "MDF GROWTH", "SPD GROWTH", "LUK GROWTH"]
    battle_char_num = 0
    for stat_name in stats_names:
        averages[stat_name] = 0
        mins[stat_name] = 9999
        maxs[stat_name] = 0
        percentile_75[stat_name] = []
        percentile_20[stat_name] = []
    for growth_name in growth_names:
        averages[growth_name] = 0
        mins[growth_name] = 9999
        maxs[growth_name] = 0
        percentile_75[growth_name] = []
        percentile_20[growth_name] = []
    for character in characters:
        if character.battle_char == False:
            pass
        else:
            battle_char_num = battle_char_num + 1
            for stat_name in stats_names:
                averages[stat_name] = averages[stat_name] + character.start_stats[stat_name]
                if character.start_stats[stat_name] > maxs[stat_name]:
                    maxs[stat_name] = character.start_stats[stat_name]
                if character.start_stats[stat_name] < mins[stat_name]:
                    mins[stat_name] = character.start_stats[stat_name]
                percentile_75[stat_name].append(character.start_stats[stat_name])
            for growth_name in growth_names:
                averages[growth_name] = averages[growth_name] + character.growths[growth_name]
                if character.growths[growth_name] > maxs[growth_name]:
                    maxs[growth_name] = character.growths[growth_name]
                if character.growths[growth_name] < mins[growth_name]:
                    mins[growth_name] = character.growths[growth_name]
                percentile_75[growth_name].append(character.growths[growth_name])
    for key, value in averages.items():
        new_value = value / battle_char_num
        averages[key] = new_value
    for key,value in percentile_75.items():
        percentile_75[key] = numpy.percentile(value,75)
        percentile_20[key] = numpy.percentile(value,20)
    return {"Averages": averages,"Mins": mins,"Maxs": maxs,"percentile_75": percentile_75,"percentile_20": percentile_20}

statistic_details = character_stat_statistics()


'''
Caps stats to 75th percentile 
'''
def cap_character_stats(character_list: list[Character]):
    for character in character_list:
        if character.battle_char == True:
            for stat_n in global_stats_names:
                if character.start_stats[stat_n] > statistic_details["percentile_75"][stat_n]:
                    print(str(character.start_stats[stat_n]) + " " + stat_n + " " + codecs.decode(character.char_name, 'rot_13'))
                    character.start_stats[stat_n] = int(statistic_details["percentile_75"][stat_n])
            for growth_n in global_growth_names:
                if character.growths[growth_n] > statistic_details["percentile_75"][growth_n]:
                    print(str(character.growths[growth_n]) + " " + growth_n + " " + codecs.decode(character.char_name,
                                                                                                  'rot_13'))
                    character.growths[growth_n] = int(statistic_details["percentile_75"][growth_n])
    return character_list

'''
HARD MODE FOR MONSTERS USING MULTIPLIERS
'''

class HardMode:
    def __init__(self, mon_list: list[Monster], seed = None):
        self.mon_list = mon_list # type: list[Monster]
        self.seed = seed

    def multiply_stat(self, stat_name: str, multiplier):
        for mon in self.mon_list:
            mon.mon_stats[stat_name] = int(mon.mon_stats[stat_name] * multiplier)




'''
RANDOMIZE
'''

class Randomizer:
    def __init__(self, char_list: list[Character], seed: int):
        self.char_list = char_list # type: list[Character]
        self.seed = seed #type: int

    def call_seed(self) -> int:
        a = int(hashlib.md5(str(self.seed).encode('utf-8')).hexdigest(), 16)
        increment = random.Random(a).randint(1,10000)
        self.seed = int((self.seed + increment))
        return self.seed

    def roll_100(self) -> int:
        roll = random.Random(self.call_seed()).randint(1,100)
        return roll

    def randomize_stats(self):
        for char in self.char_list:
            if char.battle_char == True:
                for stat_name in global_stats_names:
                    min_stat = statistic_details["Mins"][stat_name]
                    max_stat = statistic_details["percentile_75"][stat_name]
                    rand_stat = random.Random(self.call_seed()).randint(int(min_stat),int(max_stat))
                    char.start_stats[stat_name] = rand_stat
                for growth_name in global_growth_names:
                    min_gr = statistic_details["Mins"][growth_name]
                    max_gr = statistic_details["percentile_75"][growth_name]
                    rand_gr = random.Random(self.call_seed()).randint(int(min_gr), int(max_gr))
                    char.growths[growth_name] = rand_gr

    def randomize_affinities(self):
        for char in self.char_list:
            if char.battle_char == True:
                for affinity_name in rune_affinity_names:
                    affinity_chance = self.roll_100()
                    if affinity_chance > 92:
                        char.rune_affinities[affinity_name] = "A"
                    elif affinity_chance <= 92 and affinity_chance > 79:
                        char.rune_affinities[affinity_name] = "B"
                    elif affinity_chance <= 70 and affinity_chance > 40:
                        char.rune_affinities[affinity_name] = "C"
                    elif affinity_chance <= 40 and affinity_chance > 13:
                        char.rune_affinities[affinity_name] = "D"
                    elif affinity_chance <= 13 and affinity_chance >= 1:
                        char.rune_affinities[affinity_name] = "E"
                    else:
                        char.rune_affinities[affinity_name] = "E"

    def randomize_equip_skills(self):
        editable_skills = skill_name_list[0:21]
        for char in self.char_list:
            if char.battle_char == True:
                for e_skill_name in editable_skills:
                    skill_name = e_skill_name[1]
                    e_skill_chance = self.roll_100()
                    if e_skill_chance > 96:
                        char.equip_skills[skill_name] = "SS"
                    elif e_skill_chance > 88:
                        char.equip_skills[skill_name] = "S"
                    elif e_skill_chance > 76:
                        char.equip_skills[skill_name] = "A"
                    elif e_skill_chance > 61:
                        char.equip_skills[skill_name] = "B"
                    elif e_skill_chance > 26:
                        char.equip_skills[skill_name] = "C"
                    elif e_skill_chance > 11:
                        char.equip_skills[skill_name] = "D"
                    elif e_skill_chance >= 1:
                        char.equip_skills[skill_name] = "E"
                    else:
                        char.equip_skills[skill_name] = "E"

def replace_chunk (start_offset,hex_chunk, output_hex_object: str):
    output_hex_object = output_hex_object[0:offset(start_offset)] \
                          + hex_chunk + output_hex_object[offset(start_offset)+len(hex_chunk):len(output_hex_object)]
    return output_hex_object

def replace_character_bin (randomizer_object: Randomizer, output_hex_object: str):
    for char in randomizer_object.char_list:
        if char.battle_char == True:
            #stats and growths
            output_hex_object = replace_chunk(char.start_stat_offset,char.output_stat_and_growths_hex(),output_hex_object)
            #rune affinities
            output_hex_object = replace_chunk(char.start_rune_affinity_offset,char.output_rune_affinity_hex(),output_hex_object)
            #equip skills
            if char.output_skill_equip_hex() == "Elf!":
                pass
            else:
                output_hex_object = replace_chunk(char.start_skill_equip_offset,char.output_skill_equip_hex(),output_hex_object)
    return output_hex_object

def replace_monster_bin (hard_mode_object: HardMode, output_hex_object: str):
    for mon in hard_mode_object.mon_list:
        output_hex_object = replace_chunk(mon.start_stat_offset,mon.output_stat_hex(),output_hex_object)
    return output_hex_object


characters = cap_character_stats(characters)
# seed = 461793
seed = 461793
rand_chars = copy.deepcopy(characters)
hardm_mons = copy.deepcopy(monsters)
randomizer_obj = Randomizer(rand_chars,seed)
randomizer_obj.randomize_stats()
randomizer_obj.randomize_affinities()
randomizer_obj.randomize_equip_skills()
hardmode_obj = HardMode(hardm_mons)
hardmode_obj.multiply_stat("ATK",1.6)
hardmode_obj.multiply_stat("TECH",1.6)
hardmode_obj.multiply_stat("ACC",1.3)
hardmode_obj.multiply_stat("EVA",1.2)
hardmode_obj.multiply_stat("LUK",1.3)
hardmode_obj.multiply_stat("SPD",1.2)
hardmode_obj.multiply_stat("HP",1.4)
data_bin_hex_output = replace_character_bin(randomizer_obj,data_bin_hex_output)
data_bin_hex_output = replace_monster_bin(hardmode_obj,data_bin_hex_output)
test






