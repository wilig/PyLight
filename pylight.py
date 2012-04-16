import sys
import inspect
import tokenize
from StringIO import StringIO

function_calls = []
current_locals = []
touched_functions = {}

def _update_token(token, new_value):
    """
    Update the value of a parsed token.
    """
    tuple_list = list(token)
    tuple_list[1] = new_value
    return tuple(tuple_list)

def _last_equal(tokens):
    """
    Handle left/right side of the equation.

    Look for the last equal sign, and substitute from there.
    """
    equals = filter(lambda x: x[0] == 51 and x[1] == '=', tokens)
    if len(equals) > 0:
        return tokens.index(equals[-1])
    else:
        return 0

def _substitute(func, scope, line, index, lines):
    """
    Substitute values for symbols as code executes.
    """
    if line-index <= len(lines):
        token_stream = StringIO(lines[line-index]).readline
        tokens = list(tokenize.generate_tokens(token_stream))
        start_index = _last_equal(tokens)
        for token in filter(lambda x: x[0] == 1, tokens[start_index:]):
            sym = token[1]
            if sym in scope:
                l = tokens.index(token)
                try:
                    tokens[l] = _update_token(token, str(scope[sym]))
                except AttributeError:
                    pass
        translated_tokens = tokenize.untokenize(tokens)
        if func in touched_functions:
            touched_functions[func][-1][line-index] = translated_tokens
        else:
            lines[line-index] = translated_tokens
            touched_functions[func][-1] = lines

def _new_context(func, lines):
    """
    Handle recursive functions by creating a new context for each call.
    """
    if func in touched_functions:
        touched_functions[func].append(lines)
    else:
        touched_functions[func] = [lines]

def _pop_context(func):
    """
    Remove the context from the list when a function returns.
    """
    return touched_functions[func].pop()

def _add_locals(locals):
    current_locals.append(locals)

def _clear_locals():
    locals = current_locals
    #current_locals.clear()
    return locals

def _trace(frame, event, arg, verbose=False):
    """
    Install ourselves as a debugger.

    This little gem is what makes all this possible.
    """
    try:
        func = frame.f_code.co_name
        if verbose:
            _add_locals(frame.f_locals)
        scope = frame.f_locals
        line_num = frame.f_lineno
        lines, index = inspect.getsourcelines(frame.f_code)
        if event == 'call':
            _new_context(func, lines)
        if event == 'return' and func in touched_functions:
            final_code = ''.join(_pop_context(func))
            function_calls.append((final_code, _clear_locals()))
        else:
            _substitute(frame.f_code.co_name, scope, line_num, index, lines)
    except IOError:
        pass  # Happens when there is no source for a call
    return _trace

def print_trace():
    for func in reversed(function_calls):
        print func[0]

def usage():
    print "python pylight.py {python file}"

if __name__ == '__main__':
    if len(sys.argv) == 2:
        sys.settrace(_trace)
        execfile(sys.argv[1])
        sys.settrace(None)
        print_trace()
    else:
        print usage()