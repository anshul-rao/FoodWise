import React, { Component } from "react";
import Quagga from "quagga";

class BarcodeScanner extends Component {
  state = {
    inputStream: {
      name: "Live",
      type: "LiveStream",
      target: "#barcode-scanner",
    },
    decoder: {
      readers: ["upc_reader"],
      // readers: ["upc_reader", "upc_e_reader", "ean_reader", "ean_8_reader"],
    },
    locate: true
  };

  componentDidMount() {
    Quagga.init(this.state, (err) => {
      if (err) {
        console.log(err);
        return;
      }
      console.log("Initialization finished. Ready to start!");
      Quagga.start();

      Quagga.onDetected(this.onBarcodeDetected);
    });
  }

  componentWillUnmount() {
    Quagga.stop();
  }

  onBarcodeDetected = (() => {
    let loggedTime = 0;
  
    return (data) => {
      const now = Date.now();
  
      if (now - loggedTime > 2000) {
        console.log("Barcode detected:", data.codeResult.code);
        loggedTime = now;
      }
    };
  })();  

  render() {
    return (
      <div>
        <div id="barcode-scanner" />
      </div>
    );
  }
}

export default BarcodeScanner;
