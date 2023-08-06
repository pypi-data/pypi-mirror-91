(" Hissp's basic macros.\n"
 '\n'
 'These are automatically made available as unqualified macros in the\n'
 'Lissp REPL. To use them in a Hissp module, either use the\n'
 'fully-qualified names, or start with the `prelude` macro. You can\n'
 'abbreviate qualifiers with the `alias` macro:\n'
 '\n'
 '.. code-block:: Lissp\n'
 '\n'
 '  (hissp.basic.._macro_.alias b/ hissp.basic.._macro_.)\n'
 '  ;; Now the same as (hissp.basic.._macro_.define foo 2).\n'
 '  (b/#define foo 2)\n'
 '\n'
 'The basic macros are deliberately restricted in design.\n'
 '\n'
 'They have NO DEPENDENCIES in their expansions; they use only the\n'
 'standard library with no extra helper functions. This means that all\n'
 'helper code must be inlined, resulting in larger expansions than might\n'
 'otherwise be necessary. But because macros expand before runtime, the\n'
 'compiled code does not require Hissp to be installed to work, assuming,\n'
 'of course, that there are no other runtime imports of the library code.\n'
 '\n'
 'These may suffice for small projects, but projects with access to better\n'
 'alternatives need not use the basic macros at all.\n'
 '\n'
 'They also have no prerequisite initialization, beyond what is available\n'
 'in a standard Python module. For example, a ``_macro_`` namespace need\n'
 "not be available for ``defmacro``. It's smart enough to check for the\n"
 'presence of ``_macro_`` in its expansion context, and inline the\n'
 'initialization code when required.\n'
 '\n'
 'With the exception of ``prelude`` (which is only meant for the top\n'
 'level), they also eschew any expansions directly to Python code, relying\n'
 'only on the built-in special forms ``quote`` and ``lambda``, which makes\n'
 'their expansions compatible with advanced rewriting macros that process\n'
 'the Hissp expansions of other macros.\n'
 '\n'
 'To help keep macros and their expansions manageable in complexity,\n'
 'these basic macros lack some of the extra features their equivalents\n'
 'have in Python or in other Lisps.\n')

__import__('operator').setitem(
  globals(),
  '_macro_',
  __import__('types').ModuleType(
    '_macro_'))

setattr(
  _macro_,
  'defmacro',
  (lambda name,parameters,docstring,*body:
    (lambda *xAUTO0_:xAUTO0_)(
      (lambda *xAUTO0_:xAUTO0_)(
        'lambda',
        (lambda *xAUTO0_:xAUTO0_)(
          ':',
          '_GxAUTO1_',
          (lambda *xAUTO0_:xAUTO0_)(
            'lambda',
            parameters,
            *body)),
        (lambda *xAUTO0_:xAUTO0_)(
          'builtins..setattr',
          '_GxAUTO1_',
          (lambda *xAUTO0_:xAUTO0_)(
            'quote',
            '__doc__'),
          docstring),
        (lambda *xAUTO0_:xAUTO0_)(
          'builtins..setattr',
          '_GxAUTO1_',
          (lambda *xAUTO0_:xAUTO0_)(
            'quote',
            '__qualname__'),
          (lambda *xAUTO0_:xAUTO0_)(
            '.join',
            "('.')",
            (lambda *xAUTO0_:xAUTO0_)(
              'quote',
              (lambda *xAUTO0_:xAUTO0_)(
                '_macro_',
                name)))),
        (lambda *xAUTO0_:xAUTO0_)(
          'builtins..setattr',
          'hissp.basic.._macro_',
          (lambda *xAUTO0_:xAUTO0_)(
            'quote',
            name),
          '_GxAUTO1_')))))

# defmacro
(lambda _GxAUTO1_=(lambda test,then,otherwise:
  (lambda *xAUTO0_:xAUTO0_)(
    (lambda *xAUTO0_:xAUTO0_)(
      'lambda',
      (lambda *xAUTO0_:xAUTO0_)(
        'test',
        ':',
        ':*',
        'thenxH_else'),
      (lambda *xAUTO0_:xAUTO0_)(
        (lambda *xAUTO0_:xAUTO0_)(
          'operator..getitem',
          'thenxH_else',
          (lambda *xAUTO0_:xAUTO0_)(
            'operator..not_',
            'test')))),
    test,
    (lambda *xAUTO0_:xAUTO0_)(
      'lambda',
      ':',
      then),
    (lambda *xAUTO0_:xAUTO0_)(
      'lambda',
      ':',
      otherwise))):(
  __import__('builtins').setattr(
    _GxAUTO1_,
    '__doc__',
    ('``if-else`` Basic ternary branching construct.\n'
     '\n'
     "  Like Python's conditional expressions, the 'else' clause is required.\n"
     '  ')),
  __import__('builtins').setattr(
    _GxAUTO1_,
    '__qualname__',
    ('.').join(
      ('_macro_', 'ifxH_else'))),
  __import__('builtins').setattr(
    __import__('builtins').globals()['_macro_'],
    'ifxH_else',
    _GxAUTO1_))[-1])()

