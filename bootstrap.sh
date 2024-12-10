#!/bin/bash

ROOT_DIR=$( cd -- "$( dirname -- "${BASH_SOURCE[0]}" )" &> /dev/null && pwd )

print_setup_usage()
{
    echo "Usage: source bootstrap.sh setup [server|client] [--force]"
}

setup()
{
    if [[ "$1" == "server" ]]; then
        venv_dir="$ROOT_DIR/.pz_server"
        requirements="$ROOT_DIR/setup/server-requirements.txt"
    elif [[ "$1" == "client" ]]; then
        venv_dir="$ROOT_DIR/.pz_client"
        requirements="$ROOT_DIR/setup/client-requirements.txt"
    else
        print_setup_usage
        return
    fi

    if [[ "$2" == "force" ]]; then
        if hash deactivate &> /dev/null; then
            deactivate
        fi
        rm -rf "$venv_dir"
        virtualenv -p /usr/bin/python3 "$venv_dir"
        source "$venv_dir/bin/activate"
        python3 -m pip install -r "$requirements"
    fi
    source "$venv_dir/bin/activate"
}

clean()
{
    # Virtual env clear
    rm -rf "${ROOT_DIR}/.pz_client"
    rm -rf "${ROOT_DIR}/.pz_server"

    # Cache clear
    rm -rf "${ROOT_DIR}/server/__pycache__"
    rm -rf "${ROOT_DIR}/client/__pycache__"
}

main()
{
    if [[ "${1}" == "setup" ]]; then
        if [[ "${BASH_SOURCE[0]}" == "${0}" ]]; then
            print_setup_usage
            return
        fi
        shift
        if [[ "${2}" == "--force" ]]; then
            setup $1 force
        else
            setup $1
        fi
    elif [[ "${1}" == "clean" ]]; then
        clean
    else
        echo "Unrecognized command!"
    fi
}

main $@
