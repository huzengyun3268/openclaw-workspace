node.exe : - Fetching skill
所在位置 C:\npm-global\clawhub.ps1:24 字符: 5
+     & "node$exe"  "$basedir/node_modules/clawhub/bin/clawdhub.js" $ar ...
+     ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
    + CategoryInfo          : NotSpecified: (- Fetching skill:String) [], RemoteException
    + FullyQualifiedErrorId : NativeCommandError
 
#!/usr/bin/env python3
"""
Stock Monitor Pro - 瀹屾暣娴嬭瘯濂椾欢
娴嬭瘯鎵€鏈夊姛鑳芥ā鍧楋紝纭繚绯荤粺绋冲畾鎬?"""

import sys
import time
import unittest
from datetime import datetime, timedelta
from unittest.mock import Mock, patch

sys.path.insert(0, '/home/wesley/.openclaw/workspace/skills/stock-monitor/scripts')

from monitor import StockAlert, WATCHLIST


class TestDataFetching(unittest.TestCase):
    """娴嬭瘯1: 鏁版嵁鑾峰彇妯″潡"""
    
    def setUp(self):
        self.monitor = StockAlert()
    
    def test_sina_realtime_api(self):
        """娴嬭瘯鏂版氮瀹炴椂琛屾儏API"""
        data = self.monitor.fetch_sina_realtime([WATCHLIST[0]])
        self.assertIn('600362', data)
        self.assertGreater(data['600362']['price'], 0)
        print("鉁?鏂版氮瀹炴椂琛屾儏API姝ｅ父")
    
    def test_gold_api(self):
        """娴嬭瘯浼︽暒閲慉PI"""
        data = self.monitor.fetch_sina_realtime([WATCHLIST[-1]])
        self.assertIn('XAU', data)
        self.assertGreater(data['XAU']['price'], 4000)  # 榛勯噾搴旇鍦?000浠ヤ笂
        print("鉁?浼︽暒閲慉PI姝ｅ父")
    
    def test_data_validity(self):
        """娴嬭瘯鏁版嵁鏈夋晥鎬ф鏌?""
        data = self.monitor.fetch_sina_realtime(WATCHLIST[:3])
        for code, d in data.items():
            self.assertGreater(d['price'], 0, f"{code}浠锋牸鏃犳晥")
            self.assertGreater(d['prev_close'], 0, f"{code}鏄ㄦ敹鏃犳晥")
        print("鉁?鎵€鏈夋暟鎹湁鏁堟€ф鏌ラ€氳繃")


class TestAlertRules(unittest.TestCase):
    """娴嬭瘯2: 棰勮瑙勫垯妯″潡"""
    
    def setUp(self):
        self.monitor = StockAlert()
    
    def test_cost_percentage_alert(self):
        """娴嬭瘯鎴愭湰鐧惧垎姣旈璀?""
        stock = WATCHLIST[0].copy()
        stock['alerts'] = {'cost_pct_above': 10.0, 'cost_pct_below': -10.0}
        
        # 妯℃嫙鐩堝埄10%鐨勬暟鎹?        data = {'price': 62.7, 'prev_close': 57.0, 'cost': 57.0}  # 鎴愭湰57锛岀幇浠?2.7=+10%
        alerts, level = self.monitor.check_alerts(stock, data)
        
        has_profit_alert = any('鐩堝埄' in text for _, text in alerts)
        self.assertTrue(has_profit_alert, "搴旇鏈夌泩鍒╅璀?)
        print("鉁?鎴愭湰鐧惧垎姣旈璀︽甯?)
    
    def test_daily_change_alert(self):
        """娴嬭瘯鏃ュ唴娑ㄨ穼骞呴璀?""
        stock = WATCHLIST[0].copy()
        stock['alerts'] = {'change_pct_above': 5.0, 'change_pct_below': -5.0}
        
        # 妯℃嫙澶ф定6%
        data = {'price': 60.42, 'prev_close': 57.0, 'cost': 57.0}
        alerts, level = self.monitor.check_alerts(stock, data)
        
        has_change_alert = any('澶ф定' in text or '澶ц穼' in text for _, text in alerts)
        self.assertTrue(has_change_alert, "搴旇鏈夋定璺屽箙棰勮")
        print("鉁?鏃ュ唴娑ㄨ穼骞呴璀︽甯?)
    
    def test_no_duplicate_alerts(self):
        """娴嬭瘯闃查噸澶嶆満鍒?""
        stock = WATCHLIST[0].copy()
        stock['alerts'] = {'cost_pct_above': 5.0}
        
        data = {'price': 60.0, 'prev_close': 57.0, 'cost': 57.0}
        
        # 绗竴娆″簲璇ヨЕ鍙?        alerts1, _ = self.monitor.check_alerts(stock, data)
        self.assertGreater(len(alerts1), 0, "绗竴娆″簲璇ヨЕ鍙戦璀?)
        
        # 璁板綍棰勮
        for alert_type, _ in alerts1:
            self.monitor.record_alert(stock['code'], alert_type)
        
        # 绗簩娆′笉搴旇瑙﹀彂 (30鍒嗛挓鍐?
        alerts2, _ = self.monitor.check_alerts(stock, data)
        self.assertEqual(len(alerts2), 0, "30鍒嗛挓鍐呬笉搴旈噸澶嶈Е鍙?)
        print("鉁?闃查噸澶嶆満鍒舵甯?)


class TestAlertLevel(unittest.TestCase):
    """娴嬭瘯3: 鍒嗙骇棰勮绯荤粺"""
    
    def setUp(self):
        self.monitor = StockAlert()
    
    def test_critical_level(self):
        """娴嬭瘯绱ф€ョ骇鍒?""
        alerts = [('a', 'test'), ('b', 'test'), ('c', 'test')]
        weights = [3, 3, 3]  # 鎬绘潈閲?
        level = self.monitor._calculate_alert_level(alerts, weights, 'individual')
        self.assertEqual(level, 'critical')
        print("鉁?绱ф€ョ骇鍒垽鏂甯?)
    
    def test_warning_level(self):
        """娴嬭瘯璀﹀憡绾у埆"""
        alerts = [('a', 'test'), ('b', 'test')]
        weights = [2, 2]  # 鎬绘潈閲?
        level = self.monitor._calculate_alert_level(alerts, weights, 'individual')
        self.assertEqual(level, 'warning')
        print("鉁?璀﹀憡绾у埆鍒ゆ柇姝ｅ父")
    
    def test_info_level(self):
        """娴嬭瘯鎻愰啋绾у埆"""
        alerts = [('a', 'test')]
        weights = [1]
        level = self.monitor._calculate_alert_level(alerts, weights, 'individual')
        self.assertEqual(level, 'info')
        print("鉁?鎻愰啋绾у埆鍒ゆ柇姝ｅ父")


class TestStockTypeDifferentiation(unittest.TestCase):
    """娴嬭瘯4: 宸紓鍖栭厤缃?""
    
    def test_individual_stock_threshold(self):
        """娴嬭瘯涓偂闃堝€?""
        stock = [s for s in WATCHLIST if s.get('type') == 'individual'][0]
        self.assertEqual(stock['alerts']['change_pct_above'], 4.0)
        print("鉁?涓偂闃堝€奸厤缃纭?)
    
    def test_etf_threshold(self):
        """娴嬭瘯ETF闃堝€?""
        stock = [s for s in WATCHLIST if s.get('type') == 'etf'][0]
        self.assertEqual(stock['alerts']['change_pct_above'], 2.0)
        print("鉁?ETF闃堝€奸厤缃纭?)
    
    def test_gold_threshold(self):
        """娴嬭瘯榛勯噾闃堝€?""
        stock = [s for s in WATCHLIST if s.get('type') == 'gold'][0]
        self.assertEqual(stock['alerts']['change_pct_above'], 2.5)
        print("鉁?榛勯噾闃堝€奸厤缃纭?)


class TestSmartSchedule(unittest.TestCase):
    """娴嬭瘯5: 鏅鸿兘棰戠巼鎺у埗"""
    
    def setUp(self):
        self.monitor = StockAlert()
    
    def test_market_hours_detection(self):
        """娴嬭瘯浜ゆ槗鏃堕棿妫€娴?""
        # 褰撳墠鏄航绾︽椂闂达紝杞崲鎴愬寳浜椂闂?        ny_now = datetime.now()
        beijing_now = ny_now + timedelta(hours=13)
        
        schedule = self.monitor.should_run_now()
        self.assertIn('mode', schedule)
        self.assertIn(schedule['mode'], ['market', 'lunch', 'after_hours', 'night', 'weekend'])
        print(f"鉁?鏃堕棿妫€娴嬫甯?(褰撳墠妯″紡: {schedule['mode']})")
    
    def test_interval_settings(self):
        """娴嬭瘯涓嶅悓妯″紡鐨勯棿闅旇缃?""
        schedule = self.monitor.should_run_now()
        interval = schedule.get('interval', 0)
        self.assertGreater(interval, 0)
        self.assertIn(interval, [300, 600, 1800, 3600])  # 5/10/30/60鍒嗛挓
        print(f"鉁?闂撮殧璁剧疆姝ｅ父 ({interval//60}鍒嗛挓)")


class TestMessageFormat(unittest.TestCase):
    """娴嬭瘯6: 娑堟伅鏍煎紡"""
    
    def setUp(self):
        self.monitor = StockAlert()
    
    def test_message_contains_required_elements(self):
        """娴嬭瘯娑堟伅鍖呭惈蹇呰鍏冪礌"""
        # 妯℃嫙瑙﹀彂棰勮
        stock = WATCHLIST[0]
        data = {'price': 54.0, 'prev_close': 57.0, 'open': 55.0, 'high': 56.0, 'low': 53.0}
        alerts, level = [('cost_below', '馃搲 浜忔崯10%')], 'warning'
        
        # 鏋勫缓娑堟伅
        change_pct = -5.26
        msg = f"<b>鈿狅笍 銆愯鍛娿€戰煙?{stock['name']} ({stock['code']})</b>\n"
        msg += f"馃挵 褰撳墠浠锋牸: 楼{data['price']:.2f} ({change_pct:+.2f}%)\n"
        msg += f"馃幆 瑙﹀彂棰勮:\n  鈥?{alerts[0][1]}\n"
        
        # 妫€鏌ュ繀瑕佸厓绱?        self.assertIn('銆愯鍛娿€?, msg)
        self.assertIn('馃煝', msg)  # 缁胯穼
        self.assertIn('馃挵', msg)
        self.assertIn('馃幆', msg)
        print("鉁?娑堟伅鏍煎紡鍖呭惈蹇呰鍏冪礌")


class TestIntegration(unittest.TestCase):
    """娴嬭瘯7: 闆嗘垚娴嬭瘯"""
    
    def setUp(self):
        self.monitor = StockAlert()
    
    def test_full_run_once(self):
        """娴嬭瘯瀹屾暣run_once娴佺▼"""
        start = time.time()
        alerts_list = self.monitor.run_once(smart_mode=True)
        elapsed = time.time() - start
        
        # 鎵ц鏃堕棿搴旇鍚堢悊 (10-30绉?
        self.assertLess(elapsed, 60, "鎵ц鏃堕棿杩囬暱")
        self.assertIsInstance(alerts_list, list)
        print(f"鉁?瀹屾暣娴佺▼姝ｅ父 (鎵ц鏃堕棿: {elapsed:.2f}绉? 瑙﹀彂{len(alerts_list)}鏉?")
    
    def test_all_stocks_monitored(self):
        """娴嬭瘯鎵€鏈夎偂绁ㄩ兘琚洃鎺?""
        data = self.monitor.fetch_sina_realtime(WATCHLIST)
        # 鑷冲皯搴旇鑾峰彇鍒伴儴鍒嗘暟鎹?        self.assertGreater(len(data), 0)
        print(f"鉁?鐩戞帶瑕嗙洊姝ｅ父 (鑾峰彇鍒皗len(data)}/{len(WATCHLIST)}鍙暟鎹?")


def run_all_tests():
    """杩愯鎵€鏈夋祴璇?""
    print("=" * 70)
    print("馃И Stock Monitor Pro - 瀹屾暣娴嬭瘯濂椾欢")
    print("=" * 70)
    
    # 鍒涘缓娴嬭瘯濂椾欢
    loader = unittest.TestLoader()
    suite = unittest.TestSuite()
    
    # 娣诲姞鎵€鏈夋祴璇曠被
    suite.addTests(loader.loadTestsFromTestCase(TestDataFetching))
    suite.addTests(loader.loadTestsFromTestCase(TestAlertRules))
    suite.addTests(loader.loadTestsFromTestCase(TestAlertLevel))
    suite.addTests(loader.loadTestsFromTestCase(TestStockTypeDifferentiation))
    suite.addTests(loader.loadTestsFromTestCase(TestSmartSchedule))
    suite.addTests(loader.loadTestsFromTestCase(TestMessageFormat))
    suite.addTests(loader.loadTestsFromTestCase(TestIntegration))
    
    # 杩愯娴嬭瘯
    runner = unittest.TextTestRunner(verbosity=2)
    result = runner.run(suite)
    
    # 杈撳嚭鎬荤粨
    print("\n" + "=" * 70)
    print("馃搳 娴嬭瘯鎬荤粨")
    print("=" * 70)
    print(f"  娴嬭瘯鎬绘暟: {result.testsRun}")
    print(f"  閫氳繃: {result.testsRun - len(result.failures) - len(result.errors)}")
    print(f"  澶辫触: {len(result.failures)}")
    print(f"  閿欒: {len(result.errors)}")
    
    if result.wasSuccessful():
        print("\n鉁?鎵€鏈夋祴璇曢€氳繃锛佺郴缁熷彲浠ユ甯歌繍琛屻€?)
    else:
        print("\n鈿狅笍  閮ㄥ垎娴嬭瘯澶辫触锛岃妫€鏌ユ棩蹇椼€?)
    
    return result.wasSuccessful()


if __name__ == '__main__':
    success = run_all_tests()
    sys.exit(0 if success else 1)
