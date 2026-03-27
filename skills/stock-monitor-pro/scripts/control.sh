node.exe : - Fetching skill
所在位置 C:\npm-global\clawhub.ps1:24 字符: 5
+     & "node$exe"  "$basedir/node_modules/clawhub/bin/clawdhub.js" $ar ...
+     ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
    + CategoryInfo          : NotSpecified: (- Fetching skill:String) [], RemoteException
    + FullyQualifiedErrorId : NativeCommandError
 
#!/bin/bash
# Stock Monitor 涓€閿惎鍔ㄨ剼鏈?
SCRIPT_DIR="$(cd "$(dirname "$0")" && pwd)"
LOG_DIR="$HOME/.stock_monitor"
PID_FILE="$LOG_DIR/monitor.pid"

case "$1" in
    start)
        if [ -f "$PID_FILE" ] && kill -0 $(cat "$PID_FILE") 2>/dev/null; then
            echo "鈿狅笍  鐩戞帶杩涚▼宸插湪杩愯 (PID: $(cat $PID_FILE))"
            exit 1
        fi
        
        echo "馃殌 鍚姩 Stock Monitor 鍚庡彴杩涚▼..."
        mkdir -p "$LOG_DIR"
        nohup python3 "$SCRIPT_DIR/monitor_v2.py" > "$LOG_DIR/monitor.log" 2>&1 &
        echo $! > "$PID_FILE"
        echo "鉁?宸插惎鍔?(PID: $!)"
        echo "馃搵 鏃ュ織: $LOG_DIR/monitor.log"
        ;;
        
    stop)
        if [ -f "$PID_FILE" ]; then
            PID=$(cat "$PID_FILE")
            if kill -0 "$PID" 2>/dev/null; then
                echo "馃洃 鍋滄鐩戞帶杩涚▼ (PID: $PID)..."
                kill "$PID"
                rm "$PID_FILE"
                echo "鉁?宸插仠姝?
            else
                echo "鈿狅笍  杩涚▼涓嶅瓨鍦?
                rm "$PID_FILE"
            fi
        else
            echo "鈿狅笍  娌℃湁杩愯涓殑杩涚▼"
        fi
        ;;
        
    status)
        if [ -f "$PID_FILE" ] && kill -0 $(cat "$PID_FILE") 2>/dev/null; then
            echo "鉁?鐩戞帶杩愯涓?(PID: $(cat $PID_FILE))"
            echo "馃搵 鏈€杩戞棩蹇?"
            tail -5 "$LOG_DIR/monitor.log" 2>/dev/null || echo "  鏆傛棤鏃ュ織"
        else
            echo "鈴癸笍  鐩戞帶鏈繍琛?
        fi
        ;;
        
    log)
        tail -f "$LOG_DIR/monitor.log"
        ;;
        
    *)
        echo "Stock Monitor 鎺у埗鑴氭湰"
        echo ""
        echo "鐢ㄦ硶: ./control.sh [start|stop|status|log]"
        echo ""
        echo "  start   - 鍚姩鍚庡彴鐩戞帶"
        echo "  stop    - 鍋滄鐩戞帶"
        echo "  status  - 鏌ョ湅鐘舵€?
        echo "  log     - 鏌ョ湅瀹炴椂鏃ュ織"
        ;;
esac
