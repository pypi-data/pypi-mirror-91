from typing import List


def remove_empty_lines(sourcelines: List[str]) -> List[str]:
    return list(filter(lambda x: len(x.strip()) != 0, sourcelines))


def remove_indentation(sourcelines: List[str]) -> List[str]:
    while all(map(lambda x: x.startswith('    '), sourcelines)):
        sourcelines = list(map(lambda x: x[4:], sourcelines))
    return sourcelines


def remove_verbose_decorator(sourcelines: List[str]) -> List[str]:
    return list(filter(lambda x: not x.startswith('@verbosify'), sourcelines))


def rewrite_def_line(sourcelines: List[str]) -> List[str]:
    i = list(map(lambda x: x[:3], sourcelines)).index('def')
    sourcelines[i] = f"{sourcelines[i].rstrip()[:-2]}, verbose=False):"
    return sourcelines


def rewrite_comments(
    sourcelines: List[str], verbose_word: str = ' verbose: '
) -> List[str]:
    for i, sourceline in enumerate(sourcelines):
        if sourceline.strip().startswith(f"#{verbose_word}"):
            tab, text = sourceline.split(f"#{verbose_word}", maxsplit=1)
            sourcelines[i] = f"{tab}if verbose: print('{text}')"
        else:
            sourcelines[i] = sourceline
    return sourcelines


pipeline = [
    remove_empty_lines,
    remove_indentation,
    remove_verbose_decorator,
    rewrite_def_line,
    rewrite_comments,
]


def rewrite_source_code(
    source_code: str, verbose_word: str = ' verbose: '
) -> str:
    sourcelines = source_code.split('\n')
    for pipe_func in pipeline[:-1]:
        sourcelines = pipe_func(sourcelines)
    # The `rewrite_comments` needs a special arguments.
    # FIXME: I should find a way to write this more elegantly
    sourcelines = pipeline[-1](sourcelines, verbose_word)

    return '\n'.join(sourcelines)
