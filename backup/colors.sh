#!/bin/sh
# 文字颜色
COLOR_CYAN="\033[36;49;1m"
COLOR_GREEN="\033[32;49;1m"
COLOR_RED="\033[31;49;1m"
COLOR_BACK="\033[39;49;0m"

# 蓝色 文字
function _echo()
{
echo -e "${COLOR_CYAN}${1}${COLOR_BACK}"
}

# 绿色 通过 Correctness
function _cecho()
{
echo -e "${COLOR_GREEN}${1}${COLOR_BACK}"
}

# 红色 错误 error
function _eecho()
{
echo -e "${COLOR_RED}${1}${COLOR_BACK}"
}

# 默认颜色
echo -e "${COLOR_BACK}xx${COLOR_BACK}"
_echo "dir"
_cecho "success"
_eecho "error"
