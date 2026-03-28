@echo off
cd C:\Users\Administrator\.openclaw\workspace
echo [INFO] Installing skills at %date% %time% >> skills_install_log.txt
clawhub install skill-creator --force >> skills_install_log.txt 2>&1
clawhub install data-visualization-2 --force >> skills_install_log.txt 2>&1
clawhub install jina-reader --force >> skills_install_log.txt 2>&1
clawhub install humanizer-zh-cn --force >> skills_install_log.txt 2>&1
clawhub install auto-monitor --force >> skills_install_log.txt 2>&1
clawhub install einstein-research-backtest-engine-dv --force >> skills_install_log.txt 2>&1
echo [DONE] Skills install completed at %date% %time% >> skills_install_log.txt
