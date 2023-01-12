import pyodbc
from datetime import datetime
from bitstring import BitArray
#b = BitArray('0xd178')
#print(b.int)
# returns



def water_decode(payload):
    Consumption_HF = Direction = Wire_break = Battery_low = sensorTime = None
    mes = payload
    sensorTime = toData(mes,'02')
    mes2 = toNewMes(mes,'02')
    Consumption_HF = toData(mes2,'03')
    return Consumption_HF ,Direction , Wire_break , Battery_low , sensorTime

def phaseABC_decode(payload):
    A_RMS_Voltage = B_RMS_Voltage = C_RMS_Voltage = Import_reactive_SumQ1Q2 = Export_reactive_SumQ1Q2 = Import_Active_Wh_Tariff1_SumQ1Q4 = Import_Active_Wh_Tariff2_SumQ1Q4 = Import_Active_Wh_Tariff3_SumQ1Q4 = sensorTime = None
    mes = payload
    A_RMS_Voltage = toData(mes, '0e')

    mes2 = toNewMes(mes,'0e')
    B_RMS_Voltage = toData(mes2,'0f')

    mes3 = toNewMes(mes2,'0f')
    C_RMS_Voltage = toData(mes3,'10')

    mes4 = toNewMes(mes3, '10')
    Import_reactive_SumQ1Q2 = toData(mes4, '06')

    mes5 = toNewMes(mes4, '06')
    Export_reactive_SumQ1Q2 = toData(mes5, '08')

    mes6 = toNewMes(mes5, '08')
    Import_Active_Wh_Tariff1_SumQ1Q4 = toData(mes6, '2a')

    mes7 = toNewMes(mes6, '2a')
    Import_Active_Wh_Tariff2_SumQ1Q4 = toData(mes7, '2b')

    mes8 = toNewMes(mes7, '2b')
    Import_Active_Wh_Tariff3_SumQ1Q4 = toData(mes8, '2c')

    mes9 = toNewMes(mes8, '2c')
    sensorTime = toData(mes9, '02')

    return A_RMS_Voltage, B_RMS_Voltage, C_RMS_Voltage, Import_reactive_SumQ1Q2, Export_reactive_SumQ1Q2, Import_Active_Wh_Tariff1_SumQ1Q4, Import_Active_Wh_Tariff2_SumQ1Q4, Import_Active_Wh_Tariff3_SumQ1Q4, sensorTime

def th_decode(payload):
    mes = payload
    temperature = toData(mes, '80')

    mes2 = toNewMes(mes, '80')
    humidity = toData(mes2, '81')

    mes3 = toNewMes(mes2, '81')
    pinStatus = toData(mes3, '70')
    return temperature, humidity, pinStatus

def ActivePower_decode(payload):
    ActivePower= ReactivePower = ApparentPower =  CurrentUnbalance = sensorTime = None
    mes = payload
    ActivePower = toData(mes, '1b')

    mes2 = toNewMes(mes, '1b')
    ReactivePower = toData(mes2, '1f')

    mes3 = toNewMes(mes2, '1f')
    ApparentPower = toData(mes3, '23')

    mes4 = toNewMes(mes3, '23')
    CurrentUnbalance = toData(mes4, '40')

    mes5 = toNewMes(mes4, '40')
    sensorTime = toData(mes5, '02')
    return ActivePower, ReactivePower, ApparentPower, CurrentUnbalance, sensorTime

def toData(mes, obis):
    realObis = mes[:2]
    if obis != '02': # For meter
        if realObis != obis:  # Return None for meter if not included in payload
            return None
        dataLength = int(mes[2:4],16)*2
        rawData = BitArray('0x'+mes[4: dataLength + 4])
        data = rawData.int
        scaleData = toScale(mes[dataLength + 4: dataLength + 6])
        finalResult = float(data * scaleData)
        return finalResult
    if obis == '02': # For time
        dataLength = int(mes[2:4],16)*2
        data = int(mes[4: dataLength + 4], 16)
        month = mes[4:6]
        day = mes[6:8]
        year = mes[8:10]
        hour = mes[10:12]
        min = mes[12:14]
        sec = mes[14:16]
        result = year +'-' + month + '-' + day + ' ' + hour + ':' + min# + ':' +sec
        result = datetime.strptime(result, '%y-%m-%d %H:%M')
        return result

