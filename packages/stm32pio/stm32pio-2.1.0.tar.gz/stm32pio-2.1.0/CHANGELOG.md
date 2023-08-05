# stm32pio changelog

## ver. 0.1 (30.11.17)
 - Initial version

## ver. 0.2 (14.01.18)
 - New: this changelog and more comments :)
 - Fixed: compatible with new filename politics (see PlatformIO issue #1107)
   (`inc` now must be `include` so we add option to `platformio.ini`)
 - Changed: use os.path.normpath() instead of manually removing trailing `/`

## ver. 0.21 (18.01.18)
 - New: checking board name before PlatformIO start

## ver. 0.4 (03-04.04.18)
 - New: hide CubeMX and PlatformIO stdout output
 - New: shebang
 - New: choose your favourite editor with `--start-editor` option (replaces `--with-atom`)
 - New: logging module
 - New: more checks
 - New: `settings.py` file
 - New: cross-platform running
 - New: debug output (verbose `-v` mode)
 - New: `README.md` and more comments
 - Fixed: remove unnecessary imports
 - Fixed: command to initialize PlatformIO project (remove double quotation marks)
 - Changed: many architectural improvements
 - Changed: documentation improvements

## ver. 0.45 (04-05.04.18)
 - New: introducing unit-tests for the app
 - New: clean-up feature

## ver. 0.5 (07.04.18)
 - New: more comments
 - New: screenshots for the usage example
 - Fixed: many small fixes and improvements
 - Changed: test now is more isolated and uses `./stm32pio-test/stm32pio-test.ioc` file

## ver. 0.7 (05-07.11.18)
 - New: Windows support!
 - New: new editors support (Sublime Text)
 - New: more comments and docstrings
 - New: more checks to improve robustness
 - New: if `__name__ == '__main__'` block
 - New: new test: build generated project
 - New: new test: run editors
 - New: new test: user's code preservation after the code regeneration
 - New: clean run for test cases (implemented using decorator)
 - Fixed: compatible with latest PlatformIO project structure (ver 3.6.1)
 - Fixed: many small fixes and improvements
 - Changed: `java_cmd` parameter in `settings.py` (simple `java` by default)
 - Changed: move to double-quoted strings
 - Changed: remove `_getProjectNameByPath()` function (replaced by `os.path.basename()`)
 - Changed: vast f-strings usage
 - Changed: test `.ioc` file is updated to the latest STM32CubeMX version (4.27.0 at the moment)
 - Changed: use `os.path.join()` instead of manually composing of paths
 - Changed: use `with ... as ...` construction for opening files
 - Changed: 120 chars line width
 - Changed: PEP 8 conformity: variables and functions naming conventions
 - Changed: PEP 8 conformity: multi-line imports
 - Changed: `miscs.py` module is renamed to `util.py`

## ver. 0.73 (10-11.02.19)
 - New: use more convenient Python project structure
 - New: package can be install using setuptools
 - New: TODO list
 - New: `--directory` option is now optional if the program gets called from the project directory
 - Fixed: license copyright
 - Fixed: 'dot' path will be handle successfully now
 - Fixed: bug on case insensitive machines
 - Fixed: bug in tests that allowing to pass the test even in failure situation
 - Changed: test `.ioc` file is updated to the latest STM32CubeMX version (5.0.1 at the moment)
 - Changed: documentation improvements

## ver. 0.74 (27.02.19)
 - New: new internal `_get_project_path()` function (more clean main script)
 - New: optional `--with-build` option for `new` mode allowing to make an initial build to save a time
 - Changed: `util.py` functions now raising the exceptions instead of forcing the exit
 - Changed: test `.ioc` file is updated to the latest STM32CubeMX version (5.1.0 at the moment)
 - Changed: documentation improvements

## ver. 0.8 (09.19)
 - New: `setup.py` can now install executable script to run `stm32pio` from any location
 - New: stm32pio logo/schematic
 - New: add PyCharm to `.gitignore`
 - New: add clear TODOs for the next release (some sort of a roadmap)
 - New: single `__version__` reference
 - New: extended shebang
 - New: add some new tests (`test_build_should_raise`, `test_file_not_found`)
 - Fixed: options `--start-editor` and `--with-build` can now be used both for `new` and `generate` commands
 - Fixed: import scheme is now as it should be
 - Changed: migrate from `os.path` to `pathlib` as much as possible for paths management (as a more high-level module)
 - Changed: `start editor` feature is now starting an arbitrary editor (in the same way as you do it from the terminal)
 - Changed: take outside `platformio` command (to `settings.py`)
 - Changed: screenshots were actualized for recent CubeMX versions
 - Changed: logging output in standard (non-verbose) mode is simpler
 - Changed: move tests in new location
 - Changed: revised and improved tests
 - Changed: actualized `.ioc` file and clean-up the code according to the latest STM32CubeMX version (5.3.0 at the moment)
 - Changed: revised and improved util module

## ver. 0.9 (11-12.19)
 - New: tested with Python3 version of PlatformIO
 - New: `__main__.py` file (to run the app as module (`python -m stm32pio`))
 - New: 'init' subcommand (initialize the project only, useful for the preliminary tweaking)
 - New: introducing the OOP pattern: we have now a Stm32pio class representing a single project (project path as a main identifier)
 - New: projects now have a config file stm32pio.ini where the user can set the variety of parameters
 - New: `state` property calculating the estimated project state on every request to itself (beta). It is the concept for future releases
 - New: STM32CubeMX is now started more silently (without a splash screen)
 - New: add integration and CLI tests (sort of)
 - New: testing with different Python versions using pyenv (3.6+ target)
 - New: `test_start_editor` is now preliminary automatically checks whether an editor is installed on the machine
 - New: more typing annotations
 - Fixed: the app has been failed to start as `python app.py` (modify `sys.path` to fix)
 - Changed: `main()` function is now fully modular: can be run from anywhere with given CLI arguments (will be piped forward to be parsed via `argparse`)
 - Changed: rename `stm32pio.py` -> `app.py` (stm32pio is the name of the package as a whole)
 - Changed: rename `util.py` -> `lib.py` (means core library)
 - Changed: logging is now more modular: we do not set global `basicConfig` and specify separated loggers for each module instead
 - Changed: more clear description of steps to do for each user subcommand by the code
 - Changed: get rid of `print()` calls leaving only logging messages (easy to turn on/off the console output in the outer code)
 - Changed: reimagined API behavior: where to raise exceptions, where to return values and so on
 - Changed: more clean API, e.g. move out the board resolving procedure from the `pio_init()` method and so on
 - Changed: test fixture is now moved out from the repo and is deployed temporarily on every test run
 - Changed: set-up and tear-down stages are now done using `unittest` API
 - Changed: actualized `.ioc` file for the latest STM32CubeMX version (5.4.0 at the moment)
 - Changed: improved help, docs, comments

## ver. 0.95 (15.12.19)
 - New: re-made `patch()` method: it can intelligently parse `platformio.ini` and substitute necessary options. Patch can now be a general .INI-format config
 - New: `test_get_state()`
 - New: upload to PyPI
 - New: use regular expressions to test logging output format for both verbose and normal modes
 - Fix: return `-d` as an optional argument to be able to execute a short form of the app
 - Changed: subclass `ConfigParser` to add `save()` method (remove `Stm32pio.save_config()`)
 - Changed: resolve more TO-DOs (some cannot be achieved actually)
 - Changed: improve `setup.py`
 - Changed: replace traceback.print to `logging` functionality
 - Changed: no more mutable default arguments
 - Changed: use `inspect.cleandoc` to place long multi-line strings in code
 - Changed: rename `_load_config_file()`, `ProjectState.PATCHED`
 - Changed: use `interpolation=None` on `ConfigParser`
 - Changed: check whether there is already a `platformio.ini` file and warn in this case on PlatformIO init stage
 - Changed: sort imports in the alphabetic order
 - Changed: use `configparser` to test project patching

## ver. 0.96 (17.12.19)
 - Fix: `generate_code()` doesn't destroy the temp folder after execution
 - Fix: improved and actualized docs, comments, annotations
 - Changed: print Python interpreter information on testing
 - Changed: move some asserts inside subTest context managers
 - Changed: rename `pio_build()` => `build()`
 - Changed: take out to the `settings.py` the width of field in a log format string
 - Changed: use file statistic to check its size instead of reading the whole content
 - Changed: more logging output
 - Changed: change some methods signatures to return result value

## ver. 1.0 (06.03.20)
 - New: introduce GUI version of the app (beta)
 - New: redesigned stage-state machinery - integrates seamlessly into both CLI and GUI worlds. Python `Enum` represents a single stage of the project (e.g. "code generated" or "project built") while the special dictionary unfolds the full information about the project i.e. combination of all stages (True/False). Implemented in 2 classes - `ProjectStage` and `ProjectState`, though the `Stm32pio.state` property is intended to be a user's getter. Both classes have human-readable string representations
 - New: related to previous - `status` CLI command
 - New: `util.py` module (yes, now the name matches the functionality it provides)
 - New: logging machinery - adapting for more painless embedding the lib in another code. `logging.Logger` objects are now individual unique attributes of every `Stm32pio` instance so it is possible to distinguish which project is actually produced a message (not so useful for a current CLI version but for other applications, including GUI, is). `LogPipe` context manager is used to redirect `subprocess` output to the `logging` module. `DispatchingFormatter` allows to specify different `logging`' formatters depending on the origin of the log record. Substituted `LogRecordFactory` handles custom flags to `.log()` functions family
 - Changed: imporoved README
 - Changed: `platformio` package is added as a requirement and is used for retrieving the boards names (`util.py` -> `get_platformio_boards()`). Expected to become the replacement for all PlatformIO CLI calls
 - Changed: Markdown markup for this changelog
 - Changed: bump up `.ioc` file version
 - Changed: removed final "exit..." log message
 - Changed: removed `Config` subclass and move its `save()` method back to the main `Stm32pio` class. This change serves 2 goals: ensures consistency in the possible operations list (i.e. `init`, `generate`, etc.) and makes possible to register the function at the object destruction stage via `weakref.finilize()`
 - Changed: removed `_resolve_board()` method as it is not needed anymore
 - Changed: renamed `_load_config_file()` -> `_load_config()` (hide implementation details)
 - Changed: use `logger.isEnabledFor()` instead of manually comparing logging levels
 - Changed: slightly tuned exceptions (more specific ones where it make sense)
 - Changed: rename `project_path` -> `path`
 - Changed: actualized tests, more broad usage of the `app.main()` function versus `subprocess.run()`

## ver. 1.10 (15.03.20)
 - New: table of contents for the README
 - New: GitHub project wiki
 - New: `-q/--quiet` option for the `clean` CLI command. The command now by default warns the user about the content deletion
 - New: embedding example (minimal reproducible code snippet, easier than the full CLI or GUI versions)
 - New: show the exception name too when the global error has been caught (`stm32pio/app.py`)
 - New: sanitize `--start-editor` option value using `shlex.quote()`
 - New: parse `platformio.ini` to establish its correctness when checking for project states (`ProjectStage.PIO_INITIALIZED`, `ProjectStage.PATCHED`)
 - New: projects are now portable. The user specifying paths relatively to the project folder and using variables (we still don't use `configparser` interpolation but there is no need in it). The backwards compatibility with the old-style config format has been preserved though those projects still will be non-portable unless you manually edit a config
 - New: analyze STM32CubeMX output to detect errors on execution. This utility does not necessarily returns non-zero code when some error was happened (e.g. `.ioc` and app versions mismatch and so on), and just shows a dialog
 - New: `platformio_ini_config` `Stm32pio` instance property returning current `platformio.ini` parsed `ConfigParser` value. Used in some internal routines such as correctness determination and doesn't have to be used by the library user
 - New: `LogPipe` now returns "remote control" `LogPipeRC` - small utility class holding the writable stream and the reference to the string accumulating all incoming messages. It can be accessed later, in the end of the context manager, to store and analyze all the output
 - New: some new tests, I think, but I do not remember as all the tests are now moved to the new files :)
 - Fixed: warnings appearing during the `pio_build()` execution were suppressed
 - Changed: tests are moved out to the root of the repo and excluded from the distribution bundle
 - Changed: went back to the PlatformIO CLI as a single point to interact with PlatformIO (remove `platformio` package imports and dependencies) (the reason is crushes when the pio is not isolated in a separated subprocess). Use PlatformIO JSON format output to get and filter boards
 - Changed: remove `required=False` from `argparse` commands as it is a default (and even recommended) value anyway
 - Changed: remove the unnecessary logging setup when no arguments were given to the program (CLI version)
 - Changed: separate `Stm32pio` arguments onto 2 categories: project parameters and instance options and use dictionaries for them. First one has now the same form as the project config `configparser.ConfigParser` and merging into the default and file settings on the project creation. Instance options are more related to the programmatic instance itself and contains currently 2 options - `logger` and `save_on_destruction`
 - Changed: use `append()` instead of `insert()` to modify `sys.path`
 - Changed: when raising the exceptions use more elegant expressions (e.g. `raise FileNotFoundError(file)` instead of `raise FileNotFoundError("file FILE was not found")`). Use `pathlib.Path().resolve(strict=True)` where appropriate to shorten the code

## ver. 1.20 (18.04.20)
 - New: GUI. System tray notifications when the main window is not in the foreground (can be turned off in the settings)
 - New: GUI. Drag-and-drop folder(s) to add
 - New: GUI. README, screenshots, diagrams
 - New: GUI. Catch projects duplication on appending
 - New: GUI. Mark the list item when the action is done and it is not a current item
 - New: GUI. Highlight the actions that were picked for the series
 - New: GUI. setuptools `extras` option to install the GUI version via pip
 - New: GUI. Wrap imports into `try...catch`
 - New: GUI. Reset settings feature
 - New: GUI. New `ProjectListItem` members: `_from_startup` flag, `_current_action` string with corresponding properties and signals
 - New: GUI. More extensive use of the `typing` annotations
 - New: GUI. Allow to pass extra setter functions to the `Settings` which will be called on the value change
 - New: allow to specify the `.ioc` file instead of the directory. Check that `.ioc` is a non-empty text file
 - Fixed: GUI. Projects are not destructed until the app shutdown
 - Fixed: GUI. Settings dialog doesn't correctly represents the parameters
 - Fixed: GUI. Settings on Windows (case-sensitive vs insensitive situation)
 - Fixed: GUI. List item loader
 - Fixed: GUI. Flaws when index changes
 - Changed: GUI. Clean the logs too when invoking the 'Clean' action
 - Changed: GUI. Stop the chain of commands if someone drops -1 or an exception
 - Changed: GUI. Use Qt StateMachine to control the visual appearance of the project action button
 - Changed: GUI. Rename the module `stm32pio-gui` -> `stm32pio_gui`
 - Changed: GUI. Better printing of exception messages
 - Changed: GUI. Revised finalizer (similar to core version)
 - Changed: GUI. Cache `state` and `state.current_stage` both for back- and frontend to reduce IO operations
 - Changed: GUI. rename `ProjectActionWorker` -> `Worker` (as it is used for the variety of tasks) and some of its internals
 - Changed: GUI. Pass `Settings` prefix as an argument for the constructor
 - Changed: GUI. Move more stuff inside the `main()` function, less global variables
 - Changed: exclude screenshots from the setuptools bundle
 - Changed: restructure TODO.md into sections
 - Changed: remove `from __future__ import annotations` statements

## ver. 1.21 (19.04.20)
 - Fixed: GUI. All resorce paths are now reliably treated both for QML and Python
 - Changed: README installation process actualized

## ver. 1.30 (05.05.20)
 - New: `examples` folder (currently, only an embedding one (updated and moved from the wiki page))
 - New: `docs` folder with some useful internal descriptions (currently, only a logging schematic (with sources))
 - New: issues guide for GitHub (OS, content of the config, project tree, enable verbose, etc.)
 - New: GUI. Show the app version in "About" dialog
 - New: GUI. Handle a theoretical app loading error
 - New: GUI. Notify a user that the "board" parameter is empty
 - New: GUI. The app can be started from CLI
 - New: GUI. `ProjectListItem.fromStartup` property
 - New: GUI. Expose projects' `config` to QML
 - New: Tests. Preserving user files and folders on regeneration
 - New: Tests. 'verbose' and 'non-verbose' tests as `subTest` (also `should_log_error_...`)
 - New: Inform a user that given parameters have overridden the config ones
 - Fixed: GUI. `TypeError: Cannot read property 'actionRunning' of null` (deconstruction order) (on project deletion only)
 - Fixed: GUI. The app now can handle as many projects as needed (use QML `DelegateModel` to store state in the `ListView` delegate)
 - Fixed: #13 (new parsing algo to analyze the CubeMX output)
 - Changed: improved `typing` annotations
 - Changed: wrap imports into `try...except`
 - Changed: new README logo, add sources (draw.io)
 - Changed: GUI. Icons instead of a text for "Clean", "Open editor"
 - Changed: GUI. Gray out "stage" line in all projects except current
 - Changed: GUI. 2 types of logging formatters for 2 verbosity levels
 - Changed: GUI. More general `goToProject` signal instead of `duplicateFound`
 - Changed: GUI. Projects list is now saves to `Settings` in a separate thread using `QThreadPool` and `saveInSettings()` method
 - Changed: GUI. `ProjectsList.each_project_is_duplicate_of` generator
 - Changed: GUI. Optimized project' `state` handling
 - Changed: GUI. Insert board ID from config, if there is one, focus on that input field by default
 - Changed: logging mechanics is remade from scratch:
    - add `stm32pio.app.setup_logging()`, `should_setup_logging` argument fo `stm32pio.app.setup_main()`. This also fixes annoying logging errors on testing because the loggers interfere with each other
    - `stm32pio.util.ProjectLoggerAdapter()` subclass as an individual logger for every project
    - add `stm32pio.util.log_current_exception()`
    - get rid of `log_record_factory` substitution
    - add `stm32pio.util.Verbosity` entity (enum). Acts like an additional degree of freedom for the logging setup
    - rewritten `stm32pio.util.DispatchingFormatter`
    - GUI. New `BuffersDispatchingHandler()` class
    - and some others (see block schema)
 - Changed: better parameters and configs merging
 - Changed: make `platformio_ini_is_patched` a property instead of function
 - Changed: improved in-code docs

## ver 2.0.0 (28.10.20)
 - New: introducing CI/CD via Azure Pipelines. I tried to make as "general" system as possible with isolated environments, reproducible builds, etc. Due to a number of such a different tools in use and scattered infrastructure around them this task is very complex and the current configuration is far from ideal though
 - New: new project structure. All packages (core, CLI, GUI) are consolidated under the common `stm32pio` Python _namespace_
 - New: app version is completely removed from the repo and is "computed" at build-time from the VCS (GIT) current tag (using [setuptools_scm](https://github.com/pypa/setuptools_scm)). At run-time the version obtaining process depends: for newer Python it can be retrieved from a package metadata, for older one there is an auto-generated `version.py` file with a value stored in it
 - New: support multiple test fixtures to test against a different targets (e.g. lightweight `nucleo_f031k6` project + real-life `f103` and so on)
 - New: new build system. Use modern tools such as `pyproject.toml`, declarative `setup.cfg`, PEP-517 and so on. However in the middle of the development process it became evident that such a workflow is still early and not so common and there are simply not enough tools to implement it gracefully (e.g. no official tool to build both `dist` source tarball and `wheel`)
 - New: CLI. `patch` command. With this function now all meaningful (for end-user) methods of the `Stm32pio` class are mapped by CLI commands and match corresponding buttons from the GUI version so the similar workflow can be applied:
    - Initialize - `stm32pio init`
    - Generate - `stm32pio generate`
    - Init PlatformIO - `platformio project init`
    - Patch - `stm32pio patch`
    - Build - `platformio run`
 - New: CubeMX now can be invoked directly, without Java command need to be specified
 - New: add dedicated `initialized` signal to `ProjectListItem`
 - New: basic GUI tests (just make sure all imports are fine and the app at least starts)
 - Fixed: revise config handling: more robust and straightforward procedure to merge the final runtime config from different sources (fix the reported [problem](https://community.platformio.org/t/platformio-for-stm32-and-cubemx-include-error/10984/11)). Adjust corresponding test
 - Fixed: GUI. Add `project.lastActionSucceed` property to fix some visual behavior (bold borders remains after an error)
 - Changed: migrate to [Semantic Versioning](https://semver.org) (2.0.0). The next version (i.e. this one) was supposed to be 1.40 so with semver – 1.4.0. This can be confusing for some automatic tools in the future to correctly find out which version is latter though so this version will be marked with 2.0.0 tag to start things over
 - Changed: remove board absence warning in `Stm32pio` constructor (this should be done outside)
 - Changed: take out to the `settings.py` a strings that we looked for to determine successful CubeMX code generation
 - Changed: use newer `platformio project init` command, use verbose versions of CLI arguments

## ver 2.1.0
 - New: "validate environment" API. Allows to quickly verify tools specified in the config (+ corresponding test). Currently, implemented only for the CLI version
 - New: store the most recent exception in the `last_error` config file parameter (currently CLI-only) (+ corresponding test)
 - New: add shorthands for all CLI options (single-letters, e.g. `-c/--with-build`)
 - New: ignore list settings API: specify files/folders/patterns to ignore during the cleanup (hence, new `clean()` method, tests)
 - New: alternatively, use `git clean` as a removal tool
 - New: API to store the current project folder' content as ignore list in the config file
 - New: CONTRIBUTING.md guide (more like developing notes actually)
 - New: COMMANDS.md reference
 - New: CONFIG.md reference
 - New: project config reference (a little too many parameters now)
 - New: Python 3.9 CI runner
 - New: log when the config is merging with another one (DEBUG verbosity level)
 - New: handle filenames with whitespaces (both tools/project files) (#21)
 - Fixed: `clean()` method doesn't look for the determined `.ioc` file but does it by itself which can cause some unwanted behavior (potential data loss)
 - Fixed: remove done/forgotten TODOs
 - Fixed: update embedding example to match the current API
 - Fixed: `setup.cfg`: specify supported PySide2 version
 - Fixed: `setup.cfg`: PyPA parsing issues
 - Fixed: revert default CubeMX paths that seems more widespread among users
 - Fixed: GUI. Recursive layout warning in Settings window
 - Fixed: GUI. Remove the `ProjectID` parameter for the `initialized` signal to get rid of the annoying Shiboken overflow error
 - Changed: bump up CubeMX, packages, test `.ioc` file, PlatformIO versions (both for local and CI builds)
 - Changed: a completely revised documentation/examples/TODOs structure
 - Changed: spawn project-state-related code to the `state.py` module
 - Changed: spawn logging-related code to the `logging.py` module
 - Changed: separate config from the main class (new `config.py` module)
 - Changed: rename `lib.py` -> `project.py` module
 - Changed: move available config "None" options to the `settings` module (`none_options`)
 - Changed: separate CubeMX invoking code (new project's private `_cubemx_execute_script()` method)
 - Changed: edit output behavior in case of occurred error in the `generate_code()` function
 - Changed: do not cast strings where we can use path-like objects
 - Changed: pretty config printer (`__str__()` implementation, just `print(project.config)`, that's all)
 - Changed: remove `util.configparser_to_dict()` function (`ConfigParser` is already conforms with mapping protocol)
 - Changed: takeout valid user response options to `settings.py` (`yes_options`/`no_options`)
 - Changed: group and move CI-related code in the `settings.py`
 - Changed: remove `f"{STAGE_PATH.name}.ioc"` occurrences in tests
 - Changed: move `test_clean()` to unit tests
 - Changed: GUI. Remove `go_to_this` option for the `addListItem` method (instead invoke on the list model)
 - Changed: GUI. Implicitly pass the parent to the project constructor in `addListItem` method
