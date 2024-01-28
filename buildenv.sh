#!/usr/bin/bash
# This file is generated by buildenv tool -- see https://buildenv.readthedocs.io/
# Please do not edit, changes will be lost

# Check if python is installed
if test -f /git-bash.exe; then
    _BUILDENV_PYTHON=python
else
    _BUILDENV_PYTHON=${BUILDENV_PYTHON:-python3}
fi
${_BUILDENV_PYTHON} --version 2>/dev/null 1>&2
if test $? -ne 0; then
    echo "[ERROR] ${_BUILDENV_PYTHON} is not installed"
    exit 1
fi

# Wrap to buildenv script
${_BUILDENV_PYTHON} buildenv-loader.py --from-loader=sh "$@"
_BUILDENV_RC=$?

# Check for specific RC
if test ${_BUILDENV_RC} -eq 100; then
    # Spawn shell if required
    ${SHELL} --rcfile .buildenv/shell.sh
    _BUILDENV_RC=$?
elif test ${_BUILDENV_RC} -gt 100; then
    # Execute command if required (and command script found)
    _BUILDENV_CMD=.buildenv/command.${_BUILDENV_RC}.sh
    if test -f ${_BUILDENV_CMD}; then
        ${SHELL} -c ${_BUILDENV_CMD}
        _BUILDENV_RC=$?
        rm ${_BUILDENV_CMD}
    fi
fi

# Forward RC
exit ${_BUILDENV_RC}