# defmacro
(lambda _GxAUTO1_=(lambda *body:
  (lambda *xAUTO0_:xAUTO0_)(
    (lambda *xAUTO0_:xAUTO0_)(
      'lambda',
      ':',
      *body))):(
  __import__('builtins').setattr(
    _GxAUTO1_,
    '__doc__',
    ('Evaluates each form in sequence for side effects.\n'
     '\n'
     '  Evaluates to the same value as its last form (or ``()`` if empty).\n'
     '  ')),
  __import__('builtins').setattr(
    _GxAUTO1_,
    '__qualname__',
    ('.').join(
      ('_macro_', 'progn'))),
  __import__('builtins').setattr(
    __import__('builtins').globals()['_macro_'],
    'progn',
    _GxAUTO1_))[-1])()

# defmacro
(lambda _GxAUTO1_=(lambda condition,*body:
  (lambda *xAUTO0_:xAUTO0_)(
    'hissp.basic.._macro_.ifxH_else',
    condition,
    (lambda *xAUTO0_:xAUTO0_)(
      'hissp.basic.._macro_.progn',
      *body),
    ())):(
  __import__('builtins').setattr(
    _GxAUTO1_,
    '__doc__',
    ('When the condition is true,\n'
     '  evaluates each form in sequence for side effects.\n'
     '  Evaluates to the same value as its last form.\n'
     '  Otherwise, skips them and returns ``()``.\n'
     '  ')),
  __import__('builtins').setattr(
    _GxAUTO1_,
    '__qualname__',
    ('.').join(
      ('_macro_', 'when'))),
  __import__('builtins').setattr(
    __import__('builtins').globals()['_macro_'],
    'when',
    _GxAUTO1_))[-1])()

# defmacro
(lambda _GxAUTO1_=(lambda condition,*body:
  (lambda *xAUTO0_:xAUTO0_)(
    'hissp.basic.._macro_.ifxH_else',
    condition,
    (),
    (lambda *xAUTO0_:xAUTO0_)(
      'hissp.basic.._macro_.progn',
      *body))):(
  __import__('builtins').setattr(
    _GxAUTO1_,
    '__doc__',
    ('Unless the condition is true,\n'
     '  evaluates each form in sequence for side effects.\n'
     '  Evaluates to the same value as its last form.\n'
     '  Otherwise, skips them and returns ``()``.\n'
     '  ')),
  __import__('builtins').setattr(
    _GxAUTO1_,
    '__qualname__',
    ('.').join(
      ('_macro_', 'unless'))),
  __import__('builtins').setattr(
    __import__('builtins').globals()['_macro_'],
    'unless',
    _GxAUTO1_))[-1])()

# defmacro
(lambda _GxAUTO1_=(lambda pairs,*body:
  (lambda *xAUTO0_:xAUTO0_)(
    (lambda *xAUTO0_:xAUTO0_)(
      'lambda',
      (lambda *xAUTO0_:xAUTO0_)(
        ':',
        *pairs),
      *body))):(
  __import__('builtins').setattr(
    _GxAUTO1_,
    '__doc__',
    ('Creates locals. Pairs are implied. Locals are not in scope until the body.')),
  __import__('builtins').setattr(
    _GxAUTO1_,
    '__qualname__',
    ('.').join(
      ('_macro_', 'let'))),
  __import__('builtins').setattr(
    __import__('builtins').globals()['_macro_'],
    'let',
    _GxAUTO1_))[-1])()

