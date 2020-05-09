#!/bin/bash



_install_client () {

    if [ "$UPGRADE" == "1" ]; then
        log "migrate configurations to new locationo"
        migrate_config
        migrate_config_v1
    fi

    if [ -f plugins/bin/gsecmdline ]; then
        ln -sf $PWD/plugins/bin/gsecmdline /usr/bin/gsecmdline
    else
        cp plugins/bin/gsecmdline.exe ${AGENT_SETUP_PATH%/gse*}/Windows/System32/
    fi
}

download_pkg () {
    local pkgname="$1"
    local nginx_port=$(echo -n "$PKGS_SOURCE" | sed 's/^.*://g')
    local nginx_ip=( $(echo -n "$PKGS_SOURCE" | sed 's/:[0-9]\+,\?/ /g') )
    local _contiue=false

    cd  /tmp
    rm -vf /tmp/$pkgname

    curl -o /tmp/agents/$pkg_name http://"$nginx_ip"/download/$pkg_name
    [ -s /tmp/$pkgname ] && _contiue=true

    #这里一般不会执行
    if ! $_contiue; then
        for ip in ${nginx_ip[@]} ${nginx_wanip[@]}; do
            curl -o /tmp/agents/$pkg_name http://"$nginx_ip"/download/$pkg_name
            [ -s /tmp/$pkgname ] && break
        done
    fi

    cd $OLDPWD
    [ -s /tmp/$pkgname ]
}

install_agent () {
    local node_type="client"

    case $os_type in
        windows)
            log "create directory $INSTALL_TARGET_PATH/{logs,data}"
            mkdir -p $INSTALL_TARGET_PATH/{logs,data} ;;
        *)
            log "create directory /var/{log,run,lib}/slat"
            mkdir -p /var/{log,run,lib}/gse ;;
    esac

    if [ -f /tmp/agents/$pkg_name ]; then
        rm -f /tmp/$pkg_name
        mv /tmp/agents/$pkg_name /tmp/
    else
        download_pkg $pkg_name || fail "setup failed -- get gse package(client) failed. install abort"
    fi

    _install_${node_type}       || fail "setup failed -- install_client failed."
    _start agent               || fail "setup failed -- start gse agent node failed. (retcode: $?)"
    ok "agent(client) setup done -- install_success"

    log "remove temperary files"
    rm -rf /tmp/gse_* /tmp/byproxy
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
            INSTALL_TARGET_PATH=/etc/slat/
        ;;
        *CYGWIN*)
            export os_type=windows
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

    if ! which wget >/dev/null 2>&1; then
        fail "setup failed -- command wget not found. abort"
    fi
}

DIRECT=true
REMOVE=false
CLOUD_ID=2
BIZ_ID=0
QQ_ONLY=0
UPGRADE=0

while getopts A:D:E:C:I:je:t:uhrbm:i:w:l:o:g: arg; do
    case $arg in
        h) usage ;;
        m) NODE_TYPE="$OPTARG" ;;
        r) REMOVE=true; TAG_REMOVE="-r" ;;
        b) DIRECT=false ;;
        i) CLOUD_ID="$OPTARG" ;;
        I) BIZ_ID="$OPTARG" ;;
        w) PROXY_WANIP=( $(echo -n "$OPTARG" | sed 's/,/ /g') ); PROXY_WANIPS_STRING="$OPTARG" ;;
        l) PROXY_IP=( $(echo -n "$OPTARG" | sed 's/,/ /g') ); PROXY_LANIPS_STRING="$OPTARG" ;;
        g) PKGS_SOURCE="$OPTARG"; NGINX_IP_OPT="-g $OPTARG" ;;
        o) IPLIST_FILE=$OPTARG ;;
        A) export GSE_WANIP=( $(echo -n "$OPTARG" | sed 's/,/ /g' ) ) ;;
        D) export DATA_IP=$OPTARG EXTERNAL_IP=$OPTARG ;;
        E) export CONN_IP=$OPTARG; EXTERNAL_WANIP=$OPTARG ;;
        C) export CASCADE_IP=$OPTARG ;;
        e) export EXTERNAL_IP=$OPTARG ;;
        j) export QQ_ONLY=1 ;;
        u) export UPGRADE=1; UPGRADE_OPT="-u" ;;
        t) export TIMEOUT=$OPTARG ;;
        *) usage ;;
    esac
done

set_install_path
if $DIRECT; then
    # agent 直连gse server, 可以直连 nginx.
    # steps:
    #   1. 登陆机器
    #   2. 执行安装
    install_direct_area $NODE_TYPE
    rm -f /tmp/hosts_app.config /tmp/key_merged
else
    # 生成 cmd_file, 内容为安装 agent 要执行的命令列表
    if [ "$NODE_TYPE" == "proxy" ]; then
        fail "it is not permitted to install a proxy inbridge mode"
    fi

    if ! grep -qw '%HOSTS_LIST%' /tmp/hosts_app.config; then
        generate_keyfile /tmp/key_merged /tmp/hosts_app.config
        generate_cafile /tmp/ca_merged /tmp/hosts_app.config
        pare /tmp/hosts_app.config $(gen_script_shell) $(gen_script_bat)
        rm -f /tmp/hosts_app.config /tmp/key_merged /tmp/ca_merged
    elif [ -s $IPLIST_FILE ]; then
        pare $IPLIST_FILE $(gen_script_shell) $(gen_script_bat)
    else
        fail "setup failed -- not target host specified. please check."
    fi
    rm -f /tmp/hosts_app.config /tmp/key_merged
fi
