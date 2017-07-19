import React, { PropTypes } from 'react';
import styles from "sass/core-layout/core-layout.css";
import Navigation from "components/core-layout/navigation/Navigation";
import Footer from "components/core-layout/Footer";

export class CoreLayout extends React.Component {

  render() {

    return (
      <div className={styles["core-layout"]}>
        <Navigation />
        <div className={styles["core-layout__content"]}>
          {this.props.children}
        </div>
        <Footer />
      </div>
    )
  }
}

CoreLayout.propTypes = {
  children: PropTypes.element,
}
CoreLayout.defaultProps = {}

export default CoreLayout;
