"""
For parsing objdump files.

"""
import re
from collections import namedtuple
INSTRUCTION_SET = ['%al', '%bl', '%dl', 'add', 'addw', 'and', 'callq', 'cmovbe', 'cmove', 'cmovge', 'cmovne', 'cmp', 'cmpb', 'cmpq', 'cmpsb', 'data32', 'ja', 'ja', 'jae', 'jb', 'jb', 'jbe', 'je', 'je', 'jg', 'jg', 'jle', 'jmp', 'jmpq', 'jne', 'lea', 'lock', 'mov', 'movabs', 'movb', 'movl', 'movq', 'movsd', 'movslq', 'movswl', 'movw', 'movzbl', 'movzwl', 'nop', 'nopl', 'nopw', 'not', 'or', 'or', 'pop', 'push', 'pushq', 'repz', 'retq', 'sar', 'sbb', 'sete', 'setne', 'shl', 'shr', 'sub', 'test', 'testb', 'xadd', 'xchg', 'xor', 'xorb']

Section = namedtuple('Section', [
        'name',
        'content'
        ])

Function = namedtuple('Function', [
        'name',
        'addr',
        'alias',
        'args',
        'instructions',
        'plt'
        ])
Function.__new__.__defaults__ = ('', '', None, None, [], False)

Instruction = namedtuple('Instruction', [
        'name', # mov
        'addr', # addr of instruction
        'bytes', # actual bytes ['aa', 'bb', 'cc']
        'opcode', # intval of (name)
        'params', # eax, ebp, etc...
        ])

def print_function(function, print_instructions=True):
    """Pretty-prints a Function namedtuple"""
    addr_pad = 5 # tmp
    print(" \033[07m[%s]\033[0m Function \033[33m%s\033[0m" % (
            str(function.addr).zfill(addr_pad),
            str(function.name)))
    
    if function.instructions and print_instructions:
        instructions = function.instructions
        instructions.sort(key=lambda x: x.addr)
        
        for ins in instructions:
            istr = " \033[07m[%s]\033[0m\t\033[32m%s\t\033[96m%s\033[0m" % (
                str(ins.addr).zfill(addr_pad),
                ins.name,
                ', '.join(ins.params))
            print("%s\033[0m" % (str(istr)))

def _loadfile(filename):
    """Returns a list of lines from `filename`"""
    with open(filename, 'r') as fd:
        lines = filter(lambda x: x,
                       map(lambda x: x.strip(), fd.readlines()))
    return lines

