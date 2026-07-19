"""
Logging helpers for the simple-empirical-Scons-demo SCons pipeline.

This module mirrors two pieces of gslab_python/gslab_scons:

  * gslab_scons/builders/gslab_builder.py
      - GSLabBuilder.execute_system_call() records a start/end time around
        each script call; timestamp_log() prepends those timestamps to the
        builder's log file.
  * gslab_scons/log.py
      - start_log() / end_log() record the overall SCons build process,
        writing a "New build" start line, an end line, and merging the
        per-step builder logs into a single sconstruct.log.

Here we do the same for the demo's plain env.Command() pipeline:

  * Per-step logs  -> <step>/temp/Sconscript_<step_name>.log
      - scons_log.py start <log>          # writes the "created" timestamp (truncates)
      - the SCons action redirects the script's stdout/stderr with >> ... 2>&1
      - scons_log.py end <log>            # appends the "completed" timestamp
  * Top-level log   -> Sconstruct.log  (next to SConstruct)
      - sconstruct_start <log>            # called from SConstruct at parse time
      - sconstruct_end <log> <step_log>...# called via atexit, merges steps

All timestamps use the gslab convention '{YYYY-MM-DD HH:MM:SS}' so that the
Sconstruct.log merge can identify them, just as gslab_scons/log.py does.

Usage (SCons actions run from the project root, so the script is invoked as
``python modules/scons_log.py ...``).
"""
import os
import sys
from datetime import datetime


def current_time():
    """Return the current time as 'YYYY-MM-DD HH:MM:SS' (gslab convention)."""
    return datetime.now().strftime('%Y-%m-%d %H:%M:%S')


# --------------------------------------------------------------------------
# Per-step builder logs (mirror gslab_builder.timestamp_log)
# --------------------------------------------------------------------------
def stamp_start(log_path):
    """Truncate the log and write the 'created' timestamp (start of step)."""
    directory = os.path.dirname(log_path)
    if directory:
        os.makedirs(directory, exist_ok=True)
    with open(log_path, 'w', encoding='utf-8') as f:
        f.write('*** Builder log created: {%s}\n' % current_time())


def stamp_end(log_path):
    """Append the 'completed' timestamp (end of step)."""
    with open(log_path, 'a', encoding='utf-8') as f:
        f.write('*** Builder log completed: {%s}\n' % current_time())


# --------------------------------------------------------------------------
# Top-level Sconstruct.log (mirror gslab_scons/log.start_log / end_log)
# --------------------------------------------------------------------------
def sconstruct_start(log_path):
    """Begin Sconstruct.log with a 'New build' start line (parse time)."""
    directory = os.path.dirname(log_path)
    if directory:
        os.makedirs(directory, exist_ok=True)
    with open(log_path, 'w', encoding='utf-8') as f:
        f.write('*** New build: {%s} ***\n' % current_time())


def sconstruct_end(log_path, step_logs):
    """Finish Sconstruct.log: merge step logs, then write 'Build completed'.

    Mirrors gslab_scons/log.end_log, which appends each builder log (in
    dependency order) to sconstruct.log and ends with a completion line.
    """
    with open(log_path, 'a', encoding='utf-8') as f:
        for step_log in step_logs:
            if not os.path.isfile(step_log):
                # Step was not rebuilt this run (up-to-date) or failed to log.
                f.write('\n%s\n[log not found this run]\n' % step_log)
                continue
            f.write('\n' + '=' * 70 + '\n')
            f.write(step_log + '\n')
            f.write('=' * 70 + '\n')
            with open(step_log, 'r', encoding='utf-8', errors='replace') as g:
                f.write(g.read())
        f.write('\n*** Build completed: {%s} ***\n' % current_time())


# --------------------------------------------------------------------------
# CLI entry point used by SCons actions
# --------------------------------------------------------------------------
def main(argv):
    if len(argv) < 2:
        sys.stderr.write('usage: scons_log.py <start|end|sconstruct_start|'
                         'sconstruct_end> <log> [step_log ...]\n')
        return 2
    cmd = argv[1]
    if cmd == 'start' and len(argv) == 3:
        stamp_start(argv[2])
    elif cmd == 'end' and len(argv) == 3:
        stamp_end(argv[2])
    elif cmd == 'sconstruct_start' and len(argv) == 3:
        sconstruct_start(argv[2])
    elif cmd == 'sconstruct_end' and len(argv) >= 3:
        sconstruct_end(argv[2], argv[3:])
    else:
        sys.stderr.write('scons_log.py: bad arguments: %s\n' % ' '.join(argv[1:]))
        return 2
    return 0


if __name__ == '__main__':
    raise SystemExit(main(sys.argv))
