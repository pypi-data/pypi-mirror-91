# -*- coding: utf-8 -*-
import os
from .simplekernel import SimpleKernel
from pyparsing import nestedExpr, Optional, Word, alphanums, alphas,\
                      originalTextFor, Literal, SkipTo, Empty, Or, ZeroOrMore, \
                      restOfLine
from pyparsing import _MAX_INT as pyparsing_MAX_INT
import base64

def skipToMatching(opener, closer):
    """

    :param opener: opening token
    :param closer: closing token

    """
    # https://github.com/sagemath/sagetex/issues/6#issuecomment-734968972
    nest = nestedExpr(opener, closer)
    return originalTextFor(nest)

class TexSurgery(object):
    """TexSurgery allows to make some replacements in LaTeX code"""

    def __init__(self, tex_source, path='.'):
        super(TexSurgery, self).__init__()
        self.original_src = tex_source
        self.src = tex_source
        self.path = path
        #self.kernel is a lazy property
        self._kernel = self.kernel_name = None
        self._auxfiles = 0

    def __del__(self):
        """
        ## Description
        Destructor. Shuts down kernel safely.
        """
        self.shutdown()

    def shutdown(self):
        if self._kernel:
            self._kernel.kernel_manager.shutdown_kernel()
            self._kernel = None

    @property
    def kernel(self):
        if not self._kernel:
            self._kernel = SimpleKernel(self.kernel_name)
        return self._kernel

    def _add_import_action(self, packagename, options):
        def action(l,s,t):
            return '\\documentclass'+ t.restofline + '\n\\usepackage%s{%s}'%(
                '[%s]'%options if options else '',
                packagename
            )
        return action

    def add_import(self, packagename, options=''):
        documentclass = (
            '\\documentclass'+ SkipTo('\n')('restofline')
        )
        documentclass.setParseAction(
            self._add_import_action(packagename, options)
        )
        self.src = documentclass.transformString(self.src)
        return self

    def data_surgery(self, replacements):
        #TODO: use pyparsing instead of regex, for the sake of uniformity
        src = self.src
        import re
        revars = re.compile('|'.join(r'\\'+key for key in replacements))
        pos,pieces = 0, []
        m = revars.search(src)
        while m:
            start,end = m.span()
            pieces.append(src[pos:start])
            #start+1, since the backslash \ is not part of the key
            name = src[start+1:end]
            pieces.append(replacements[name])
            pos = end
            m = revars.search(src, pos=pos)
        pieces.append(src[pos:])
        self.src = ''.join(map(str, pieces))
        return self

    def latexify(self, results):
        #TODO 'image/png' grab base64 data, write to a file
        # then insert includegraphics
        #TODO do something special with 'text/html'?
        #TODO error -> texttt
        result = ''
        for r in results:
            hasimage = r.get('image/png')
            if hasimage:
                images_folder = 'images'
                images_path = os.path.join(self.path, images_folder)
                filename = 'texsurgery_image{}.png'.format(self._auxfiles)
                fullpath = os.path.join(
                    images_path,
                    'texsurgery_image{}.png'.format(self._auxfiles))
                if not os.path.exists(images_path):
                    os.mkdir(images_path)
                with open(fullpath, 'wb') as fd:
                    fd.write(base64.b64decode(hasimage))
                result = result+'\n\\includegraphics{%s}\n'%os.path.join(images_folder, filename)
                self._auxfiles += 1
            else:
                result = result+(r.get('text/plain') or r.get('text/html') or r.get('text/latex') or r.get('error'))
        return result

    def runsilent(self, l, s, t):
        self.kernel.executesilent(t.content)
        return ''

    def run(self, l, s, t):
        return self.latexify(self.kernel.execute(t.content, allow_errors=True))

    def eval(self, l, s, t):
        code =  t.content[1:-1]
        return self.latexify(self.kernel.execute(code))

    def srepl(self, l, s, t):
        r"""
        Use for a block of code that should reflect what happens in an interactive sage session
        (both input and output)
        """
        code = t.content
        lines = code.split('\n')+['']
        if not lines:
            return ''
        result = '\\begin{verbatim}\n'
        partialblock = lines.pop(0) +'\n'
        result += 'sage: ' + partialblock
        while lines:
            line = lines.pop(0)
            if line and line[0] in [' ', '\t']:
                partialblock += line+'\n'
                result += '....: '+line+'\n'
            else:
                answer = self.latexify(self.kernel.execute(partialblock))
                if len(answer)>0:
                    result += answer +'\n'
                partialblock = line +'\n'
                if line:
                    result += 'sage: '+line +'\n'
        return result + '\\end{verbatim}'


    def _strip_quotes(self, s):
        if isinstance(s, str) and (s[0]==s[-1]=="'" or s[0]==s[-1]=='"'):
            return s[1:-1]
        return s

    def evalstr(self, l, s, t):
        code =  t.content[1:-1]
        results = self.kernel.execute(code)
        return '\n'.join(
            self._strip_quotes(r.get('text/plain')) or r.get('text/html') or r.get('error')
            for r in results
        )

    def sage(self, l, s, t):
        code =  t.content[1:-1]
        return self.latexify(self.kernel.execute('latex(%s)'%code))

    def sinput(self, l, s, t):
        filename =  t.content[1:-1]
        with open(filename, 'r') as codefile:
            code = codefile.read()
        return self.latexify(self.kernel.execute(code))

    def _truish(self, s):
        '''Return True if the string correspond to the True value
        in the current kernel'''
        if self.kernel_name in ('python2', 'python3', 'sagemath'):
            #TODO: non exhaustive (but just a helper for the user!)
            return s not in ('False', '', '[]', '0', '0.0')
        else:
            return s in ('true', 'True')

    def sif(self, l, s, t):
        code =  t.condition[1:-1]
        results = self.kernel.execute(code)
        if (len(results)==1 and
            self._truish(results[0].get('text/plain'))):
            return t.texif[1:-1]
        else:
            return t.texelse[1:-1]

    def code_surgery(self):
        # Look for usepackage[kernel]{surgery} markup to choose sage, python, R, julia
        #  or whatever interactive command line application
        # Use pyparsing as in student_surgery to go through sage|sagestr|sagesilent|sif|schoose in order
        # Use SimpleKernel to comunicate with a sage process ?

        # Look for usepackage[kernel]{surgery} markup to choose the kernel
        usepackage = '\\usepackage' + Optional('[' + Word(alphanums) + ']') + '{texsurgery}'
        self.kernel_name = usepackage.searchString(self.src, maxMatches=1)[0][2]
        usepackage.setParseAction(lambda l,s,t: '')

        run = self._parserFor('run')
        run.setParseAction(self.run)
        runsilent = self._parserFor('runsilent')
        runsilent.setParseAction(self.runsilent)
        eval = self._parserFor('\\eval', options=False)
        eval.setParseAction(self.eval)
        evalstr = self._parserFor('\\evalstr', options=False)
        evalstr.setParseAction(self.evalstr)
        sage = self._parserFor('\\sage', options=False)
        sage.setParseAction(self.sage)
        sinput = self._parserFor('\\sinput', options=False)
        sinput.setParseAction(self.sinput)
        sif = self._parserFor(
            '\\sif{condition}{texif}{texelse}', options=False
        )
        sif.setParseAction(self.sif)
        srepl = self._parserFor('srepl')
        srepl.setParseAction(self.srepl)
        codeparser = usepackage | run | runsilent | eval | evalstr | sage | sif | sinput | srepl
        codeparser.ignore('%' + restOfLine)
        self.src = codeparser.transformString(self.src)
        return self

    def _opts_parser(self, str_opts):
        '''parse a string of the form "key1=val1,key2=val2..."'''
        return dict(map((lambda s: s.strip()),str_pair.strip().split('='))
                    for str_pair in str_opts.split(','))

    def _parserFor(self, selector, options=True):
        parts, args, restrictions = self._parse_selector(selector)
        name = parts.name
        if args:
            args_parser = sum(
                (Literal('{%s}'%restrictions[arg])(arg) if (arg in restrictions)
                  else skipToMatching('{','}')(arg)
                 for arg in args),
                Empty()
            )
        elif name[0]=='\\':
            args_parser = skipToMatching('{','}')('content')
        else:
            args_parser = Empty()
        if options:
            args_parser = Optional(skipToMatching('[',']'))('options') + args_parser
        if name[0]=='\\':
            return Literal(name)('name') + args_parser
        else:
            return ('\\begin{' + Literal(name)('name') + '}' +
                    args_parser +
                    SkipTo('\\end{'+name+'}')('content') +
                   ('\\end{' + name + '}'))

    def _wholeEnvParserFor(self, env):
        return originalTextFor(
                ('\\begin{' + Literal(env) + '}')
               + SkipTo('\\end{'+env+'}')
               + ('\\end{' + env + '}')
            )('all')

    def _parse_selector(self, selector):
        command_parser = (
            originalTextFor(Optional('\\') + Word(alphas))('name') +
            (ZeroOrMore(nestedExpr('{','}')))('namedargs') +
            originalTextFor(Optional(nestedExpr('[',']')))('options')
            )
        parts = command_parser.searchString(selector)[0]
        args = []
        if parts.namedargs:
            args += [m[0] for m in parts.namedargs]
        if parts.options:
            options = self._opts_parser(parts.options[1:-1])
            if '_nargs' in options:
                nargs = int(options['_nargs'])
                args += ['arg%d'%k for k in  range(nargs)]
                del options['_nargs']
            restrictions = options
        else:
            restrictions = {}
        return parts, args, restrictions

    def insertAfter(self, selector, text):
        istart, iend = self.interval(selector)
        self.src = self.src[:iend] + text + self.src[iend:]
        return self

    def interval(self, selector, tex=None):
        '''starting and ending indices for the first match of a selector'''
        tex = tex or self.src
        #First, if there is a ", " at the top level, we split there
        if ', ' in selector:
            return min(self.interval(subselector, start=start)
                       for subselector in selector.split(', '))
        #the syntax first_element, *rest_of_list works if the list has
        # one element, or two
        parent, *rest = selector.split(' ', 1)
        if rest:
            names = Or([self._wholeEnvParserFor(env_or_command)
                for env_or_command in parent.split(',')])
            match, start, _ = next(names.scanString(tex, maxMatches=1))
            start += len(match.beginenv)
            interv = self.interval(rest[0], match.all)
            if interv:
                nest_start, nest_stop = interv
                return start + nest_start, start + nest_stop
            else:
                return None
        else:
            names = Or([self._parserFor(env_or_command)
                for env_or_command in parent.split(',')])
            match, start, end = next(names.scanString(tex, maxMatches=1))
            return start, end

    def find(self, selector):
        res = self.findall(selector, maxMatches=1)
        return res[0] if res else None

    def findall(self, selector, tex=None, maxMatches=pyparsing_MAX_INT):
        '''Finds all occurrences of a given selector

        currently it is not possible to look for commands nested inside commands,
        the parent can only be an environment.

        :param str selector: a string with the CSS-style selector
        :param str tex: string to search, usually None except for recursive calls
        :param int maxMatches: maximum number of matches, usually either 1
                               or a very big number

        >>> from texsurgery.texsurgery import TexSurgery
        >>> tex = open('tests/test_find.tex').read()
        >>> TexSurgery(tex).findall('question,questionmultx runsilent')
        [('questionmultx', [('runsilent', 'a = randint(1,10)\n')]),
         ('question',
           [('runsilent', 'a = randint(2,10)\nf = sin(a*x)\nfd = f.derivative(x)\n')])]
        >>> TexSurgery(tex).findall('question,questionmultx choices \correctchoice')
        [('question', [('choices', [('\correctchoice', '$\sage{fd}$')])])]
        >>> TexSurgery(tex).findall('questionmultx \AMCnumericChoices[_nargs=2]')
        [('questionmultx', [('\\AMCnumericChoices',
          ['\\eval{8+a}', 'digits=2,sign=false,scoreexact=3'])]
        )]
        '''
        tex = tex or self.src
        #First, if there is a ", " at the top level, we split there
        if ', ' in selector:
            return sum((self.findall(subselector) for subselector in selector.split(', ')), [])
        parent, *rest = selector.split(' ', 1)
        names = Or([self._parserFor(env_or_command)
            for env_or_command in parent.split(',')])
        if rest:
            matches = [
                (match.name, self.findall(rest[0], match.content))
                for match in names.searchString(tex, maxMatches=maxMatches)
            ]
            return [(name,nest) for (name,nest) in matches if nest]
        #if selector is a command (currently it is not possible to look for commands
        # nested inside commands)
        parts, args, restrictions = self._parse_selector(selector)
        if selector[0]=='\\':
            if args:
                return [
                    (match.name, dict((arg, match[arg][1:-1]) for arg in args))
                    for match in names.searchString(tex, maxMatches=maxMatches)
                ]
            return [
                (match.name, match.content[1:-1])
                for match in names.searchString(tex, maxMatches=maxMatches)
            ]
        else:
            if args:
                return [(match.name,
                         dict((arg, match[arg][1:-1]) for arg in args),
                         match.content)
                    for match in names.searchString(tex, maxMatches=maxMatches)
                ]
            else:
                return [
                    (match.name, match.content)
                    for match in names.searchString(tex, maxMatches=maxMatches)
                ]