# defmacro
(lambda _GxAUTO1_=(lambda name,parameters,docstring=(),*body:
  # let
  (lambda xDOLR_fn='_fnxAUTO7_':
    # let
    (lambda fn=(lambda *xAUTO0_:xAUTO0_)(
      'lambda',
      parameters,
      docstring,
      *body),ns=# unless
    # hissp.basic.._macro_.ifxH_else
    (lambda test,*thenxH_else:
      __import__('operator').getitem(
        thenxH_else,
        __import__('operator').not_(
          test))())(
      __import__('operator').contains(
        __import__('hissp.compiler',fromlist='?').NS.get(),
        '_macro_'),
      (lambda :()),
      (lambda :
        # hissp.basic.._macro_.progn
        (lambda :
          (lambda *xAUTO0_:xAUTO0_)(
            (lambda *xAUTO0_:xAUTO0_)(
              'operator..setitem',
              (lambda *xAUTO0_:xAUTO0_)(
                'builtins..globals'),
              (lambda *xAUTO0_:xAUTO0_)(
                'quote',
                '_macro_'),
              (lambda *xAUTO0_:xAUTO0_)(
                'types..ModuleType',
                (lambda *xAUTO0_:xAUTO0_)(
                  'quote',
                  '_macro_')))))())),dc=# when
    # hissp.basic.._macro_.ifxH_else
    (lambda test,*thenxH_else:
      __import__('operator').getitem(
        thenxH_else,
        __import__('operator').not_(
          test))())(
      __import__('hissp.reader',fromlist='?').is_string(
        docstring),
      (lambda :
        # hissp.basic.._macro_.progn
        (lambda :
          (lambda *xAUTO0_:xAUTO0_)(
            (lambda *xAUTO0_:xAUTO0_)(
              'builtins..setattr',
              xDOLR_fn,
              (lambda *xAUTO0_:xAUTO0_)(
                'quote',
                '__doc__'),
              docstring)))()),
      (lambda :())),qn=(lambda *xAUTO0_:xAUTO0_)(
      'builtins..setattr',
      xDOLR_fn,
      (lambda *xAUTO0_:xAUTO0_)(
        'quote',
        '__qualname__'),
      (lambda *xAUTO0_:xAUTO0_)(
        '.join',
        "('.')",
        (lambda *xAUTO0_:xAUTO0_)(
          'quote',
          (lambda *xAUTO0_:xAUTO0_)(
            '_macro_',
            name)))):
      (lambda *xAUTO0_:xAUTO0_)(
        'hissp.basic.._macro_.let',
        (lambda *xAUTO0_:xAUTO0_)(
          xDOLR_fn,
          fn),
        *ns,
        *dc,
        qn,
        (lambda *xAUTO0_:xAUTO0_)(
          'builtins..setattr',
          '_macro_',
          (lambda *xAUTO0_:xAUTO0_)(
            'quote',
            name),
          xDOLR_fn)))())()):(
  __import__('builtins').setattr(
    _GxAUTO1_,
    '__doc__',
    ('Creates a new macro for the current module.\n'
     '\n'
     "  If there's no ``_macro_``, creates one (using `types.ModuleType`).\n"
     "  If there's a docstring, stores it as the new lambda's ``__doc__``.\n"
     "  Adds the ``_macro_`` prefix to the lambda's ``__qualname__``.\n"
     '  Saves the lambda in ``_macro_`` using the given attribute name.\n'
     '  ')),
  __import__('builtins').setattr(
    _GxAUTO1_,
    '__qualname__',
    ('.').join(
      ('_macro_', 'defmacro'))),
  __import__('builtins').setattr(
    __import__('builtins').globals()['_macro_'],
    'defmacro',
    _GxAUTO1_))[-1])()

# defmacro
# hissp.basic.._macro_.let
(lambda _fnxAUTO7_=(lambda name,value:(
  ('Assigns a global in the current module.'),
  (lambda *xAUTO0_:xAUTO0_)(
    'operator..setitem',
    (lambda *xAUTO0_:xAUTO0_)(
      'builtins..globals'),
    (lambda *xAUTO0_:xAUTO0_)(
      'quote',
      name),
    value))[-1]):(
  __import__('builtins').setattr(
    _fnxAUTO7_,
    '__doc__',
    ('Assigns a global in the current module.')),
  __import__('builtins').setattr(
    _fnxAUTO7_,
    '__qualname__',
    ('.').join(
      ('_macro_', 'define'))),
  __import__('builtins').setattr(
    _macro_,
    'define',
    _fnxAUTO7_))[-1])()

# defmacro
# hissp.basic.._macro_.let
(lambda _fnxAUTO7_=(lambda name,bases,*body:(
  ('Defines a type (class) in the current module.\n'
   '\n'
   '  Key-value pairs are implied in the body.\n'
   '  '),
  (lambda *xAUTO0_:xAUTO0_)(
    'hissp.basic.._macro_.define',
    name,
    (lambda *xAUTO0_:xAUTO0_)(
      'builtins..type',
      (lambda *xAUTO0_:xAUTO0_)(
        'quote',
        name),
      (lambda *xAUTO0_:xAUTO0_)(
        (lambda *xAUTO0_:xAUTO0_)(
          'lambda',
          (lambda *xAUTO0_:xAUTO0_)(
            ':',
            ':*',
            'xAUTO0_'),
          'xAUTO0_'),
        *bases),
      (lambda *xAUTO0_:xAUTO0_)(
        'builtins..dict',
        ':',
        *body))))[-1]):(
  __import__('builtins').setattr(
    _fnxAUTO7_,
    '__doc__',
    ('Defines a type (class) in the current module.\n'
     '\n'
     '  Key-value pairs are implied in the body.\n'
     '  ')),
  __import__('builtins').setattr(
    _fnxAUTO7_,
    '__qualname__',
    ('.').join(
      ('_macro_', 'deftype'))),
  __import__('builtins').setattr(
    _macro_,
    'deftype',
    _fnxAUTO7_))[-1])()

