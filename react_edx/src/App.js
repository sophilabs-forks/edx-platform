import React, { Component } from "react";
import CoreLayout from "layouts/CoreLayout/CoreLayout";
import IndexView from "views/IndexView";
import response from "response";
import "sass/App.css";

class App extends Component {
  render() {
    return (
      <CoreLayout>
        <IndexView />
      </CoreLayout>
    );
  }
}

export default App;
