import React, { PropTypes } from "react";
import styles from "sass/core-layout/navigation/navigation-item.css";

export class NavigationItem extends React.Component {
  render() {

    return (
      <a
        href={this.props.item.itemURL}
        className={`${this.props.item.isButton ? `${styles["item-button"]} ${styles["button-medium"]} ${styles["button-primary"]} ${styles["button-positive"]}` : styles["item-regular"] }`} target={this.props.item.openInNewTab ? '_blank' : '_self'}
        >
        {this.props.item.itemLabel}
      </a>
    );
  }
}

NavigationItem.propTypes = {
  item: PropTypes.object,
}
NavigationItem.defaultProps = {

}

export default NavigationItem;
