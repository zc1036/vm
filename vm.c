
#include <stdio.h>
#include <stdint.h>
#include <stdlib.h>

#define require(X)                                  \
    if (!(X)) {                                     \
        fprintf(stderr, "Assertion " #X " failed on line %d\n", __LINE__); \
        exit(1);                                    \
    }

typedef enum OPCODES
{
    OP_ADD            = 1,
    OP_SUB            = 2,
    OP_DIV            = 3,
    OP_MUL            = 4,
    OP_BIT_AND        = 5,
    OP_BIT_OR         = 6,
    OP_FADD           = 7,
    OP_FSUB           = 8,
    OP_FDIV           = 9,
    OP_FMUL           = 0xA,
    OP_LOAD_BYTE      = 0xB,
    OP_LOAD_2BYTE     = 0xC,
    OP_LOAD_4BYTE     = 0xD,
    OP_LOAD_WORD      = 0xE,
    OP_LOAD_SLIMM     = 0xF,
    OP_LOAD_ULIMM     = 0x10,
    OP_OR_UUIMM       = 0x11,
    OP_STORE_BYTE     = 0x12,
    OP_STORE_2BYTE    = 0x13,
    OP_STORE_4BYTE    = 0x14,
    OP_STORE_WORD     = 0x15,
    OP_REGCALL        = 0x16,
    OP_RELCALL        = 0x17,
    OP_RELJUMP_IF0    = 0x19,
    OP_RELJUMP_IFLT0  = 0x1A,
    OP_RELJUMP_IFGT0  = 0x1B,
    OP_RELJUMP_IFLTE0 = 0x1C,
    OP_RELJUMP_IFGTE0 = 0x1D,
    OP_SYSCALL        = 0x1F
} OPCODES;

typedef struct vmstate {
    size_t registers[256];
    double fregisters[128];
    size_t memory_size;
    uint8_t* memory;
} vmstate;

typedef uint32_t inst_t;
typedef size_t addr_t;

typedef struct {
    addr_t untrusted_addr;
} untrusted_addr;

addr_t check_addr(const untrusted_addr ptr, const vmstate* const vm, const size_t size) {
    require(size <= vm->memory_size);
    require(ptr.untrusted_addr <= vm->memory_size - size);
    return ptr.untrusted_addr;
}

enum {
    REG_IP = 0,
    REG_LR = 1,
    REG_SP = 2,

    OPCODE_SPECIAL_BIT = 0x80
};

untrusted_addr get_ip(vmstate* const vm) {
    const untrusted_addr a = { vm->registers[REG_IP] & ~(addr_t)3 };
    return a;
}

void set_ip(vmstate* const vm, addr_t ip) {
    vm->registers[REG_IP] = ip;
}

untrusted_addr get_lr(vmstate* const vm) {
    const untrusted_addr a = { vm->registers[REG_LR] & ~(addr_t)3 };
    return a;
}

void set_lr(vmstate* const vm, const addr_t lr) {
    vm->registers[REG_LR] = lr;
}

untrusted_addr get_sp(vmstate* const vm) {
    const untrusted_addr a = { vm->registers[REG_SP] };
    return a;
}

void set_sp(vmstate* const vm, const addr_t sp) {
    vm->registers[REG_SP] = sp;
}

untrusted_addr get_addr(vmstate* const vm, const uint8_t reg, const uint8_t offset) {
    untrusted_addr a = { vm->registers[reg] + offset };
    return a;
}

uint8_t inst_op(const inst_t inst) {
    return (inst & 0xFF000000u) >> 24;
}

uint8_t inst_3op_dst(const inst_t inst) {
    return (inst & 0x00FF0000u) >> 16;
}

uint8_t inst_3op_lhs(const inst_t inst) {
    return (inst & 0x0000FF00u) >> 8;
}

uint8_t inst_3op_rhs(const inst_t inst) {
    return inst & 0x000000FFu;
}

#define COUNTOF(X) ((sizeof(X)/sizeof(*X)))

void get_regname(char* const buf, const int reg) {
    switch (reg) {
    case REG_IP:
        strcpy(buf, "rip");
        break;
    case REG_LR:
        strcpy(buf, "rlr");
        break;
    case REG_SP:
        strcpy(buf, "rsp");
        break;
    default:
        sprintf(buf, "r%d", reg);
    }
}

void print_regs(const vmstate* const vm) {
    char regnamel[16], regnamer[16];

    for (int r = 0; r < COUNTOF(vm->registers) / 2; ++r) {
        const int r2 = r + COUNTOF(vm->registers) / 2;

        if (vm->registers[r] != 0 || vm->registers[r2] != 0) {
            get_regname(regnamel, r);
            get_regname(regnamer, r2);

            printf("%4s = 0x%-16lx    %s = 0x%-16lx\n", 
                   regnamel, vm->registers[r],
                   regnamer, vm->registers[r2]);
        }
    }
}

void handle_syscall(vmstate* const vm) {
    print_regs(vm);
}

uint32_t b32toh(uint32_t x) {
    return ((x & 0xFF) << 24) | ((x & 0xFF00) << 8) | ((x & 0xFF0000) >> 8) | ((x & 0xFF000000u) >> 24);
}

void execute(vmstate* const vm, const long imgsize)
{
    while (1) {
        const addr_t ipaddr = check_addr(get_ip(vm), vm, 4);
        set_ip(vm, ipaddr + sizeof(inst_t));
        const inst_t* const ip = (inst_t*)(vm->memory + ipaddr);

        const inst_t inst = b32toh(*ip);

        const uint8_t
            // all encodings
            opcode = inst_op(inst),

            // 3-op encoding
            dst = inst_3op_dst(inst),
            lhs = inst_3op_lhs(inst),
            rhs = inst_3op_rhs(inst),

            // mem encoding
            reg = dst,
            addrreg = lhs,
            offset = rhs,

            // jump encoding
            jumpreg = dst,
            compreg = dst;

        const int16_t
            // jump encoding
            jumpoffset = (lhs << 8) | rhs;
    
        const size_t jumpamt = (jumpoffset < 0
                                ? (size_t)0 - (((size_t)-jumpoffset & 0xFFFF) << 2)
                                : ((size_t)jumpoffset & 0xFFFF) << 2);

        const size_t jumpdst = ipaddr + jumpamt;

        const untrusted_addr addr = get_addr(vm, addrreg, offset);

        fprintf(stderr, "Opcode = 0x%x\n", opcode);

        switch (opcode) {
        case OP_ADD: {
            vm->registers[dst] = vm->registers[lhs] + vm->registers[rhs];
            break;
        }

        case OP_SUB: {
            vm->registers[dst] = vm->registers[lhs] - vm->registers[rhs];
            break;
        }

        case OP_DIV: {
            vm->registers[dst] = vm->registers[lhs] / vm->registers[rhs];
            break;
        }

        case OP_MUL: {
            vm->registers[dst] = vm->registers[lhs] * vm->registers[rhs];
            break;
        }

        case OP_BIT_AND: {
            vm->registers[dst] = vm->registers[lhs] & vm->registers[rhs];
            break;
        }

        case OP_BIT_OR: {
            vm->registers[dst] = vm->registers[lhs] | vm->registers[rhs];
            break;
        }

            // FLOATING POINT OPS

        case OP_FADD: {
            vm->fregisters[dst] = vm->fregisters[lhs] + vm->fregisters[rhs];
            break;
        }

        case OP_FSUB: {
            vm->fregisters[dst] = vm->fregisters[lhs] - vm->fregisters[rhs];
            break;
        }

        case OP_FDIV: {
            vm->fregisters[dst] = vm->fregisters[lhs] / vm->fregisters[rhs];
            break;
        }

        case OP_FMUL: {
            vm->fregisters[dst] = vm->fregisters[lhs] * vm->fregisters[rhs];
            break;
        }

            // MEMORY OPS

        case OP_LOAD_BYTE: {
            const addr_t taddr = check_addr(addr, vm, sizeof(uint8_t));
            vm->registers[reg] = vm->memory[taddr];
            break;
        }

        case OP_LOAD_2BYTE: {
            const addr_t taddr = check_addr(addr, vm, sizeof(uint16_t));
            vm->registers[reg] = *(uint16_t*)(vm->memory + taddr);
            break;
        }

        case OP_LOAD_4BYTE: {
            const addr_t taddr = check_addr(addr, vm, sizeof(uint32_t));
            vm->registers[reg] = *(uint32_t*)(vm->memory + taddr);
            break;
        }

        case OP_LOAD_WORD: {
            const addr_t taddr = check_addr(addr, vm, sizeof(size_t));
            vm->registers[reg] = *(size_t*)(vm->memory + taddr);
            break;
        }

        case OP_LOAD_SLIMM: {
            const int16_t value = (lhs << 8) | rhs;
            if (value < 0) {
                vm->registers[dst] = ((size_t)-1 & ~(size_t)0xFFFFu) | (uint16_t)value;
            } else {
                vm->registers[dst] = (size_t)value & 0xFFFFu;
            }
            break;
        }

        case OP_LOAD_ULIMM: {
            const uint16_t value = (lhs << 8) | rhs;
            vm->registers[dst] = value;
            break;
        }

        case OP_OR_UUIMM: {
            const uint32_t value = ((uint32_t)lhs << 24) | ((uint32_t)rhs << 16);
            vm->registers[dst] |= value;
            break;
        }

        case OP_STORE_BYTE: {
            const addr_t taddr = check_addr(addr, vm, sizeof(uint8_t));
            vm->memory[taddr] = vm->registers[reg] & 0xFF;
            break;
        }

        case OP_STORE_2BYTE: {
            const addr_t taddr = check_addr(addr, vm, sizeof(uint16_t));
            *(uint16_t*)(vm->memory + taddr) = vm->registers[reg] & 0xFFFF;
            break;
        }

        case OP_STORE_4BYTE: {
            const addr_t taddr = check_addr(addr, vm, sizeof(uint32_t));
            *(uint32_t*)(vm->memory + taddr) = vm->registers[reg] & 0xFFFFFFFF;
            break;
        }

        case OP_STORE_WORD: {
            const addr_t taddr = check_addr(addr, vm, sizeof(size_t));
            *(size_t*)(vm->memory + taddr) = vm->registers[reg];
            break;
        }

        case OP_REGCALL: {
            set_lr(vm, ipaddr);
            set_ip(vm, vm->registers[jumpreg]);
            break;
        }

        case OP_RELCALL: {
            set_lr(vm, ipaddr);
            set_ip(vm, ipaddr + jumpoffset);
            break;
        }

        case OP_RELJUMP_IF0: {
            if (vm->registers[compreg] == 0) {
                set_ip(vm, jumpdst);
            }
            break;
        }

        case OP_RELJUMP_IFLT0: {
            if (vm->registers[compreg] & ~(SIZE_MAX >> 1)) {
                set_ip(vm, jumpdst);
            }
            break;
        }

        case OP_RELJUMP_IFGT0: {
            if (!(vm->registers[compreg] & ~(SIZE_MAX >> 1))) {
                set_ip(vm, jumpdst);
            }
            break;
        }

        case OP_RELJUMP_IFLTE0: {
            if ((vm->registers[compreg] == 0) | (vm->registers[compreg] & ~(SIZE_MAX >> 1))) {
                set_ip(vm, jumpdst);
            }
            break;
        }

        case OP_RELJUMP_IFGTE0: {
            if ((vm->registers[compreg] == 0) | !(vm->registers[compreg] & ~(SIZE_MAX >> 1))) {
                set_ip(vm, jumpdst);
            }
            break;
        }

        case OP_SYSCALL:
            handle_syscall(vm);
            break;

        default:
            fprintf(stderr, "Opcode 0x%02x unrecognized\n", opcode);
            require(!"Unrecognized opcode");
            break;
        }
    }
}

int main(const int argc, const char* const* const argv) {
    if (argc < 2) {
        fprintf(stderr, "Usage: %s FILE\n", argv[0]);
        exit(1);
    }

    FILE* in = fopen(argv[1], "rb");

    if (in) {
        require(fseek(in, 0, SEEK_END) == 0);
        const long pos = ftell(in);

        require(fseek(in, 0, SEEK_SET) == 0);

        vmstate* const vm = calloc(sizeof(*vm), 1);

        vm->memory_size = 1 * 1024 * 1024 * 1024;
        vm->memory = malloc(vm->memory_size);

        require(fread(vm->memory, pos, 1, in) == 1);
        fclose(in);
        in = NULL;

        execute(vm, pos);
    } else {
        fprintf(stderr, "Can't open %s\n", argv[1]);
        exit(1);
    }

    return 0;
}
