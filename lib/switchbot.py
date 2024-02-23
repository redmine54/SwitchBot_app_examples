from bluepy import btle
import struct
#Broadcastデータ取得用デリゲート
class SwitchbotScanDelegate(btle.DefaultDelegate):
    #コンストラクタ
    def __init__(self, macaddr):
        btle.DefaultDelegate.__init__(self)
        #print(f'macaddr={macaddr.lower()}')
        #センサデータ保守用変数
        self.sensorValue=None
        self.macaddr=macaddr

    #スキャンハンドラー
    def handleDiscovery(self, dev, isNewDev, isNewData):
        #対象MACアドレスのデバイスが見つかったら
        if dev.addr.lower()==self.macaddr.lower():
            #print(f'found addr:{dev.addr.lower()}')
            #アドバタイズデータ取り出し
            for (adtype, desc, value) in dev.getScanData():
                #環境データの時、データ取出し
                #print(f'desc={desc}')
                if desc=='16b Service Data':
                    #センサデータ取り出し
                    #print(f"fech desc='16b Service Data'")
                    #print(f'value={value}')
                    self._decodeSensorData(value)
    #センサデータを取り出してdist形式に変換
    def _decodeSensorData(self, valueStr):
        #文字列センサデータ（4文字目以降）のみ取出し、バイナリに変換
        #print(valueStr)
        valueBinary=bytes.fromhex(valueStr[4:])
        #バイナリ形式のセンサデータを数値に変換
        batt=valueBinary[2] & 0b01111111
        isTemperatureAboveFreezing = valueBinary[4] & 0b10000000
        temp=(valueBinary[3] & 0b00001111) / 10 + (valueBinary[4] & 0b01111111)
        if not isTemperatureAboveFreezing:
            temp=-temp
        humid=valueBinary[5] & 0b01111111
        #dictに格納
        self.sensorValue={
                'SensorType':'SwitchBot',
                'Temperature':temp,
                'Humidity':humid,
                'BatteryVoltage':batt
                }
    
