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
      readers: ["upc_reader", "ean_reader"],
    },
    locate: true,
  };

  componentDidMount() {
    Quagga.init(this.state, (err) => {
      if (err) {
        console.log(err);
        return;
      }

      Quagga.start();

      Quagga.onDetected(this.onBarcodeDetected);
    });
  }

  componentWillUnmount() {
    Quagga.stop();
  }

  onBarcodeDetected = (() => {
    let lastLoggedTime = 0;
  
    return (data) => {
      const now = Date.now();
  
      if (now - lastLoggedTime > 3000) {
        console.log("Barcode detected:", data.codeResult.code);
        lastLoggedTime = now;
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