# defmacro
# hissp.basic.._macro_.let
(lambda _fnxAUTO7_=(lambda *args:
  (lambda *xAUTO0_:xAUTO0_)(
    'builtins..print',
    ("('Nothingness above abstraction\\n'\n"
     " '  but implementation is / the best name.\\n'\n"
     " 'Terseness may make one too many / get used to them\\n'\n"
     " '  else overflow your brain.\\n'\n"
     " 'No substitute for understanding\\n'\n"
     " 'Code;     the liability\\n'\n"
     " 'as asset; the   ability.\\n'\n"
     " 'The biggest chunks / are hard to swallow\\n'\n"
     " '  as simple as possible / no more.\\n'\n"
     " 'Source was made / for the human\\n'\n"
     " '  object / the machine.\\n'\n"
     " 'Are you lazy enough to bear / the sincerest form / of other ways of "
     "being?\\n'\n"
     " '*having* decent standards / is more important / than exactly what they "
     "are\\n'\n"
     " 'Perfection / is expensive\\n'\n"
     " '  magic / highly prized\\n'\n"
     ' "  pay for when / it\'s Worth It\\n"\n'
     " '  a quarter is advised\\n'\n"
     " 'Readability / is mainly / laid out on the page.\\n'\n"
     " 'Golfing / makes good practice / best practice it betrays.\\n'\n"
     " 'Castles built / in the air / where they do belong\\n'\n"
     " '  Elegance / then exception\\n'\n"
     " '  Form / before detail\\n'\n"
     " '  whence under them,\\n'\n"
     " 'Foundations appear.\\n'\n"
     " 'Make the right way obvious,\\n'\n"
     " 'meditate on this.\\n'\n"
     " '  --Za Zen of Hissp\\n')"))):(
  __import__('builtins').setattr(
    _fnxAUTO7_,
    '__qualname__',
    ('.').join(
      ('_macro_', 'import'))),
  __import__('builtins').setattr(
    _macro_,
    'import',
    _fnxAUTO7_))[-1])()

# defmacro
# hissp.basic.._macro_.let
(lambda _fnxAUTO7_=(lambda target,*args:(
  ('Attaches the named variables to the target as attributes.\n'
   '\n'
   '  Positional arguments must be unqualified identifiers,\n'
   '  and use that as the attribute name.\n'
   '  Names after the ``:`` are attribute-value pairs.\n'
   '  Returns the target.\n'
   '  '),
  # let
  (lambda iargs=iter(
    args),xDOLR_target='_targetxAUTO16_':
    # let
    (lambda args=__import__('itertools').takewhile(
      (lambda a:
        __import__('operator').ne(
          a,
          ':')),
      iargs):
      (lambda *xAUTO0_:xAUTO0_)(
        'hissp.basic.._macro_.let',
        (lambda *xAUTO0_:xAUTO0_)(
          xDOLR_target,
          target),
        *map(
          (lambda arg:
            (lambda *xAUTO0_:xAUTO0_)(
              'builtins..setattr',
              xDOLR_target,
              (lambda *xAUTO0_:xAUTO0_)(
                'quote',
                arg),
              arg)),
          args),
        *map(
          (lambda kw:
            (lambda *xAUTO0_:xAUTO0_)(
              'builtins..setattr',
              xDOLR_target,
              (lambda *xAUTO0_:xAUTO0_)(
                'quote',
                kw),
              next(
                iargs))),
          iargs),
        xDOLR_target))())())[-1]):(
  __import__('builtins').setattr(
    _fnxAUTO7_,
    '__doc__',
    ('Attaches the named variables to the target as attributes.\n'
     '\n'
     '  Positional arguments must be unqualified identifiers,\n'
     '  and use that as the attribute name.\n'
     '  Names after the ``:`` are attribute-value pairs.\n'
     '  Returns the target.\n'
     '  ')),
  __import__('builtins').setattr(
    _fnxAUTO7_,
    '__qualname__',
    ('.').join(
      ('_macro_', 'attach'))),
  __import__('builtins').setattr(
    _macro_,
    'attach',
    _fnxAUTO7_))[-1])()

