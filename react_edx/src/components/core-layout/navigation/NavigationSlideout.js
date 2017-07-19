import React, { PropTypes } from "react";
import styles from "sass/core-layout/navigation/navigation-slideout.css";
import FontAwesome from "react-fontawesome";

export class NavigationSlideout extends React.Component {
  constructor(props: Props) {
    super(props);
    this.state = {
      slideoutToggled: false,
    };
    this.onClick = this.onClick.bind(this);
  }

  onClick(_event) {
    this.setState({
      slideoutToggled: !(this.state.slideoutToggled),
    } );
    console.log(this.state.slideoutToggled);
  }

  render() {

    return (
      <div className={`d-flex ml-auto ${styles["nav-dropdown"]}`}>
        <button className={`d-flex ${styles["toggle-button"]} ${this.state.slideoutToggled ? styles["toggled"] : ''}`} onClick={this.onClick}>
          <FontAwesome
            className={styles["toggle-icon"]}
            name="bars"
          />
        </button>
        <button className={`d-flex ml-auto ${styles["dismiss-button"]} ${this.state.slideoutToggled ? styles["toggled"] : ''}`} onClick={this.onClick}>
          <FontAwesome
            className={styles["toggle-icon"]}
            name="remove"
          />
        </button>
        <nav className={`${styles["nav-dropdown__drawer"]} ${this.state.slideoutToggled ? styles["toggled"] : ''}`}>
          <div className={`${styles["general-items"]}`}>
            { (this.props.navItems.length > this.props.maxExpandedNavItems) && (
              this.props.navItems.map(function(item, key){
                return (
                  <a
                    key={key}
                    href={item.itemURL}
                    className={`${item.isButton ? styles["item-button"] : styles["item-regular"] }`} target={item.openInNewTab ? '_blank' : '_self'}
                    >
                    {item.itemLabel}
                  </a>
                )
              })
            )}
          </div>
          {(this.props.userData && (this.props.navItems.length > this.props.maxExpandedNavItems)) && (
            <span className={`${styles["lists-separator"]}`}></span>
          )}
          {this.props.userData && (
            <div className={`${styles["user-related-items"]}`}>
              Blabla user stuff
            </div>
          )}
        </nav>
      </div>
    );
  }
}

NavigationSlideout.propTypes = {
  navItems: PropTypes.array,
  userData: PropTypes.object,
  maxExpandedNavItems: PropTypes.integer,
}
NavigationSlideout.defaultProps = {
  userData: null,
}

export default NavigationSlideout;
