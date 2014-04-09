import ops
import bytestream
import script

def compile(filename):
    """
    Compile a .bt file into a script.

    """
    f = open(filename,'r')
    raw_string = f.read().replace('\n',' ')
    raw_list = [x for x in raw_string.split(' ') if x != '']
    parsed_list = []
    #for i in xrange(1,len(raw_list)):
    for item in raw_list:
        #item = raw_list[i]
        if len(item) > 1 and item[:2] == 'OP':
            try:
                parsed_list.append(ops.word[item])
            except KeyError:
                print "Unrecognized op %s" % (item,)
                return
        else:
            bstream = bytestream.bytestream(item)
            # add a pushing op if needed
            if (len(parsed_list) == 0 or
                ((isinstance(parsed_list[-1], ops.op) and (parsed_list[-1].opcode < 1 or parsed_list[-1].opcode > 75)) or
                not isinstance(parsed_list[-1], ops.op))):
                parsed_list.append(ops.code[len(bstream)])
            parsed_list.append(bstream)

    stream = bytestream.bytestream('')
    for parsed_item in parsed_list:
        if(isinstance(parsed_item, ops.op)):
            stream += parsed_item.stream()
        else:
            stream += parsed_item
    return script.script(stream)
    
