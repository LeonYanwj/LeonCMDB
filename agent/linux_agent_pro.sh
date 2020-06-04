#!/bin/bash
# vim:ft=sh

log () {
   # 打印消息, 并记录到日志, 日志文件由 LOG_FILE 变量定义
   local retval=$?
   local timestamp=$(date +%Y%m%d-%H%M%S)
   local level=INFO

   echo "[$(blue_echo ${CONN_IP:-$LAN_IP})]$timestamp $BASH_LINENO   $@"
   return $retval
}

warn () {
   # 打印警告消息, 并返回0
   # 屏幕输出使用黄色字体
   local timestamp=$(date +%Y%m%d-%H%M%S)
   local level=WARN

   echo "[$(yellow_echo ${CONN_IP:-$LAN_IP})]$timestamp $BASH_LINENO   $(yellow_echo $@)"
   return 0
}

fail () {
   # 打印错误消息,并以非0值退出程序
   # 参数1: 消息内容
   # 参数2: 可选, 返回值, 若不提供默认返回1
   local timestamp=$(date +%Y%m%d-%H%M%S)
   local level=FATAL
   local retval=${2:-1}

   echo "[$(red_echo ${CONN_IP:-$LAN_IP})]$timestamp $BASH_LINENO   $(red_echo $@)" >&2
   exit $retval
}

red_echo ()      { [ "$HASTTY" != "1" ] && echo "$@" || echo -e "\033[031;1m$@\033[0m"; }
green_echo ()    { [ "$HASTTY" != "1" ] && echo "$@" || echo -e "\033[032;1m$@\033[0m"; }
yellow_echo ()   { [ "$HASTTY" != "1" ] && echo "$@" || echo -e "\033[033;1m$@\033[0m"; }
blue_echo ()     { [ "$HASTTY" != "1" ] && echo "$@" || echo -e "\033[034;1m$@\033[0m"; }
purple_echo ()   { [ "$HASTTY" != "1" ] && echo "$@" || echo -e "\033[035;1m$@\033[0m"; }
bred_echo ()     { [ "$HASTTY" != "1" ] && echo "$@" || echo -e "\033[041;1m$@\033[0m"; }
bgreen_echo ()   { [ "$HASTTY" != "1" ] && echo "$@" || echo -e "\033[042;1m$@\033[0m"; }
byellow_echo ()  { [ "$HASTTY" != "1" ] && echo "$@" || echo -e "\033[043;1m$@\033[0m"; }
bblue_echo ()    { [ "$HASTTY" != "1" ] && echo "$@" || echo -e "\033[044;1m$@\033[0m"; }
bpurple_echo ()  { [ "$HASTTY" != "1" ] && echo "$@" || echo -e "\033[045;1m$@\033[0m"; }
bgreen_echo ()   { [ "$HASTTY" != "1" ] && echo "$@" || echo -e "\033[042;34;1m$@\033[0m"; }


get_lan_ip () {
    #
    ip addr | \
        awk -F'[ /]+' '/inet/{
               split($3, N, ".")
               if ($3 ~ /^192.168/) {
                   print $3
               }
               if (($3 ~ /^172/) && (N[2] >= 16) && (N[2] <= 31)) {
                   print $3
               }
               if ($3 ~ /^10\./) {
                   print $3
               }
          }'

   return $?
}

get_win_lanip () {
    ipconfig | awk '/IP(v4)? /{
               split($NF, N, ".")
               if ($NF ~ /^192.168/) {
                   print $NF
               }
               if (($NF ~ /^172/) && (N[2] >= 16) && (N[2] <= 31)) {
                   print $NF
               }
               if ($NF ~ /^10\./) {
                   print $NF
               }
        }'
}

migrate_config () {
    sed -i "/#master: salt/c\master: $MASTER_LANIP$"  ${INSTALL_TARGET_PATH}minion
    sed -i "/^#id:/c\id: $LAN_IP" ${INSTALL_TARGET_PATH}minion
}

