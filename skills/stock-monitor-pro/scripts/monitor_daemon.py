node.exe : - Fetching skill
所在位置 C:\npm-global\clawhub.ps1:24 字符: 5
+     & "node$exe"  "$basedir/node_modules/clawhub/bin/clawdhub.js" $ar ...
+     ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
    + CategoryInfo          : NotSpecified: (- Fetching skill:String) [], RemoteException
    + FullyQualifiedErrorId : NativeCommandError
 
#!/usr/bin/env python3
"""
Stock Monitor Daemon - 鍚庡彴甯搁┗杩涚▼
鑷姩杩愯鐩戞帶锛屾櫤鑳芥帶鍒堕鐜囷紝鏀寔 graceful shutdown
"""

import sys
import time
import signal
import logging
from datetime import datetime
from pathlib import Path

# 璁剧疆鏃ュ織
log_dir = Path.home() / ".stock_monitor"
log_dir.mkdir(exist_ok=True)
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(levelname)s - %(message)s',
    handlers=[
        logging.FileHandler(log_dir / "monitor.log"),
        logging.StreamHandler(sys.stdout)
    ]
)
logger = logging.getLogger(__name__)

# 瀵煎叆鐩戞帶绫?sys.path.insert(0, str(Path(__file__).parent))
from monitor import StockAlert, WATCHLIST

class MonitorDaemon:
    def __init__(self):
        self.monitor = StockAlert()
        self.running = True
        self.last_run_time = 0
        
        # 璁剧疆淇″彿澶勭悊
        signal.signal(signal.SIGTERM, self.handle_shutdown)
        signal.signal(signal.SIGINT, self.handle_shutdown)
    
    def handle_shutdown(self, signum, frame):
        """浼橀泤閫€鍑?""
        logger.info(f"鏀跺埌淇″彿 {signum}锛屾鍦ㄥ叧闂?..")
        self.running = False
    
    def get_sleep_interval(self):
        """鏍规嵁褰撳墠鏃堕棿鑾峰彇鐫＄湢闂撮殧"""
        schedule = self.monitor.should_run_now()
        if not schedule.get("run"):
            # 濡傛灉褰撳墠涓嶉渶瑕佽繍琛岋紝璁＄畻鍒颁笅娆¤繍琛岀殑鏃堕棿
            now = datetime.now()
            hour = now.hour
            
            # 鍑屾櫒鏃舵锛?灏忔椂鍚庢鏌?            if 0 <= hour < 9:
                return 3600
            return 300  # 榛樿5鍒嗛挓
        
        return schedule.get("interval", 300)
    
    def run(self):
        """涓诲惊鐜?""
        logger.info("=" * 60)
        logger.info("馃殌 Stock Monitor Daemon 鍚姩")
        logger.info(f"馃搵 鐩戞帶鏍囩殑: {len(WATCHLIST)} 鍙?)
        logger.info("=" * 60)
        
        while self.running:
            try:
                # 妫€鏌ユ槸鍚﹀簲璇ユ墽琛?                schedule = self.monitor.should_run_now()
                
                if schedule.get("run"):
                    mode = schedule.get("mode", "normal")
                    stocks_count = len(schedule.get("stocks", []))
                    logger.info(f"[{mode}] 鎵弿 {stocks_count} 鍙爣鐨?..")
                    
                    # 鎵ц鐩戞帶
                    alerts = self.monitor.run_once(smart_mode=False)  # 宸茬粡鍒ゆ柇杩囦簡
                    
                    if alerts:
                        logger.info(f"鈿狅笍 瑙﹀彂 {len(alerts)} 鏉￠璀?)
                        # 杩欓噷浼氶€氳繃 message 宸ュ叿鍙戦€侀€氱煡
                    else:
                        logger.debug("鉁?鏃犻璀?)
                    
                    self.last_run_time = time.time()
                
                # 璁＄畻鐫＄湢闂撮殧
                sleep_interval = self.get_sleep_interval()
                logger.debug(f"涓嬫妫€鏌? {sleep_interval} 绉掑悗")
                
                # 鍒嗘鐫＄湢锛屾柟渚垮強鏃跺搷搴旈€€鍑轰俊鍙?                slept = 0
                while slept < sleep_interval and self.running:
                    time.sleep(1)
                    slept += 1
                    
            except Exception as e:
                logger.error(f"杩愯鍑洪敊: {e}", exc_info=True)
                time.sleep(60)  # 鍑洪敊鍚庣瓑寰?鍒嗛挓閲嶈瘯
        
        logger.info("馃憢 Daemon 宸插仠姝?)

if __name__ == '__main__':
    daemon = MonitorDaemon()
    daemon.run()
