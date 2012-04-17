import ast
import inspect

def graph(func):
    funcs = _graph(func, [])
    print "\nCall graph\n---------------------"
    for f in funcs:
        print
        print ''.join(inspect.getsource(f))

def _graph(func, visited_funcs):
    if func not in visited_funcs:
        visited_funcs.append(func)
        context = func.__globals__
        tree = ast.parse(inspect.getsource(func))
        calls = filter(lambda x: type(x) is ast.Call, ast.walk(tree))
        [_graph(c, visited_funcs) for c in _resolve_calls(calls, context)]
        return visited_funcs

def _resolve_calls(calls, context):
    funcs = []
    for call in calls:
        if type(call.func) is ast.Name:
            try:
                func = context[call.func.id]
                funcs.append(func)
            except KeyError:
                print "Warning, couldn't resolve '%s'" % call.func.id
        elif type(call.func) is ast.Attribute and type(call.func.value) is not ast.Subscript:
            print ("Error resolving %s.%s failed can't resolve attribute "
                   "lookups yet." % (call.func.value.id, call.func.attr))
    return funcs