def toScale(scaleHex):
    if scaleHex == '00':
       return 1
    if scaleHex == 'ff':
        return 0.1
    if scaleHex == 'fe':
        return 0.01
    if scaleHex == 'fd':
        return 0.001
    if scaleHex == 'fc':
        return 0.0001
    if scaleHex == 'fb':
        return 0.00001
    return 1

def toNewMes(mes, obis):
    realObis = mes[:2]
    if realObis != obis:
        return mes  # Return original payload so next meter will use this payload.
    if obis!='02':
        index1 = int(mes[2:4], 16) * 2 + 6 # Return next payload for next meter. (4 for obis, datalength + 2 for scale)
        return mes[index1:]
    else:
        index1 = int(mes[2:4], 16) * 2 + 4  # Return next payload for next meter. (4 for obis, datalength)
        return mes[index1:]

############## Setup SQL connection
conn = pyodbc.connect('Driver={SQL Server};'
                      'Server=192.168.1.103;'
                      'Database=graphAPI;'
                      'Trusted_Connection=yes;')

cursor = conn.cursor()


def ActivePower_decode(payload):
    ActivePower= ReactivePower = ApparentPower =  CurrentUnbalance = sensorTime = None
    mes = payload
    ActivePower = toData(mes, '1b')

    mes2 = toNewMes(mes, '1b')
    ReactivePower = toData(mes2, '1f')

    mes3 = toNewMes(mes2, '1f')
    ApparentPower = toData(mes3, '23')

    mes4 = toNewMes(mes3, '23')
    CurrentUnbalance = toData(mes4, '40')

    mes5 = toNewMes(mes4, '40')
    sensorTime = toData(mes5, '02')
    return ActivePower, ReactivePower, ApparentPower, CurrentUnbalance, sensorTime

def phaseABC_decode_db(DevEUI,payload_hex,A_RMS_Voltage, B_RMS_Voltage, C_RMS_Voltage, Import_reactive_SumQ1Q2, Export_reactive_SumQ1Q2, Import_Active_Wh_Tariff1_SumQ1Q4, Import_Active_Wh_Tariff2_SumQ1Q4, Import_Active_Wh_Tariff3_SumQ1Q4, sensorTime):
    cursor.execute("""INSERT INTO iot_phaseABC
                            (
                            devuid,
                            payload_hex,
                            A_RMS_Voltage,
                            B_RMS_Voltage,
                            C_RMS_Voltage,
                            Import_reactive_SumQ1Q2,
                            Export_reactive_SumQ1Q2,
                            Import_Active_Wh_Tariff1_SumQ1Q4,
                            Import_Active_Wh_Tariff2_SumQ1Q4,
                            Import_Active_Wh_Tariff3_SumQ1Q4,
                            sensorTime
                            )
                      VALUES (?,?,?,?,?,?,?,?,?,?,?)""", (DevEUI,payload_hex,A_RMS_Voltage, B_RMS_Voltage, C_RMS_Voltage, Import_reactive_SumQ1Q2, Export_reactive_SumQ1Q2, Import_Active_Wh_Tariff1_SumQ1Q4, Import_Active_Wh_Tariff2_SumQ1Q4, Import_Active_Wh_Tariff3_SumQ1Q4, sensorTime))
    conn.commit()

def activePower_decode_db(DevEUI,payload_hex,ActivePower, ReactivePower, ApparentPower,CurrentUnbalance, sensorTime ):
    cursor.execute("""INSERT INTO iot_activePower
                                (
                                devuid,
                                payload_hex,
                                ActivePower,
                                ReactivePower,
                                ApparentPower,
                                CurrentUnbalance,
                                sensorTime
                                )
                          VALUES (?,?,?,?,?,?,?)""", (
    DevEUI, payload_hex,ActivePower,ReactivePower,ApparentPower,CurrentUnbalance, sensorTime))
    conn.commit()

def water_decode_db(DevEUI,payload_hex, Consumption_HF ,Direction , Wire_break , Battery_low , sensorTime  ):
    cursor.execute("""INSERT INTO iot_water
                                (
                                devuid,
                                payload_hex,
                                Consumption_HF,
                                Direction,
                                Wire_break,
                                Battery_low,
                                sensorTime
                                )
                          VALUES (?,?,?,?,?,?,?)""", (
    DevEUI,payload_hex, Consumption_HF ,Direction , Wire_break , Battery_low , sensorTime))
    conn.commit()

ActivePower_decode('1b02f95bfd1f022e88fd2302d178fd0206110222000000')