# Filename: PEanalysis.py
# Author: Ezra Fast
# Course: ITSC-203, Scripting for Tool Construction
# Details: This script is the solution for Lab 3b, problem 2, ITSC-203; It deals with PE file headers and sections programatically

from pefile import PE
import pefile
from struct import pack
from datetime import datetime
from prettytable import PrettyTable
import os

'''
Each file needs: (PEFile = PE(fileName))
    - File name
    - pehdrOffset   --> PEFile.DOS_HEADER.e_lfanew
    - PEsig         --> pack('<H', PEFile.NT_HEADERS.Signature)
    - Machine Type  --> PEFile.FILE_HEADER.Machine
    - Timestamp
        --> timestamp = PEFile.FILE_HEADER.TimeDateStamp
            timestamp = datetime.fromtimestamp(timestamp).strftime('%m/%d/%Y %H:%M:%S')     # datetime was not sufficiently covered.
            print(f'timestamp: {timestamp}')                  # time stamp from FILE header
    - Characteristics   --> PEFile.FILE_HEADER.Characteristics
    - OptMagic          --> PEFile.OPTIONAL_HEADER.Magic
    - ImageBase         --> PEFile.OPTIONAL_HEADER.ImageBase
    - EntryPoint        --> PEFile.OPTIONAL_HEADER.AddressOfEntryPoint
    - Subsystem         --> PEFile.OPTIONAL_HEADER.Subsystem
    - DLL/EXE           --> PEFile.is_exe()     /       PEFile.is_dll()
'''

'''
Values that require Dictionary Lookup:
    - machine Type
    - Characteristics
    - Optional Header Magic Value (OptMagic)
    - Subsystem
'''

def usageWarning():
    print('Usage: This program should be run in the directory that contains the directory to be analyzed (expandPE)')

# Dictionary Declarations:
machineTypeDict = {
    "0x0": "IMAGE_FILE_MACHINE_UNKNOWN",
    "0x184": "IMAGE_FILE_MACHINE_ALPHA",
    "0x284": "IMAGE_FILE_MACHINE_ALPHA64",
    "0x1d3": "IMAGE_FILE_MACHINE_AM33",
    "0x8664": "IMAGE_FILE_MACHINE_AMD64",
    "0x1c0": "IMAGE_FILE_MACHINE_ARM",
    "0xaa64": "IMAGE_FILE_MACHINE_ARM64",
    "0x1c4": "IMAGE_FILE_MACHINE_ARMNT",
    "0x284": "IMAGE_FILE_MACHINE_AXP64",
    "0xebc": "IMAGE_FILE_MACHINE_EBC",
    "0x14c": "IMAGE_FILE_MACHINE_I386",
    "0x200": "IMAGE_FILE_MACHINE_IA64",
    "0x6232": "IMAGE_FILE_MACHINE_LOONGARCH32",
    "0x6264": "IMAGE_FILE_MACHINE_LOONGARCH64",
    "0x9041": "IMAGE_FILE_MACHINE_M32R",
    "0x266": "IMAGE_FILE_MACHINE_MIPS16",
    "0x366": "IMAGE_FILE_MACHINE_MIPSFPU",
    "0x466": "IMAGE_FILE_MACHINE_MIPSFPU16",
    "0x1f0": "IMAGE_FILE_MACHINE_POWERPC",
    "0x1f1": "IMAGE_FILE_MACHINE_POWERPCFP",
    "0x166": "IMAGE_FILE_MACHINE_R4000",
    "0x5032": "IMAGE_FILE_MACHINE_RISCV32",
    "0x5064": "IMAGE_FILE_MACHINE_RISCV64",
    "0x5128": "IMAGE_FILE_MACHINE_RISCV128",
    "0x1a2": "IMAGE_FILE_MACHINE_SH3",
    "0x1a3": "IMAGE_FILE_MACHINE_SH3DSP",
    "0x1a6": "IMAGE_FILE_MACHINE_SH4",
    "0x1a8": "IMAGE_FILE_MACHINE_SH5",
    "0x1c2": "IMAGE_FILE_MACHINE_THUMB",
    "0x169": "IMAGE_FILE_MACHINE_WCEMIPSV2"
}

