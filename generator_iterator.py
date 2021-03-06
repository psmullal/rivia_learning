import sys
import time


def spinner():
    # think_lib = ' .oO*Oo. '
    # think_lib = '-\|/'
    # think_lib = ' -=#=- '
    # think_lib = '*#+-.'

    # think_lib = ['m!   ', 'om!  ', 'oom! ', 'boom!', 'Boom!', 'BOom!', 'BOOm!',
    #              'BOOM!', '  *  ', ' <*> ', '<(*)>', '(***)', '** **', '*   *',
    #              '     ']

    # think_lib = ['     ', '>    ', '->   ', ' ->  ', '  -> ', '   ->', '    -',
    #              '     ', '    <', '   <-', '  <- ', ' <-  ', '-    ']

    # think_lib = ['     ', ')    ', '=)   ', ' =)  ', '  =) ', '   =)', '    =',
    #              '     ', '    (', '   (=', '  (= ', ' (=  ', '=    ']

    # think_lib = ['     ', '+    ', ' +   ', '  +  ', '   + ', '    +', '    *',
    #              '     ', '    +', '   + ', '  +  ', ' +   ', '*    ']

    # think_lib = '><((^>'
    # think_lib = ['     ', '>    ', '->   ', ' ->  ', '  -> ', '   ->', '    -',
    #              '     ', '    <', '   <-', '  <- ', ' <-  ', '-    ']
    # think_lib = ['     ', ')    ', '=)   ', ' =)  ', '  =) ', '   =)', '    =',
    #              '     ', '    (', '   (=', '  (= ', ' (=  ', '=    ']
    # think_lib = ['     ', '+    ', ' +   ', '  +  ', '   + ', '    +', '    *',
                #  '     ', '    +', '   + ', '  +  ', ' +   ', '*    ']
    think_lib = ['>    ', '>>   ', '->>  ', ' ->> ', '  ->>', '   ->', '    -', '    *',
                 '    <', '   <<', '  <<-', ' <<- ', '<<-  ', '<-   ', '-    ', '*    '
                ]
    while True:
        for i in think_lib:
            yield i

t = spinner()

for _ in range(50):
    s = '\r[%s]' % next(t)
    sys.stdout.write(s)
    sys.stdout.flush()
    time.sleep(.25)

sys.stdout.write('\r          ')
sys.stdout.flush()

print('')
