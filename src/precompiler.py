from sys import argv, exit
from os import path

ALLOWED_TYPES = (
    'char',
    'int8_t',
    'uint8_t',
    'int16_t',
    'uint16_t',
    'int32_t',
    'uint32_t',
    'float',
    'double'
)

# Allow char* too!

class Struct:
    def __init__(self, name=None):
        self.name = name
        self.attrs = []
    
    def __str__(self):
        return "Struct" + str((self.name, self.attrs))

    def is_valid(self):
        # check if attributes are valid

        # simple check
        for attr in self.attrs:
            if attr.split(' ')[0] not in ALLOWED_TYPES:
                return False
        return True

def usage():
    print("Usage: {0} path".format(argv[0]))
    exit(1)

def perror(msg):
    print("[ERROR] %s" %msg)

def print_allowed_types():
    print("ALLOWED_TYPES:")
    for allowed_type in ALLOWED_TYPES:
        print("  %s" %allowed_type)

def write_header(filename, structs):
    f = open(filename + '_serializers.h', 'w')
    f.write('#ifndef %s_SERIALIZERS_H\n' %filename.upper())
    f.write('#define %s_SERIALIZERS_H\n' %filename.upper())
    f.write('\n')
    f.write('#include <buffer.h>\n')
    f.write('\n')

    for struct in structs:
        f.write('int %s_serialize(const struct %s*, char *dst, int size);\n'\
            %(struct.name, struct.name))
        f.write('int %s_deserialize(const char *src, int size, struct %s*);\n'\
            %(struct.name, struct.name))
        f.write('\n')
    
    f.write('#endif\n')
    f.close()

def write_source(filename, structs):
    f = open(filename + '_serializers.c', 'w')
    f.write('#include "%s.h"' %(filename + '_serializers'))
    f.write('\n')

    for struct in structs:
        f.write('int %s_serialize(const struct %s *s, char *dst, int size)\n'\
            %(struct.name, struct.name))
        f.write('{\n')
        f.write('\tauto_buffer_t b = buffer_create_default();')


    f.close()


# TODO: Nested struct support
def process(data):
    SEEK = 0
    SEEK_EX = '//!serialize\n'

    PARSE_NAME = 1
    # TODO: Support typedef
    PARSE_NAME_EX = 'struct'
    sname = ''

    PARSE_ATTRS_PRELUDE = 2
    PARSE_ATTRS = 3
    PARSE_ATTRS_BCOUNT = 0 # { adds, } subs
    attr = ''

    ex = 0
    state = SEEK

    structs = []
    struct = None

    for c in data:
        if state == SEEK:
            if c == ' ':
                continue # skip
            if c == SEEK_EX[ex]:
                ex += 1
            elif ex > 0:
                ex = 0 # reset
            if ex == len(SEEK_EX):
                state = PARSE_NAME
                ex = 0
        
        elif state == PARSE_NAME:
            if ex == len(PARSE_NAME_EX):
                if not c.isspace():
                    ex = -1
                    name = c
                continue
            elif ex == -1:
                if c.isspace():
                    struct = Struct(name)
                    state = PARSE_ATTRS_PRELUDE
                else:
                    name += c
                continue
                    
            if c.isspace():
                continue # skip
            if c == PARSE_NAME_EX[ex]:
                ex += 1
            elif ex > 0:
                state = SEEK
                ex = 0

        elif state == PARSE_ATTRS_PRELUDE:
            if c.isspace():
                continue # skip
            elif c == '{':
                state = PARSE_ATTRS
                PARSE_ATTRS_BCOUNT = 1
            else:
                # not expected
                state = SEEK
                ex = 0
        
        elif state == PARSE_ATTRS:
            if c == '{':
                PARSE_ATTRS_BCOUNT += 1
            elif c == '}':
                PARSE_ATTRS_BCOUNT -= 1
                
                if PARSE_ATTRS_BCOUNT == 0:
                    structs.append(struct)
                    state = SEEK
                    ex = 0
            elif c == ';':
                struct.attrs.append(attr.strip())
                attr = ''
            else:
                attr += c

    invalid = [struct for struct in structs if not struct.is_valid()]
    if invalid:
        for struct in invalid:
            perror('Struct "{0}" has unsopported attribute types'
                .format(struct.name))
        print('')
        print_allowed_types()
        exit(1)

    return structs
        

def main():
    if len(argv) != 2:
        usage()
    
    filename = argv[1]

    with open(filename) as f:
        structs = process(f.read())
        write_header(path
            .split(filename)[1]
            .split('.')[0], structs)
        write_source(path
            .split(filename)[1]
            .split('.')[0], structs)


if __name__ == '__main__':
    main()