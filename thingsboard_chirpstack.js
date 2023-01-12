// Decode an uplink message from a buffer
// payload - array of bytes
// metadata - key/value object

/** Decoder **/

// decode payload to string
var payloadStr = decodeToString(payload);

// decode payload to JSON
var data = decodeToJson(payload);
var incomingHexData = hex_to_ascii(base64ToHex(data.data));
var deviceName = data.deviceInfo.deviceName;

// Result object with device/asset attributes/telemetry data
var result = {
    data:incomingHexData,
    deviceName:deviceName,
     attributes: {
       applicationId: data.deviceInfo.applicationName,
       DevEUI: data.deviceInfo.devEui,
       integrationName: metadata['integrationName'],
       txInfo: data.txInfo,
       fPort: data.fPort,
       devAddr: data.devAddr,
       dr: data.dr
   },
   telemetry: {
       hex_payload: incomingHexData,
   },
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

return result;