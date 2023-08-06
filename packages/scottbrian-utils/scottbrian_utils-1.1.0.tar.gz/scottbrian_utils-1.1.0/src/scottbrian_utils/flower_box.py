"""flower_box.py module.

==========
flower_box
==========

With **print_flower_box_msg** you can print messages in a flower_box like this:

:Example: print a one line message in a flower box

>>> from scottbrian_utils.flower_box import print_flower_box_msg
>>> print_flower_box_msg('This is my message to the world')
<BLANKLINE>
***********************************
* This is my message to the world *
***********************************

"""

import sys
from typing import List, Optional, TextIO, Union


def print_flower_box_msg(msgs: Union[str, List[str]], *,
                         end: str = '\n',
                         file: Optional[TextIO] = None,
                         flush: bool = False) -> None:
    r"""Print a single or multi-line message inside a flower box (asterisks).

    Args:
        msgs: single message or list of messages to print
        end: Specifies the argument to use on the print statement *end*
               parameter. The default is '\\n'.
        file: Specifies the argument to use on the print statement
                *file* parameter. The default is sys.stdout (via None).
        flush: Specifies the argument to use on the print statement
                 *flush* parameter. The default is False.

    :Example: print a two line message in a flower box

    >>> from scottbrian_utils.flower_box import print_flower_box_msg

    >>> msg_list = ['This is my first line test message', 'and my second line']
    >>> print_flower_box_msg(msg_list)
    <BLANKLINE>
    **************************************
    * This is my first line test message *
    * and my second line                 *
    **************************************

    """
    # =========================================================================
    # Note: the following code that sets file to sys.stdout is needed to allow
    # the test cases to use the pytest capsys built-in fixture. Having
    # sys.stdout as the default parameter in the function definition does
    # not work because capsys changes sys.stdout after the test case gets
    # control, meaning the print statements in StartStopHeader code are not
    # captured. This is also appears to be the case for doctest.
    # So, we simply use None as the default and set file to sys.stdout here
    # which works fine.
    # =========================================================================

    if file is None:
        file = sys.stdout

    if isinstance(msgs, str):  # single message
        msgs = [msgs]  # convert to list

    max_msg_len: int = len(max(msgs, key=len)) + 4  # 4 for front/end asterisks

    # ensure a new line so that our flower box is properly aligned
    print('', file=file)

    print('*' * max_msg_len, end=end, file=file, flush=flush)
    for msg in msgs:
        msg = '* ' + msg + ' ' * (max_msg_len - len(msg) - 4) + ' *'
        print(msg, end=end, file=file, flush=flush)
    print('*' * max_msg_len, end=end, file=file, flush=flush)
