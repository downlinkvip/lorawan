// Decode an uplink message from a buffer
// payload - array of bytes
// metadata - key/value object

/** Decoder **/

// decode payload to string
var payloadStr = decodeToString(payload);

// decode payload to JSON
var data = decodeToJson(payload).DevEUI_uplink;
var payload_hex=data.payload_hex;
var DevEUI = data.DevEUI;
var DevAddr = data.DevAddr;
var telemetry = thingpark_uplink(payload_hex);

// Result object with device/asset attributes/telemetry data
var result = {
    deviceName:DevEUI,
    DevAddr:DevAddr,
    telemetry:telemetry,
    payload_hex: payload_hex,
};

/** Helper functions **/

function decodeToString(payload) {
   return String.fromCharCode.apply(String, payload);
}

function decodeToJson(payload) {
   // covert payload to string.
   var str = decodeToString(payload);

   // parse string to JSON
   var data = JSON.parse(str);
   return data;
}

function base64ToHex(str) {
  var raw = atob(str);
  var res = "";
  for (var i = 0; i < raw.length; i++) {
    var hex = raw.charCodeAt(i).toString(16);
    res += (hex.length === 2 ? hex : '0' + hex);
  }
  return res.toUpperCase();
}

function hex_to_ascii(str1)
 {
  var hex  = str1.toString();
  var str = '';
  for (var n = 0; n < hex.length; n += 2) {
    str += String.fromCharCode(parseInt(hex.substr(n, 2), 16));
  }
  return str;
 }

function water_decode(payload) {
  var Battery_low, Consumption_HF, Direction, Wire_break, mes, mes2, sensorTime;
  Consumption_HF = Direction = Wire_break = Battery_low = sensorTime = null;
  mes = payload;
  sensorTime = toData(mes, "02");
  mes2 = toNewMes(mes, "02");
  Consumption_HF = toData(mes2, "03");
  return {Consumption_HF:Consumption_HF, Direction:Direction, Wire_break:Wire_break, Battery_low:Battery_low, sensorTime:sensorTime};
}

function phaseABC_decode(payload) {
  var A_RMS_Voltage, B_RMS_Voltage, C_RMS_Voltage, Export_reactive_SumQ1Q2, Import_Active_Wh_Tariff1_SumQ1Q4, Import_Active_Wh_Tariff2_SumQ1Q4, Import_Active_Wh_Tariff3_SumQ1Q4, Import_reactive_SumQ1Q2, mes, mes2, mes3, mes4, mes5, mes6, mes7, mes8, mes9, sensorTime;
  A_RMS_Voltage = B_RMS_Voltage = C_RMS_Voltage = Import_reactive_SumQ1Q2 = Export_reactive_SumQ1Q2 = Import_Active_Wh_Tariff1_SumQ1Q4 = Import_Active_Wh_Tariff2_SumQ1Q4 = Import_Active_Wh_Tariff3_SumQ1Q4 = sensorTime = null;
  mes = payload;
  A_RMS_Voltage = toData(mes, "0e");
  mes2 = toNewMes(mes, "0e");
  B_RMS_Voltage = toData(mes2, "0f");
  mes3 = toNewMes(mes2, "0f");
  C_RMS_Voltage = toData(mes3, "10");
  mes4 = toNewMes(mes3, "10");
  Import_reactive_SumQ1Q2 = toData(mes4, "06");
  mes5 = toNewMes(mes4, "06");
  Export_reactive_SumQ1Q2 = toData(mes5, "08");
  mes6 = toNewMes(mes5, "08");
  Import_Active_Wh_Tariff1_SumQ1Q4 = toData(mes6, "2a");
  mes7 = toNewMes(mes6, "2a");
  Import_Active_Wh_Tariff2_SumQ1Q4 = toData(mes7, "2b");
  mes8 = toNewMes(mes7, "2b");
  Import_Active_Wh_Tariff3_SumQ1Q4 = toData(mes8, "2c");
  mes9 = toNewMes(mes8, "2c");
  sensorTime = toData(mes9, "02");
  return {A_RMS_Voltage:A_RMS_Voltage, B_RMS_Voltage:B_RMS_Voltage, C_RMS_Voltage:C_RMS_Voltage, Import_reactive_SumQ1Q2:Import_reactive_SumQ1Q2, Export_reactive_SumQ1Q2:Export_reactive_SumQ1Q2, Import_Active_Wh_Tariff1_SumQ1Q4:Import_Active_Wh_Tariff1_SumQ1Q4, Import_Active_Wh_Tariff2_SumQ1Q4:Import_Active_Wh_Tariff2_SumQ1Q4, Import_Active_Wh_Tariff3_SumQ1Q4:Import_Active_Wh_Tariff3_SumQ1Q4, sensorTime:sensorTime};
}

