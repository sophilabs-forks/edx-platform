import React, { PropTypes } from "react";
import FontAwesome from "react-fontawesome";
import styles from "sass/ui-elements/ui-button.css";

export class UIButton extends React.Component {
  render() {

    return (
      <button className={`${styles["button"]} ${styles[this.props.buttonSize]} ${styles[this.props.buttonAlignment]} ${styles[this.props.buttonStyle]} ${styles[this.props.buttonType]}`} onClick={this.props.onClick}>
        {this.props.buttonIcon && (
          <FontAwesome
            className={styles["button-icon"]}
            name={this.props.buttonIcon}
          />
        )}
        {this.props.buttonLabel && (
          <span className={styles["button-label"]}>{this.props.buttonLabel}</span>
        )}
      </button>
    );
  }
}

UIButton.propTypes = {
  buttonSize: PropTypes.string,
  buttonAlignment: PropTypes.string,
  buttonStyle: PropTypes.string,
  buttonType: PropTypes.string,
  buttonIcon: PropTypes.string,
  buttonLabel: PropTypes.string,
  onClick: PropTypes.function,
}
UIButton.defaultProps = {
  buttonSize: "button-medium",
  buttonAlignment: "align-top",
  buttonStyle: "button-positive",
  buttonType: "button-primary",
  buttonIcon: null,
  buttonLabel: null,
  onClick: null,
}

export default UIButton;
