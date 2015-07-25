# baker: Build C libraries and programs without makefiles

This tool will automatically build C code without any makefiles. It does so by searching the directory it's run in and all of its
subdirectories for .c files. It then compiles them. Any unresolved include (.h) files are searched for first in its cache, then in
the directory and its subdirectories, and finally, in the directories ancestors and their subdirectories. Baker will keep looking
until the user's home directory is reached.

Once all code is compiled, libraries are created in any source directory that doesn't contain a program (a .c file containing a
*main* function). Finally, any programs are linked, using a similar process as for include files to find libaries that contain
symbols they require.

For improved performance, the rules used to compile each directory are stored in JSON format in the file *baker.doh*. This file can
be checked in to git along with the code. If new dependencies are added, baker will detect them and modify the doh for you.

## Current Release Status

Alpha: Proof of concept. I've used this version to build a couple of simple projects.

## How to Install and Run

Bring baker down from github. Include the main directory in your path or create a symbolic link to "baker" from a directory in your
path. Go to the directory you want to compile and type "baker"

## Options

Run baker -h for help:

Option | Long Option | Description
------ | ----------- | -----------
    -n | --noaction  | Tells you what commands would be run, but doesn't actually build the code
    -t | --test      | Run any program whose name begins with "test". If -n is specified, tell what would be run. 
    -v | --verbose   | Output addition information

## Working With Doh

You can tweak some of the values in the *baker.doh* files to deal with special cases.

Property           | Tyoe | Description
------------------ | ---- | -----------
preferredLibraries | list | List of directory filenames that will be preferred if there is more than one containing a required symbol

More will be added in future versions.


## Copyright and License

Baker is copyrighted by Jim Belton

It is licensed under the GNU Public License, version 3. See http://www.gnu.org/licenses/gpl-3.0.en.html