# defmacro
# hissp.basic.._macro_.let
(lambda _fnxAUTO7_=(lambda self,*calls:(
  ('Call multiple methods on one object.\n'
   '\n'
   '  Evaluates the given ``self``, then injects it as the first argument to\n'
   '  a sequence of calls. Returns the result of the last call.\n'
   '  '),
  # let
  (lambda xDOLR_self='_selfxAUTO20_':
    (lambda *xAUTO0_:xAUTO0_)(
      (lambda *xAUTO0_:xAUTO0_)(
        'lambda',
        (lambda *xAUTO0_:xAUTO0_)(
          ':',
          xDOLR_self,
          self),
        *map(
          (lambda call:
            (lambda *xAUTO0_:xAUTO0_)(
              __import__('operator').getitem(
                call,
                (0)),
              xDOLR_self,
              *__import__('operator').getitem(
                call,
                slice(
                  (1),
                  None)))),
          calls))))())[-1]):(
  __import__('builtins').setattr(
    _fnxAUTO7_,
    '__doc__',
    ('Call multiple methods on one object.\n'
     '\n'
     '  Evaluates the given ``self``, then injects it as the first argument to\n'
     '  a sequence of calls. Returns the result of the last call.\n'
     '  ')),
  __import__('builtins').setattr(
    _fnxAUTO7_,
    '__qualname__',
    ('.').join(
      ('_macro_', 'cascade'))),
  __import__('builtins').setattr(
    _macro_,
    'cascade',
    _fnxAUTO7_))[-1])()

# defmacro
# hissp.basic.._macro_.let
(lambda _fnxAUTO7_=(lambda expr,*forms:(
  ("``->`` 'Thread-first'.\n"
   '\n'
   '  Converts a pipeline to function calls by recursively threading it as\n'
   '  the first argument of the next form.\n'
   '  E.g. ``(-> x (A b) (C d e))`` is ``(C (A x b) d e)``\n'
   '  Makes chained method calls easier to read.\n'
   '  '),
  # ifxH_else
  (lambda test,*thenxH_else:
    __import__('operator').getitem(
      thenxH_else,
      __import__('operator').not_(
        test))())(
    forms,
    (lambda :
      (lambda *xAUTO0_:xAUTO0_)(
        'hissp.basic..xAUTO_.xH_xGT_',
        (lambda *xAUTO0_:xAUTO0_)(
          __import__('operator').getitem(
            __import__('operator').getitem(
              forms,
              (0)),
            (0)),
          expr,
          *__import__('operator').getitem(
            __import__('operator').getitem(
              forms,
              (0)),
            slice(
              (1),
              None))),
        *__import__('operator').getitem(
          forms,
          slice(
            (1),
            None)))),
    (lambda :expr)))[-1]):(
  __import__('builtins').setattr(
    _fnxAUTO7_,
    '__doc__',
    ("``->`` 'Thread-first'.\n"
     '\n'
     '  Converts a pipeline to function calls by recursively threading it as\n'
     '  the first argument of the next form.\n'
     '  E.g. ``(-> x (A b) (C d e))`` is ``(C (A x b) d e)``\n'
     '  Makes chained method calls easier to read.\n'
     '  ')),
  __import__('builtins').setattr(
    _fnxAUTO7_,
    '__qualname__',
    ('.').join(
      ('_macro_', 'xH_xGT_'))),
  __import__('builtins').setattr(
    _macro_,
    'xH_xGT_',
    _fnxAUTO7_))[-1])()

# defmacro
# hissp.basic.._macro_.let
(lambda _fnxAUTO7_=(lambda expr,*forms:(
  ("``->>`` 'Thread-last'.\n"
   '\n'
   '  Converts a pipeline to function calls by recursively threading it as\n'
   '  the last argument of the next form.\n'
   '  E.g. ``(->> x (A b) (C d e))`` is ``(C d e (A b x))``.\n'
   '  Can replace partial application in some cases.\n'
   '  Also works inside a ``->`` pipeline.\n'
   '  E.g. ``(-> x (A a) (->> B b) (C c))`` is ``(C (B b (A x a)) c)``.\n'
   '  '),
  # ifxH_else
  (lambda test,*thenxH_else:
    __import__('operator').getitem(
      thenxH_else,
      __import__('operator').not_(
        test))())(
    forms,
    (lambda :
      (lambda *xAUTO0_:xAUTO0_)(
        'hissp.basic..xAUTO_.xH_xGT_xGT_',
        (lambda *xAUTO0_:xAUTO0_)(
          *__import__('operator').getitem(
            forms,
            (0)),
          expr),
        *__import__('operator').getitem(
          forms,
          slice(
            (1),
            None)))),
    (lambda :expr)))[-1]):(
  __import__('builtins').setattr(
    _fnxAUTO7_,
    '__doc__',
    ("``->>`` 'Thread-last'.\n"
     '\n'
     '  Converts a pipeline to function calls by recursively threading it as\n'
     '  the last argument of the next form.\n'
     '  E.g. ``(->> x (A b) (C d e))`` is ``(C d e (A b x))``.\n'
     '  Can replace partial application in some cases.\n'
     '  Also works inside a ``->`` pipeline.\n'
     '  E.g. ``(-> x (A a) (->> B b) (C c))`` is ``(C (B b (A x a)) c)``.\n'
     '  ')),
  __import__('builtins').setattr(
    _fnxAUTO7_,
    '__qualname__',
    ('.').join(
      ('_macro_', 'xH_xGT_xGT_'))),
  __import__('builtins').setattr(
    _macro_,
    'xH_xGT_xGT_',
    _fnxAUTO7_))[-1])()