characteristicsDict = {
    0x0001: "IMAGE_FILE_RELOCS_STRIPPED",
    0x0002: "IMAGE_FILE_EXECUTABLE_IMAGE",
    0x0004: "IMAGE_FILE_LINE_NUMS_STRIPPED",
    0x0008: "IMAGE_FILE_LOCAL_SYMS_STRIPPED",
    0x0010: "IMAGE_FILE_AGGRESSIVE_WS_TRIM",
    0x0020: "IMAGE_FILE_LARGE_ADDRESS_AWARE",
    0x0040: "Reserved_1",
    0x0080: "IMAGE_FILE_BYTES_REVERSED_LO",
    0x0100: "IMAGE_FILE_32BIT_MACHINE",
    0x0200: "IMAGE_FILE_DEBUG_STRIPPED",
    0x0400: "IMAGE_FILE_REMOVABLE_RUN_FROM_SWAP",
    0x0800: "IMAGE_FILE_NET_RUN_FROM_SWAP",
    0x1000: "IMAGE_FILE_SYSTEM",
    0x2000: "IMAGE_FILE_DLL",
    0x4000: "IMAGE_FILE_UP_SYSTEM_ONLY",
    0x8000: "IMAGE_FILE_BYTES_REVERSED_HI"
}

optHeaderDict = {
    "0x10b": "PE32",
    "0x20b": "PE32+",
    "0x107": "ROM Image"
}

subsystemData = {
    0: "IMAGE_SUBSYSTEM_UNKNOWN",
    1: "IMAGE_SUBSYSTEM_NATIVE",
    2: "IMAGE_SUBSYSTEM_WINDOWS_GUI",
    3: "IMAGE_SUBSYSTEM_WINDOWS_CUI",
    5: "IMAGE_SUBSYSTEM_OS2_CUI",
    7: "IMAGE_SUBSYSTEM_POSIX_CUI",
    8: "IMAGE_SUBSYSTEM_NATIVE_WINDOWS",
    9: "IMAGE_SUBSYSTEM_WINDOWS_CE_GUI",
    10: "IMAGE_SUBSYSTEM_EFI_APPLICATION",
    11: "IMAGE_SUBSYSTEM_EFI_BOOT_SERVICE_DRIVER",
    12: "IMAGE_SUBSYSTEM_EFI_RUNTIME_DRIVER",
    13: "IMAGE_SUBSYSTEM_EFI_ROM",
    14: "IMAGE_SUBSYSTEM_XBOX",
    16: "IMAGE_SUBSYSTEM_WINDOWS_BOOT_APPLICATION",
}

usageWarning()

table = PrettyTable()
table.field_names = ["Filename", "PEHdrOff", "PESig", "Machine Type", "Timestamp", "Characteristics", "OptMagic", "ImageBase", "EntryPoint", "SubSystem", "DLL/EXE"]

dirName = 'expandPE'
precedingPath = os.getcwd()

listOfNeither = []

for fileName in os.listdir(dirName):
    characteristicsList = []
    try:
        PEFile = PE(f'{precedingPath}/{dirName}/{fileName}')
    except:
        listOfNeither.append(fileName)
        continue
    PEFile = PE(f'{dirName}/{fileName}')
    pehrOffset = PEFile.DOS_HEADER.e_lfanew
    PESig = pack('<H', PEFile.NT_HEADERS.Signature)
    machineType = machineTypeDict[hex(PEFile.FILE_HEADER.Machine)]  # dict lookup
    timeStamp = PEFile.FILE_HEADER.TimeDateStamp
    timeStamp = datetime.fromtimestamp(timeStamp).strftime('%m/%d/%Y %H:%M:%S')
    characteristics = hex(PEFile.FILE_HEADER.Characteristics)
    characteristicsList = [characteristicsDict[flagValue] for flagValue in characteristicsDict if int(hex(PEFile.FILE_HEADER.Characteristics), 16) & flagValue]
    OptMagic = optHeaderDict[hex(PEFile.OPTIONAL_HEADER.Magic)]     # dict lookup
    ImageBase = hex(PEFile.OPTIONAL_HEADER.ImageBase)
    EntryPoint = hex(PEFile.OPTIONAL_HEADER.AddressOfEntryPoint)
    Subsystem = subsystemData[PEFile.OPTIONAL_HEADER.Subsystem]
    DLLorEXE = ''
    if PEFile.is_exe() == True:
        DLLorEXE = 'EXE'
    elif PEFile.is_dll() == True:
        DLLorEXE = 'DLL'
    else:
        DLLorEXE = 'neither'# notice that this never shows up in output despite mismatches...file extensions can be deceiving
    
    table.add_row([fileName, pehrOffset, PESig, machineType, timeStamp, '\n'.join(characteristicsList), OptMagic, ImageBase, EntryPoint, Subsystem, DLLorEXE], divider=True)

print(table)

print('Non-PE files:', end=' ')
print(', '.join(listOfNeither))