_install_client () {
    yum -y install /tmp/agents/*.rpm
    migrate_config
}

_stop () {
    systemctl disable salt-minion
    systemctl stop salt-minion
}

remove () {

    if [ "$UPGRADE" == "1" ]; then
        log "backup configurations for gse plugins"
        backup_config
        backup_config_v1
    fi

    log "remove old gse agent"
    _stop
    rm -rf $INSTALL_TARGET_PATH /var/{log,run,lib}/salt
    yum remove salt* zeromq  -y
}

mkfs () {

    local fsname="$1"
    if [ ! -d "$fsname" ];then
        mkdir $fsname
    fi
}

download_pkg () {
    local pkgname="$1"
    local nginx_port=$(echo -n "$PKGS_SOURCE" | sed 's/^.*://g')
    local nginx_ip=( $(echo -n "$PKGS_SOURCE" | sed 's/:[0-9]\+,\?/ /g') )
    local _contiue=false

    cd  /tmp/
    rm -vf /tmp/agents/$pkgname

    curl -o /tmp/agents/$pkg_name http://"$nginx_ip"/download/$pkg_name
    [ -s /tmp/agents/$pkgname ] && _contiue=true

    #这里一般不会执行
    if ! $_contiue; then
        curl -o /tmp/agents/$pkg_name http://"${nginx_ip}:${nginx_port}"/download/$pkg_name
    fi
    [ -s /tmp/agents/$pkgname ]

}

_start () {
    local proj=$1
    systemctl daemon-reload
    systemctl start salt-minion
    if [ "$?" -eq 0 ];then
        log "start salt-minion service success"
    else
        log "start salt-minion service failed"
    fi
}

install_agent () {
    local node_type="client"

    case $os_type in
        windows)
            log "create directory $INSTALL_TARGET_PATH/{logs,data}"
            mkdir -p $INSTALL_TARGET_PATH/{logs,data} ;;
        *)
            log "create directory /var/{log,run,lib}/salt"
            # mkdir -p /var/{log,run,lib}/salt ;;
    esac

    mkfs /tmp/agents || fail "craete directory failed"
    if [ -f /tmp/agents/$pkg_name ]; then
        rm -f /tmp/$pkg_name
        mv /tmp/agents/$pkg_name /tmp/
        download_pkg $pkg_name || fail "setup failed -- get salt package(client) failed. install abort"
    else
        download_pkg $pkg_name || fail "setup failed -- get salt package(client) failed. install abort"
    fi

    _install_${node_type}       || fail "setup failed -- install_client failed."
    _start agent               || fail "setup failed -- start gse agent node failed. (retcode: $?)"
    ok "agent(client) setup done -- install_success"

    log "remove temperary files"
}

_remove () {
    remove || fail "remove failed -- remove old version of gse agent failed."
    if $REMOVE; then
        ok "remove done -- remove_success"
        exit 0
    fi
}

install_direct_area () {
    local node_type="$1"

    pkg_name=salt-${node_type}-${os_type}-${cpu_arch}.tgz
    case $node_type in
        proxy)
            export AGENT_SETUP_PATH=$INSTALL_TARGET_PATH/proxy

            _remove

            install_python
                install_proxy
         ;;
        client|agent)
            case $os_type in
                linux|aix) export AGENT_SETUP_PATH=$INSTALL_TARGET_PATH/agent ;;
                windows) export AGENT_SETUP_PATH=$INSTALL_TARGET_PATH/gseagentw ;;
            esac

            _remove

            install_agent ;;
        *) echo "unkown node_type '$node_type'."
           usage
        ;;
    esac
}

usage () {
    echo "usage: ${0##*/} -m { proxy | client } OPTIONS"
    echo ""
    echo "OPTIONS list:"
    echo "  -h    print this help page"
    echo "  -r    uninstall"
    echo "  -m    'proxy' or 'client'"
    echo "        client: a host under the control of proxy or server"
    echo "        proxy: manager node of seperated datacenter"
    echo "  -b    bridge mode of client, client connected to proxy"
    echo "  -u    upgrade agent/proxy, with configuration reserved/migrated"
    echo "  -t    set timeout limit"
    echo "  -e    NAT ip, usefull when agent is behined a NATed firewall"
    echo ""
    echo "when BRIDGE MODE enabled"
    echo "  -i    datacenter id, valid in proxy mode. default: 2"
    echo "  -w    ip1,ip2, multi proxy server seperated by comma"
    echo "  -l    ip1,ip2, multi proxy server seperated by comma"
    echo "  -o    target host ip list file. default: /tmp/hosts.config"
    echo "        each line format like this:"
    echo "          IP PORT USERNAME IDENTITY"

    exit 0
}

set_install_path () {
    # 检查安装环境, 确定需要安装的版本.
    case $(uname -s) in
        *Linux)
            export os_type=linux

            if [ $(getconf LONG_BIT) == 64 ]; then
                cpu_arch=x86_64
            else
                cpu_arch=x86
            fi
            INSTALL_TARGET_PATH=/etc/salt/
            export LAN_IP=$(get_lan_ip | head -1)
        ;;
        *CYGWIN*)
            export os_type=windows
            export LAN_IP=$(get_win_lanip | head -1)
            if uname -s | grep -q 'WOW64'; then
                cpu_arch=x86_64
            else
                cpu_arch=x86
            fi

            INSTALL_TARGET_PATH=C:\\slat
        ;;
        *)
            fail "operating system: $(uname -o) is not supported"
        ;;
    esac

    if ! which curl >/dev/null 2>&1; then
        fail "setup failed -- command curl not found. abort"
    fi
}

REMOVE=false
BIZ_ID=0
UPGRADE=0

while getopts A:I:hrm:g:t: arg; do
    case $arg in
        h) usage ;;
        m) NODE_TYPE="$OPTARG" ;;
        r) REMOVE=true; TAG_REMOVE="-r" ;;
        I) BIZ_ID="$OPTARG" ;;
        g) PKGS_SOURCE="$OPTARG" ;;
        A) export MASTER_LANIP=( $(echo -n "$OPTARG" | sed 's/,/ /g' ) ) ;;
        t) export TIMEOUT=$OPTARG ;;
        *) usage ;;
    esac
done


set_install_path
install_direct_area $NODE_TYPE
rm -f /tmp/hosts_app.config /tmp/key_merged