# defmacro
# hissp.basic.._macro_.let
(lambda _fnxAUTO7_=(lambda *pairs:(
  ('Multiple condition branching.\n'
   '\n'
   '  Pairs are implied. Default is ``()``. Use ``:else`` to change it.\n'
   '  For example::\n'
   '\n'
   '   (cond)  ; ()\n'
   "   ;; Assume some number 'x\n"
   '   (cond (operator..gt x 0) (print "positive")\n'
   '         (operator..lt x 0) (print "negative")\n'
   '         (operator..eq x 0) (print "zero")\n'
   '         :else (print "not a number"))\n'
   '  '),
  # when
  # hissp.basic.._macro_.ifxH_else
  (lambda test,*thenxH_else:
    __import__('operator').getitem(
      thenxH_else,
      __import__('operator').not_(
        test))())(
    pairs,
    (lambda :
      # hissp.basic.._macro_.progn
      (lambda :
        (lambda *xAUTO0_:xAUTO0_)(
          'hissp.basic.._macro_.ifxH_else',
          __import__('operator').getitem(
            pairs,
            (0)),
          __import__('operator').getitem(
            pairs,
            (1)),
          (lambda *xAUTO0_:xAUTO0_)(
            'hissp.basic..xAUTO_.cond',
            *__import__('operator').getitem(
              pairs,
              slice(
                (2),
                None)))))()),
    (lambda :())))[-1]):(
  __import__('builtins').setattr(
    _fnxAUTO7_,
    '__doc__',
    ('Multiple condition branching.\n'
     '\n'
     '  Pairs are implied. Default is ``()``. Use ``:else`` to change it.\n'
     '  For example::\n'
     '\n'
     '   (cond)  ; ()\n'
     "   ;; Assume some number 'x\n"
     '   (cond (operator..gt x 0) (print "positive")\n'
     '         (operator..lt x 0) (print "negative")\n'
     '         (operator..eq x 0) (print "zero")\n'
     '         :else (print "not a number"))\n'
     '  ')),
  __import__('builtins').setattr(
    _fnxAUTO7_,
    '__qualname__',
    ('.').join(
      ('_macro_', 'cond'))),
  __import__('builtins').setattr(
    _macro_,
    'cond',
    _fnxAUTO7_))[-1])()

# defmacro
# hissp.basic.._macro_.let
(lambda _fnxAUTO7_=(lambda variable,iterable,*body:(
  ('``any-for``\n'
   '  Bind the variable and evaluate the body for each item from the\n'
   '  iterable until any result is true (and return ``True``),\n'
   '  or until the iterable is exhausted (and return ``False``).\n'
   '  '),
  (lambda *xAUTO0_:xAUTO0_)(
    'builtins..any',
    (lambda *xAUTO0_:xAUTO0_)(
      'builtins..map',
      (lambda *xAUTO0_:xAUTO0_)(
        'lambda',
        (lambda *xAUTO0_:xAUTO0_)(
          variable),
        *body),
      iterable)))[-1]):(
  __import__('builtins').setattr(
    _fnxAUTO7_,
    '__doc__',
    ('``any-for``\n'
     '  Bind the variable and evaluate the body for each item from the\n'
     '  iterable until any result is true (and return ``True``),\n'
     '  or until the iterable is exhausted (and return ``False``).\n'
     '  ')),
  __import__('builtins').setattr(
    _fnxAUTO7_,
    '__qualname__',
    ('.').join(
      ('_macro_', 'anyxH_for'))),
  __import__('builtins').setattr(
    _macro_,
    'anyxH_for',
    _fnxAUTO7_))[-1])()

