// This is a simple example and you may want to add more error handling and more robustness to your final code.
// You can use this sample code in Browsers like Chrome or Edge directly after adapting the IP address if needed (Press `F12` and copy paste the code to the console).

const base64ToArrayBuffer = (base64) => {
  const binaryString = atob(base64);
  const len = binaryString.length;
  const bytes = new Uint8Array(len);
  for (let i = 0; i < len; i++) {
    bytes[i] = binaryString.charCodeAt(i);
  }
  return bytes.buffer;
};

const ws = new WebSocket('ws://192.168.0.1/crownJSON');

ws.onerror = function (error) {
  console.log('Shit happens', error)
};

ws.onmessage = function (msgRaw) {
  const msg = JSON.parse(msgRaw.data);

  if (msg.header.clientId === 1) {
    const handleId = msg.data.handle.id;

    ws.send('{"header":{"type":"FunctionCall","clientId":2,"function":"View/Present/setID"},"data":{"id":"default","handle":{"type":"handle","id":' + handleId + '}},"options":{}}')
    ws.send('{"header":{"type":"FunctionCall","clientId":3,"function":"View/Present/register"},"data":{"eventname":"OnPresentLive","handle":{"type":"handle","id":' + handleId + '}},"options":{"queue":{"priority":"MID","maxSize":1,"discardIfFull":"OLDEST"}}}')
  }
  else if (msg.header.clientId === 2) {
    // answer setID 
  }
  else if (msg.header.clientId === 3) {
    // new Scan Event

    for (const entry of msg.data.viewObject) {
      for (const iconic of entry.data.data.Iconics) {

        const binaryDataOfDistChannel1 = base64ToArrayBuffer(iconic.data.DistValues[0].data)
        const distChannelFloat32 = new Float32Array(binaryDataOfDistChannel1);

        // carefully // this line floods the console
        console.log(iconic.class, distChannelFloat32);
      }
    }
  }
}

ws.onopen = function () {
  ws.send('{"header":{"type":"FunctionCall","clientId":1,"function":"View/Present/create"}}');
};