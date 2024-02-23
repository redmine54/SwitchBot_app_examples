from bluepy import btle
from lib.switchbot import SwitchbotScanDelegate

######SwitchBotの値取得######
#switchbot.pyのセンサ値取得デリゲートを、スキャン時実行に設定
print('start switchbot_toSpreadSheet!')
macaddr='D1:E0:78:0E:BA:00'
scanner=btle.Scanner().withDelegate(SwitchbotScanDelegate(macaddr))
#スキャンしてセンサ値取得（タイムアウト5秒）
scanner.scan(5.0)
sensorValue=scanner.delegate.sensorValue
print(f"  Temperature   ={sensorValue['Temperature']:6.1f} degC")
print(f"  Humidity      ={sensorValue['Humidity']:6.1f} %")
print(f"  BatteryVoltage={sensorValue['BatteryVoltage']:6.1f} %")