class Objdump:
    def __init__(self, data=None):
        self.data = data
        self.sections = None
        self.values = {} # {'$0x01': 1}
        self.mmap = {}
        self.functions = {}
        self.regex = {
            'byte_single': re.compile('^[0-9A-F]{2}$', re.I),

            'hex_str': re.compile('^[0-9A-F]+$', re.I),

            'function': 
            re.compile('^([0-9A-F]+)\s<([0-9A-Z_\.@]+)>:$', re.I|re.M),

            'instruction': 
            re.compile('([0-9A-F]+):(\s+)(([0-9A-F]{2}\s+){1,7})', re.I|re.M)
            }
    def _getHTMLHeader(self):
        return """<!DOCTYPE html><html><head>
<title> Object Dump </title>
<style>html,body{font-family:monospace;background:#111;color:#ccc;}a{color:orange;text-decoration:none;}a:hover{text-decoration:underline}</style>
</head><body>"""

    def _htmlTag(self, title):
        return "<h3>%s</h3>"  % (str(title))

    def _blue(self, title):
        return "<span style='color:blue;'>%s</span>" % (str(title))

    def _red(self, title):
        return "<span style='color:red;'>%s</span>" % (str(title))

    def _green(self, title):
        return "<span style='color:green;'>%s</span>" % (str(title))

    def _darkgray(self, title):
        return "<span style='color:#666;'>%s</span>" % (str(title))

    def _bold(self, text):
        return "<strong>%s</strong>" % (str(text))

    def _htmlAnchor(self, name):
        return "<a name=\"%s\" id=\"%s\"></a><pre>%s</pre>" % (str(name), str(name), str(name))

    def _htmlLink(self, href, text='[Link]'):
        try:
            return "<a href=\"%s\">%s</a>" % (str(href), str(text))
        except ValueError:
            print "--------------------------------"
            print href
            print text
            print "--------------------------------"

    def _html_print_function(self, func):
        name =func.name
        name = name.replace('_ZN', '::').replace('12', '::')
        html = "<tr><td><pre>%s</pre></td><td colspan=3 style=\"width:80%\">%s</td></tr>" % (
            self._htmlAnchor(func.addr), 
            self._htmlLink("#%s"%func.addr, self._bold(name))
            )

        return html

    def _html_print_instruction(self, ins):
        pstring = ''
        if ins.params:
            for param in ins.params:
                if param == '':
                    continue
                elif ',' in param:
                    pstring += param
                elif param.startswith('<') and param.endswith('>'):
                    param = param[1:-1]
                    for a in self.functions:
                        if self.functions[a] == param:
                            pstring += self._htmlLink("#%s"%a, param)
                            break
                elif param.startswith('$'):
                    pstring += self._htmlLink('#', param)
                elif param in self.mmap.keys():
                    pstring += self._htmlLink("#%s"%param, param)
                else:
                    pstring += "{%s}" % param

        html = "<tr>"
        html += ''.join([
                "<td style='min-width:100px'>%s</td>" % self._htmlAnchor(ins.addr),
                "<td style='min-width:75px'>%s</td>" % self._blue(ins.name),
                "<td style='min-width:200px'>%s</td>" % self._darkgray(' '.join(ins.bytes)),
                "<td>%s</td></tr>" % self._green(pstring)
                ])
        html += '</tr>'
        return html
    
    def _addr2HTML(self, addr):
        if str(type(self.mmap[addr])) == "<class '__main__.Instruction'>":
            try:
                return self._html_print_instruction(self.mmap[addr])
            except KeyError:
                pass
        elif str(type(self.mmap[addr])) == "<class '__main.Function'>":
            try:
                return self._html_print_function(self.mmap[addr])
            except KeyError:
                pass
        else:
            try:
                return self._html_print_function(self.mmap[addr])
            except KeyError:
                return "<tr><td style='color:red;'>'%s'<br>%s</td><td>%s</td></tr>" % (str(type(self.mmap[addr])), addr, str(self.mmap[addr]))

    def toHTML(self, filename=None):
        """Writes HTML file if filename is not None, else returns string"""
        # Move these to separate class
        html = self._getHTMLHeader()
        html += self._htmlTag('Sections')
        for section in self.sections.keys():
            html += "<li>%s</li>" % section
        html += "<hr>"
        html += "<table width='100%'>"

        for addr in sorted(self.mmap.keys()):
            if addr is not None and self.mmap[addr] is not None:
                html += self._addr2HTML(addr)

        if filename is not None:
            with open('/home/cmattoon/Desktop/objdump.html','wb') as fd:
                fd.write(html)
        return html

    def _parseData(self, data=None):
        data = self.data if data is None else data

        lengths = {}
        function = None
        self.sections = {}
        names = set([])
        current_func = None
        for line in data:
            parts = [part.strip() for part in line.split() if not 
                     part.strip().startswith('#')]
            _len = len(parts)
            x = 0
            if _len is 2:

                addr, byte = parts
                addr = addr[:-1]
                if byte.startswith('<'):
                    addr = addr.lstrip('0')
                    byte = byte[:-1]
                    self.addFunction(addr, byte[1:-1])
                    current_func = addr

                elif byte == '00':
                    self.mmap[addr] = None
                else:
                    print("else: \033[32m%s\033[33m %s\033[0m"%(addr,byte))

            elif _len is 4:
                if line.startswith('Disassembly of section'):
                    pre, section = line.split('Disassembly of section ')
                    section = section[:-1]
                    self.addSection(section)

            elif self.regex['instruction'].match(line):
                addr, cmd = line.split(":\t")
                parts = filter(lambda x: x,[x.strip() for x in cmd.split(' ')])
                instr = self.parseInstruction(addr, parts, current_func)
                self.mmap[addr] = instr

    def addSection(self, section_name):
        """Currently, makes note that a given section was seen.

        Example:
        self.sections = {'.fini':True,'.init':True,'.plt':True,'.text':True}
        """
        self.sections[section_name.strip()] = True

    def getMain(self):
        return self.mmap[[addr for addr in self.functions.keys() 
                          if self.functions[addr] == 'main'][0]]

    def getFunctions(self):
        """Yields a list of Function namedtuples"""
        for addr in self.functions.keys():
            yield self.mmap[addr]

    def getAddr(self, address):
        """Returns the namedtuple at `address` if it exists, else None"""
        try:
            return self.mmap[addr]
        except KeyError:
            return None

    def addFunction(self, addr, function_name):
        self.functions[addr] = function_name

        self.mmap[addr] = Function(
            name=function_name,
            addr=addr,
            alias=None,
            args=None,
            instructions=None,
            plt=('@plt' in function_name))

    def parseInstruction(self, addr, parts, func_ptr=None):
        """Parses an assembly instruction:
        addr, parts =  2baf3, [4c 8b ac 24 b0 07 00 mov 0x7b0(%rsp),%r13]
        
        Args:
          - addr (string): Address of instruction
          - parts (list): A list of strings representing the instruction
          - func_ptr (string): The address of the current function,
                  if applicable. If not None, adds the instruction 
                  namedtuple to the list of instructions for the 
                  function 'pointed to' by `func_ptr`.
        """
        params = []
        rawbytes = []
        name = ''
        cmd_found = False
        
        for i, part in enumerate(parts):
            _len = len(part)
            if part is '#':
                break
            
            if part in INSTRUCTION_SET:
                name = part
                cmd_found = True

            elif _len is 2 and self.regex['byte_single'].match(part):
                # Bytecode
                rawbytes.append(part)

            elif part.startswith('<'):
                if cmd_found:
                    params.append(part)
                else:
                    print("\033[93m%s\033[0m" % (part))
            elif part.startswith('$'):
                params.append(part)
                self.values[part] = part

            elif self.regex['byte_single'].match(part):
                # Not part of the hex bytecode
                params.append(part)

            elif self.regex['hex_str'].match(part):
                params.append(part)

            elif '%' in part:
                # 0xe60(%rsp),%rsi
                params.append(part)

            else:
                print("\033[91;01m%s\033[0m" % (str(part)))

        instr = Instruction(
            name=name,
            addr=addr,
            bytes=rawbytes,
            opcode=None,
            params=params
            )
        if func_ptr is not None:
            self.assignInstructionToFunction(instr, func_ptr)
        return instr

    def assignInstructionToFunction(self, instruction, fptr):
            function = None
            try:
                function = self.mmap[fptr]
            except KeyError:
                pass

            if function:
                instrs = [instruction]
                if function.instructions is not None:
                    instrs += function.instructions

                self.mmap[fptr] = Function(
                    name=function.name,
                    addr=function.addr,
                    alias=function.alias,
                    args=function.args,
                    instructions=instrs,
                    plt=('@plt' in function.name))

            

    def getSections(self):
        """Returns a list of sections in the file (.init, .text, .plt...)"""
        if self.sections is None:
            self._getSections()
        return self.sections

    def _getSections(self):
        for line in self.data:
            if line.startswith('Disassembly of section'):
                pre, section = line.split('Disassembly of section')
                self.sections[section.trim()] = True
        return self.sections

if __name__ == '__main__':
    obj = Objdump(_loadfile('output.asm'))
    obj._parseData()
    obj.toHTML('/home/cmattoon/Desktop/objdump.html')
    #for k in sorted(obj.mmap.keys()):
        #print("\033[92m%s\t\033[36m%s\033[0m" % (k, str(obj.mmap[k])))
    #for function in obj.getFunctions():
    #    print_function(function)
        
