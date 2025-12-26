#!/bin/bash

function _fmt () {
  local color_ok="\x1b[32m"
  local color_bad="\x1b[31m"
  
  local color="${color_bad}"
  if [ "${1}" = "debug" ] || [ "${1}" = "info" ] || [ "${1}" = "notice" ]; then
    color="${color_ok}"
  fi
  
  local color_reset="\x1b[0m"
  if [[ "${TERM}" != "xterm"* ]] || [ -t 1 ]; then
    # Don't use colors on pipes or non-recognized terminals
    color=""; color_reset=""
  fi
  #echo -e "$(date -u +"%Y-%m-%d %H:%M:%S UTC") ${color}$(printf "[%9s]" ${1})${color_reset}";
  echo -e "${color}$(printf "[%9s]" ${1})${color_reset}";
}

function error () {
  echo "$(_fmt error) ${@}" 1>&2 || true;
}
function warning () {
  echo "$(_fmt warning) ${@}" 1>&2 || true;
}
function info () {
  echo "$(_fmt info) ${@}" 1>&2 || true;
}
function debug () {
  echo "$(_fmt debug) ${@}" 1>&2 || true;
}