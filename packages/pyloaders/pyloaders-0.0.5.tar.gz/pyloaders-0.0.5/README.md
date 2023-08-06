pyloaders
=========

Basic animated ASCII loaders for Python scripts. Python 2 & 3 compatible.

- Spinning Loader
- Text Loader
- Bar Loader
- Progress Loader

## Installation

```bash
pip install pyloaders
```

#### From Source

```bash
git clone https://gitlab.com/ml394/pyloaders.git
cd pyloaders
python setup.py install
```

## Usage

All loaders are declared by calling `LoaderClass(<arguments>)`

#### Arguments

| Option        | Description                         | Type  | Choices                  | Default   | Valid For           |
|---------------|-------------------------------------|-------|--------------------------|-----------|---------------------|
| text          | Text displayed while loading        | str   |                          | 'Loading' | Text, Spinning      |
| size          | Full width of loader                | str   | small, medium, large     | 'medium'  | Text, Bar, Progress |
| character     | ASCII value used in loader          | str   | . = * > ~ # @ $ + ! ? ,  | '.' / '=' | Text, Bar, Progress |
| speed         | Time between loader paints          | float |                          | .25       | Text, Spinning, Bar |
| duration      | Runtime of fixed loader, in seconds | int   |                          | 10        | Text, Spinning, Bar |
| direction     | Initial direction of moving loader  | str   | ltr, rtl                 | 'ltr'     | Text, Bar           |
| animation     | Continuous or oscillating movement  | str   | loop, bounce             | 'loop'    | Text, Bar           |
| colour        | Terminal colour support required    | str   | blue, green, yellow, red | None      | ALL                 |
| style         | Terminal styles support required    | str   | header, bold, underline  | None      | ALL                 |
| complete_text | Text displayed after loader ends    | str   |                          | 'Done!'   | ALL                 |
| start         | Progress loader start position      | int   |                          | 0         | Progress            |
| total         | Progress loader total count         | int   |                          | 100       | Progress            |

### Indeterminate

**Available Classes:** SpinningLoader, TextLoader, BarLoader

Run as threads which can be started and stopped dynamically by you at any stage.
- To start a loader, call its `start()` method.
- After you have completed your tasks, call the loader's `stop()` method to terminate the thread.
- If you have set a fixed _duration_ of the loader, call the `run()` method to run the loader for the set amount of time.

#### Threaded
```python
from loaders import TextLoader

loader = TextLoader()
loader.start()
# Perform some tasks
loader.stop()
```

#### Fixed Duration
```python
from loaders import TextLoader

fixed_loader = TextLoader(duration=10)
fixed_loader.run() # Pauses program execution and runs loader for 10s
```

**Output**
```
/ Loading...        # SpinningLoader

.....Loading...     # TextLoader

|   ======    |     # BarLoader
```

**Remember**: Don't try to start more than one loader at the same time!

### Determinate

**Available Classes:** ProgressLoader

Used to measure the completion progress of a loop or function.

When you initialize a `ProgressLoader` object, you should specify the total number of iterations that will be performed in your loop as the `total` argument.

On each iteration, call the loader's `progress(n)` method, where `n` is the current iteration count, to update the progress bar in the terminal.

```python
from loaders import ProgressLoader

loader = ProgressLoader(total=10)
for i in range(10):
    # Perform some task each loop
    loader.progress(i)
```

**Output**
```
|==========          | 50%
```

**Remember:** Don't print anything to the console while the loader is running!

### Bash
*New in version 0.0.5*

You can now start a loader for shell commands
```
$ load some --shell command
[    ========    ]
```

## Tests

There is a small test suite that uses the **pytest** module.
1. Clone the repository
2. Install pytest and dependencies
3. Run pytest from project folder

```bash
git clone https://gitlab.com/ml394/pyloaders.git
cd pyloaders
pip install -r requirements.txt
pytest
```

### Examples

An visual example can be performed by running `example.py` from the project directory.

This will run a suite of example loaders specified in the file for 5s each. By default, the indeterminate examples are run on fixed durations. To run them as threads, use the optional `thread` argument.

```bash
# Fixed duration
python example.py

# Threaded
python example.py thread
```

## Contributing

To contribute to this project, clone master and create your own development branch.
```bash
git clone https://gitlab.com/ml394/pyloaders.git
git checkout -b <feature-name>
```

Push your branch remotely, and create a merge request to master so we can review your code.

If the merge request is approved, your new feature will be merged and pushed for the next release.

### To Do

- [x] Loader colours / styles
- [x] CI/CD Pipeline
- [ ] API Documentation
- [ ] Print output while loader running

## Donate

BTC donations (no matter how tiny) accepted at wallet address:

`1PSWQrgbagNARvtum6pGS7rPUub4YiLmzX`
