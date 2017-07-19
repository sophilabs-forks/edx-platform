import React, { Component } from "react";
import styles from "sass/test/Govno.css";

class Govno extends Component {
  render() {
    return (
      <div>
        <div className={styles.container}>
          <h1 className={`${styles.govno}`}>GOVNO</h1>
        </div>
      </div>
    );
  }
}

export default Govno;
