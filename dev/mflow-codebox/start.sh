#!/bin/bash
# start.sh — codebox 平台进程管理契约
# 平台调用: start.sh start <name> <port>
# 平台调用: start.sh stop  <name>
# 平台调用: start.sh status <name>

case "$1" in
  start)
    PORT=$3
    mkdir -p logs run

    # 构建 Go 二进制
    go build -o run/server ./cmd/server 2>&1 | tee logs/build.log
    if [ $? -ne 0 ]; then
      echo "build failed"
      exit 1
    fi

    # 启动
    nohup ./run/server > logs/server.log 2>&1 &
    echo $! > run/server.pid
    sleep 1

    if kill -0 $(cat run/server.pid) 2>/dev/null; then
      echo "started on port $PORT (pid=$(cat run/server.pid))"
    else
      echo "failed to start"
      cat logs/server.log
      exit 1
    fi
    ;;
  stop)
    if [ -f run/server.pid ]; then
      PID=$(cat run/server.pid)
      if kill -0 "$PID" 2>/dev/null; then
        kill "$PID"
        echo "stopped (pid=$PID)"
      else
        echo "already stopped"
      fi
      rm -f run/server.pid
    else
      echo "no pid file"
    fi
    ;;
  status)
    if [ -f run/server.pid ] && kill -0 $(cat run/server.pid) 2>/dev/null; then
      echo "running (pid=$(cat run/server.pid))"
    else
      echo "stopped"
    fi
    ;;
  *)
    echo "usage: start.sh {start|stop|status}"
    exit 1
    ;;
esac
