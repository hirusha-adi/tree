import os


class c:
    UNDERLINE = '\033[4m'
    G = '\033[92m'  # GREEN
    R = '\033[91m'  # RED
    W = '\033[0m'  # RESET COLOR
    P = '\033[35m'  # PURPLE
    C = "\x1b[1;36m"  # Cyan


def showlogo():
    print(f"""
    {c.C} _                 
    | |_ _ __ ___  ___ 
    | __| '__/ _ \/ _ \\
    | |_| | |  __/  __/
     \__|_|  \___|\___|
         For Linux
    """)


def create_tree_file():
    tree_file_code = r"""
#!/usr/bin/env python3
import os
from pathlib import Path

# I do not own this code and i am not the person who developed this file
# I found this qustion on stack overflow
# Link: https://stackoverflow.com/questions/9727673/list-directory-tree-structure-in-python
# This is not the selected correct answer in that question in stack overflow
# But this provied a lot of customizability than using os.walk()


class DisplayablePath(object):
    display_filename_prefix_middle = '├──'
    display_filename_prefix_last = '└──'
    display_parent_prefix_middle = '    '
    display_parent_prefix_last = '│   '

    def __init__(self, path, parent_path, is_last):
        self.path = Path(str(path))
        self.parent = parent_path
        self.is_last = is_last
        if self.parent:
            self.depth = self.parent.depth + 1
        else:
            self.depth = 0

    @property
    def displayname(self):
        if self.path.is_dir():
            return self.path.name + '/'
        return self.path.name

    @classmethod
    def make_tree(cls, root, parent=None, is_last=False, criteria=None):
        root = Path(str(root))
        criteria = criteria or cls._default_criteria

        displayable_root = cls(root, parent, is_last)
        yield displayable_root

        children = sorted(list(path
                               for path in root.iterdir()
                               if criteria(path)),
                          key=lambda s: str(s).lower())
        count = 1
        for path in children:
            is_last = count == len(children)
            if path.is_dir():
                yield from cls.make_tree(path,
                                         parent=displayable_root,
                                         is_last=is_last,
                                         criteria=criteria)
            else:
                yield cls(path, displayable_root, is_last)
            count += 1

    @classmethod
    def _default_criteria(cls, path):
        return True

    @property
    def displayname(self):
        if self.path.is_dir():
            return self.path.name + '/'
        return self.path.name

    def displayable(self):
        if self.parent is None:
            return self.displayname

        _filename_prefix = (self.display_filename_prefix_last
                            if self.is_last
                            else self.display_filename_prefix_middle)

        parts = ['{!s} {!s}'.format(_filename_prefix,
                                    self.displayname)]

        parent = self.parent
        while parent and parent.parent is not None:
            parts.append(self.display_parent_prefix_middle
                         if parent.is_last
                         else self.display_parent_prefix_last)
            parent = parent.parent

        return ''.join(reversed(parts))


paths = DisplayablePath.make_tree(Path(f'{os.getcwd()}'))
for path in paths:
    print(path.displayable())
    
"""
    with open("tree", "w", encoding="utf-8") as tree_file:
        tree_file.write(tree_file_code)


if __name__ == "__main__":
    showlogo()
    create_tree_file()
    print(f"{c.P}+ {c.G}Created ./tree file")
    print(f"{c.P}+ {c.G}Copying file to /usr/bin/{c.R}{c.UNDERLINE}")
    x = os.system("cp tree /usr/bin/")
    print(f"{c.W}{c.P}- {c.G}Deleting ./tree file{c.R}{c.UNDERLINE}")
    os.system("rm -rf tree")