# defmacro
# hissp.basic.._macro_.let
(lambda _fnxAUTO7_=(lambda *exprs:(
  ("``&&`` 'and'. Like Python's ``and`` operator, but for any number of arguments."),
  # cond
  # hissp.basic.._macro_.ifxH_else
  (lambda test,*thenxH_else:
    __import__('operator').getitem(
      thenxH_else,
      __import__('operator').not_(
        test))())(
    __import__('operator').not_(
      exprs),
    (lambda :True),
    (lambda :
      # hissp.basic..xAUTO_.cond
      # hissp.basic.._macro_.ifxH_else
      (lambda test,*thenxH_else:
        __import__('operator').getitem(
          thenxH_else,
          __import__('operator').not_(
            test))())(
        __import__('operator').eq(
          len(
            exprs),
          (1)),
        (lambda :
          __import__('operator').getitem(
            exprs,
            (0))),
        (lambda :
          # hissp.basic..xAUTO_.cond
          # hissp.basic.._macro_.ifxH_else
          (lambda test,*thenxH_else:
            __import__('operator').getitem(
              thenxH_else,
              __import__('operator').not_(
                test))())(
            ':else',
            (lambda :
              (lambda *xAUTO0_:xAUTO0_)(
                'hissp.basic.._macro_.let',
                (lambda *xAUTO0_:xAUTO0_)(
                  '_GxAUTO27_',
                  __import__('operator').getitem(
                    exprs,
                    (0))),
                (lambda *xAUTO0_:xAUTO0_)(
                  'hissp.basic.._macro_.ifxH_else',
                  '_GxAUTO27_',
                  (lambda *xAUTO0_:xAUTO0_)(
                    'hissp.basic..xAUTO_.xET_xET_',
                    *__import__('operator').getitem(
                      exprs,
                      slice(
                        (1),
                        None))),
                  '_GxAUTO27_'))),
            (lambda :
              # hissp.basic..xAUTO_.cond
              ())))))))[-1]):(
  __import__('builtins').setattr(
    _fnxAUTO7_,
    '__doc__',
    ("``&&`` 'and'. Like Python's ``and`` operator, but for any number of arguments.")),
  __import__('builtins').setattr(
    _fnxAUTO7_,
    '__qualname__',
    ('.').join(
      ('_macro_', 'xET_xET_'))),
  __import__('builtins').setattr(
    _macro_,
    'xET_xET_',
    _fnxAUTO7_))[-1])()

# defmacro
# hissp.basic.._macro_.let
(lambda _fnxAUTO7_=(lambda first=(),*rest:(
  ("``||`` 'or'. Like Python's ``or`` operator, but for any number of arguments."),
  # ifxH_else
  (lambda test,*thenxH_else:
    __import__('operator').getitem(
      thenxH_else,
      __import__('operator').not_(
        test))())(
    rest,
    (lambda :
      (lambda *xAUTO0_:xAUTO0_)(
        'hissp.basic.._macro_.let',
        (lambda *xAUTO0_:xAUTO0_)(
          '_firstxAUTO28_',
          first),
        (lambda *xAUTO0_:xAUTO0_)(
          'hissp.basic.._macro_.ifxH_else',
          '_firstxAUTO28_',
          '_firstxAUTO28_',
          (lambda *xAUTO0_:xAUTO0_)(
            'hissp.basic..xAUTO_.xBAR_xBAR_',
            *rest)))),
    (lambda :first)))[-1]):(
  __import__('builtins').setattr(
    _fnxAUTO7_,
    '__doc__',
    ("``||`` 'or'. Like Python's ``or`` operator, but for any number of arguments.")),
  __import__('builtins').setattr(
    _fnxAUTO7_,
    '__qualname__',
    ('.').join(
      ('_macro_', 'xBAR_xBAR_'))),
  __import__('builtins').setattr(
    _macro_,
    'xBAR_xBAR_',
    _fnxAUTO7_))[-1])()

# defmacro
# hissp.basic.._macro_.let
(lambda _fnxAUTO7_=(lambda expr1,*body:(
  ('Evaluates each expression in sequence (for side effects),\n'
   '  resulting in the value of the first.'),
  (lambda *xAUTO0_:xAUTO0_)(
    'hissp.basic.._macro_.let',
    (lambda *xAUTO0_:xAUTO0_)(
      '_value1xAUTO29_',
      expr1),
    *body,
    '_value1xAUTO29_'))[-1]):(
  __import__('builtins').setattr(
    _fnxAUTO7_,
    '__doc__',
    ('Evaluates each expression in sequence (for side effects),\n'
     '  resulting in the value of the first.')),
  __import__('builtins').setattr(
    _fnxAUTO7_,
    '__qualname__',
    ('.').join(
      ('_macro_', 'prog1'))),
  __import__('builtins').setattr(
    _macro_,
    'prog1',
    _fnxAUTO7_))[-1])()

