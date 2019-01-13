#!/usr/bin/python

import subprocess
from optparse import OptionParser
import brainy_quote


def run_command(command):
    process = subprocess.Popen(command.split(), stdout=subprocess.PIPE)
    output = process.communicate()[0]


def vararg_callback(option, opt_str, value, parser):
    assert value is None
    value = []

    def floatable(str):
        try:
            float(str)
            return True
        except ValueError:
            return False

    for arg in parser.rargs:
        # stop on --foo like options
        if arg[:2] == "--" and len(arg) > 2:
            break
        # stop on -a, but not on -3 or -3.0
        if arg[:1] == "-" and len(arg) > 1 and not floatable(arg):
            break
        value.append(arg)

    del parser.rargs[:len(value)]
    setattr(parser.values, option.dest, value)


def make_query_string(words):
    return '+'.join(words)


def search(query):
    run_command("python -mwebbrowser https://www.google.com/search?q={search_string}".format(
        search_string=make_query_string(query)))


def feeling_luck():
    feel_good_query = ['happy', 'place']

    try:
        quote = brainy_quote.get_random_quote()
        print(quote)
        if len(quote) != 0:
            feel_good_query = [word for word in quote[0].split()]
    except TypeError:
        pass

    return feel_good_query


def main():
    usage = "usage: %prog [options] arg1 arg2"
    parser = OptionParser(usage)
    parser.add_option("-s", "--search", dest="query",
                      action="callback", callback=vararg_callback)
    parser.add_option("-l", "--lucky",
                      action="store_true", dest="feeling_lucky", help="feeling lucky today, let me search for you")
    (options, args) = parser.parse_args()
    if options.feeling_lucky and options.query:
        parser.error("options -s and -l are mutually exclusive")
    elif options.feeling_lucky:
        search(feeling_luck())
    elif options.query:
        search(parser.values.query)


if __name__ == "__main__":
    main()
