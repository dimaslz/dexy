from dexy.commands.utils import dummy_wrapper
import dexy.doc
import dexy.filter

def env_command():
    """
    Prints list of template plugins.
    """
    f = dexy.filter.Filter.create_instance("template")
    f.doc = dexy.doc.Doc('dummy', dummy_wrapper())
    env = f.run_plugins()

    for k in sorted(env):
        try:
            helpstring, value = env[k]
        except Exception:
            print k
            print "Values should be a (docstring, value) tuple."
            raise

        print "%s: %s" % (k, helpstring,)

from pygments import highlight
from pygments.lexers import PythonLexer
import dexy.data
import dexy.exceptions
import inspect
import pygments.formatters
from dexy.utils import indent
import textwrap

def datas_command(
        alias=False, # Alias of data type to print detaile dinfo for.
        source=False, # Whether to print source code for methods.
        nocolor=False, # If printing source, whether to colorize it.
    ):
    """
    Prints list of data types.
    """
    wrapper = dummy_wrapper()
    settings = {
            'canonical-name' : 'foo'
            }

    generic_methods = [k for (k, v) in inspect.getmembers(dexy.data.Data) if inspect.ismethod(v)]

    print ""

    if not alias:
        for d in dexy.data.Data.__iter__("foo", ".txt", "foo", settings, wrapper):
            print d.alias

        print ""
        print "For more information about a particular data type,"
        print "use the -alias flag and specify the data type alias."
        print ""
    else:
        d = dexy.data.Data.create_instance(alias, "foo", ".txt", "foo", settings, wrapper)

        print alias
        print ""
        print d.setting('help')
        print ""

        print "Methods:"
        for k, v in inspect.getmembers(d):
            if k.startswith('_'):
                continue

            if inspect.ismethod(v) and not k in generic_methods:
                print "    %s" % k

                docs = inspect.getdoc(v)
                if not docs:
                    raise dexy.exceptions.InternalDexyProblem("Must provide docstring for %s" % k)

                print ""
                print indent(docs, 8)
                print ""

                args, varargs, keywords, defaults = inspect.getargspec(v)

                if not source and len(args) > 1:
                    print "        Takes arguments. Run with -source option to see source code."


                if source:
                    source_code = textwrap.dedent(inspect.getsource(v))
                    if nocolor:
                        print indent(source_code, 8)
                    else:
                        formatter = pygments.formatters.TerminalFormatter()
                        lexer = PythonLexer()
                        print indent(highlight(source_code, lexer, formatter), 8)

                print ""