# defmacro
# hissp.basic.._macro_.let
(lambda _fnxAUTO7_=(lambda raw:(
  ('``b#`` bytes literal reader macro'),
  # xH_xGT_
  # hissp.basic..xAUTO_.xH_xGT_
  # hissp.basic..xAUTO_.xH_xGT_
  # hissp.basic..xAUTO_.xH_xGT_
  # hissp.basic..xAUTO_.xH_xGT_
  __import__('ast').literal_eval(
    # xH_xGT_xGT_
    # hissp.basic..xAUTO_.xH_xGT_xGT_
    ("b'{}'").format(
      raw.replace(
        ("'"),
        ("\\'")).replace(
        ('\n'),
        ('\\n')))))[-1]):(
  __import__('builtins').setattr(
    _fnxAUTO7_,
    '__doc__',
    ('``b#`` bytes literal reader macro')),
  __import__('builtins').setattr(
    _fnxAUTO7_,
    '__qualname__',
    ('.').join(
      ('_macro_', 'bxHASH_'))),
  __import__('builtins').setattr(
    _macro_,
    'bxHASH_',
    _fnxAUTO7_))[-1])()

# defmacro
# hissp.basic.._macro_.let
(lambda _fnxAUTO7_=(lambda :(
  ('Grants unqualified access to the basics.\n'
   '\n'
   '  Star imports from `operator` and `itertools`.\n'
   '  And adds the basic macros, but only if available,\n'
   '  so its expansion does not require Hissp to be installed.\n'
   '  (This overwrites ``_macro_`` if you already had one.)\n'
   '  '),
  (lambda *xAUTO0_:xAUTO0_)(
    'builtins..exec',
    ("('from operator import *\\n'\n"
     " 'from itertools import *\\n'\n"
     " 'try:\\n'\n"
     " '    from hissp.basic import _macro_\\n'\n"
     ' "    _macro_ = __import__(\'types\').SimpleNamespace(**vars(_macro_))\\n"\n'
     " 'except ModuleNotFoundError:\\n'\n"
     " '    pass')")))[-1]):(
  __import__('builtins').setattr(
    _fnxAUTO7_,
    '__doc__',
    ('Grants unqualified access to the basics.\n'
     '\n'
     '  Star imports from `operator` and `itertools`.\n'
     '  And adds the basic macros, but only if available,\n'
     '  so its expansion does not require Hissp to be installed.\n'
     '  (This overwrites ``_macro_`` if you already had one.)\n'
     '  ')),
  __import__('builtins').setattr(
    _fnxAUTO7_,
    '__qualname__',
    ('.').join(
      ('_macro_', 'prelude'))),
  __import__('builtins').setattr(
    _macro_,
    'prelude',
    _fnxAUTO7_))[-1])()

# defmacro
# hissp.basic.._macro_.let
(lambda _fnxAUTO7_=(lambda alias,module:(
  ('Defines a reader macro abbreviation of a symbol prefix\n'
   '  (such as a qualifier). For example,\n'
   '\n'
   '  .. code-block:: Lissp\n'
   '\n'
   '     (hissp.basic.._macro_.alias b/ hissp.basic.._macro_.)\n'
   '     ;; Now the same as (hissp.basic.._macro_.define foo 2).\n'
   '     (b/#define foo 2)\n'
   '  '),
  (lambda *xAUTO0_:xAUTO0_)(
    'hissp.basic.._macro_.defmacro',
    ('{}{}').format(
      alias,
      'xHASH_'),
    (lambda *xAUTO0_:xAUTO0_)(
      '_GxAUTO31_'),
    (lambda *xAUTO0_:xAUTO0_)(
      'quote',
      ('Aliases {} as {}#').format(
        module,
        alias)),
    (lambda *xAUTO0_:xAUTO0_)(
      '.format',
      "('{}{}')",
      (lambda *xAUTO0_:xAUTO0_)(
        'quote',
        module),
      '_GxAUTO31_')))[-1]):(
  __import__('builtins').setattr(
    _fnxAUTO7_,
    '__doc__',
    ('Defines a reader macro abbreviation of a symbol prefix\n'
     '  (such as a qualifier). For example,\n'
     '\n'
     '  .. code-block:: Lissp\n'
     '\n'
     '     (hissp.basic.._macro_.alias b/ hissp.basic.._macro_.)\n'
     '     ;; Now the same as (hissp.basic.._macro_.define foo 2).\n'
     '     (b/#define foo 2)\n'
     '  ')),
  __import__('builtins').setattr(
    _fnxAUTO7_,
    '__qualname__',
    ('.').join(
      ('_macro_', 'alias'))),
  __import__('builtins').setattr(
    _macro_,
    'alias',
    _fnxAUTO7_))[-1])()