function th_decode(payload) {
  var humidity, mes, mes2, mes3, pinStatus, temperature;
  mes = payload;
  temperature = toData(mes, "80");
  mes2 = toNewMes(mes, "80");
  humidity = toData(mes2, "81");
  mes3 = toNewMes(mes2, "81");
  pinStatus = toData(mes3, "70");
  return {temperature:temperature, humidity:humidity, pinStatus:pinStatus};
}

function ActivePower_decode(payload) {
  var ActivePower, ApparentPower, CurrentUnbalance, ReactivePower, mes, mes2, mes3, mes4, mes5, sensorTime;
  ActivePower = ReactivePower = ApparentPower = CurrentUnbalance = sensorTime = null;
  mes = payload;
  ActivePower = toData(mes, "1b");
  mes2 = toNewMes(mes, "1b");
  ReactivePower = toData(mes2, "1f");
  mes3 = toNewMes(mes2, "1f");
  ApparentPower = toData(mes3, "23");
  mes4 = toNewMes(mes3, "23");
  CurrentUnbalance = toData(mes4, "40");
  mes5 = toNewMes(mes4, "40");
  sensorTime = toData(mes5, "02");
  return {ActivePower:ActivePower, ReactivePower:ReactivePower, ApparentPower:ApparentPower, CurrentUnbalance:CurrentUnbalance, sensorTime:sensorTime};
}

function toData(mes, obis) {
  var data, dataLength, day, finalResult, hour, min, month, realObis, result, scaleData, sec, year;
  realObis = mes.slice(0, 2);

  if (obis !== "02") {
    if (realObis !== obis) {
      return null;
    }
    dataLength = Number.parseInt(mes.slice(2, 4), 16) * 2;
    rawData = mes.slice(4, dataLength + 4);
	data = parseInt(rawData, 16);
    scaleData = toScale(mes.slice(dataLength + 4, dataLength + 6));
    finalResult = Number.parseFloat(data * scaleData);
    return finalResult;
  }

  if (obis === "02") {
    dataLength = Number.parseInt(mes.slice(2, 4), 16) * 2;
    data = Number.parseInt(mes.slice(4, dataLength + 4), 16);
    month = mes.slice(4, 6);
    day = mes.slice(6, 8);
    year = mes.slice(8, 10);
    hour = mes.slice(10, 12);
    min = mes.slice(12, 14);
    sec = mes.slice(14, 16);
    result = year + "-" + month + "-" + day + " " + hour + ":" + min;
    //result = datetime.strptime(result, "%y-%m-%d %H:%M");
    return result;
  }
}

function toScale(scaleHex) {
  if (scaleHex === "00") {
    return 1;
  }

  if (scaleHex === "ff") {
    return 0.1;
  }

  if (scaleHex === "fe") {
    return 0.01;
  }

  if (scaleHex === "fd") {
    return 0.001;
  }

  if (scaleHex === "fc") {
    return 0.0001;
  }

  if (scaleHex === "fb") {
    return 1e-05;
  }

  return 1;
}

function toNewMes(mes, obis) {
  var index1, realObis;
  realObis = mes.slice(0, 2);

  if (realObis !== obis) {
    return mes;
  }

  if (obis !== "02") {
    index1 = Number.parseInt(mes.slice(2, 4), 16) * 2 + 6;
    return mes.slice(index1);
  } else {
    index1 = Number.parseInt(mes.slice(2, 4), 16) * 2 + 4;
    return mes.slice(index1);
  }
}


function thingpark_uplink(payload_hex) {
  var A_RMS_Voltage, ActivePower, ApparentPower, B_RMS_Voltage, Battery_low, C_RMS_Voltage, Consumption_HF, CurrentUnbalance, Direction, Export_reactive_SumQ1Q2, Import_Active_Wh_Tariff1_SumQ1Q4, Import_Active_Wh_Tariff2_SumQ1Q4, Import_Active_Wh_Tariff3_SumQ1Q4, Import_reactive_SumQ1Q2, ReactivePower, Wire_break, first_obis, humitidy, pinStatus, sensorTime, temperature;
  first_obis = payload_hex.slice(0, 2);

  if (first_obis === "80") {
    telemetry = th_decode(payload_hex);
    return telemetry;
  } else {
    if (first_obis === "0e" || first_obis === "06" || first_obis === "2a") {
      telemetry = phaseABC_decode(payload_hex);
      return telemetry;
    } else {
      if (first_obis === "1b") {
        telemetry =  ActivePower_decode(payload_hex);
        return  telemetry;
      } else {
        if (first_obis === "02") {
          telemetry = water_decode(payload_hex);
          return telemetry;
        }
      }
    }
  }
  return requestBody;
}

return result;