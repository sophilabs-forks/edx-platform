import React, { PropTypes } from "react";
import styles from "sass/core-layout/navigation/navigation.css";
import NavigationItem from "components/core-layout/navigation/NavigationItem";
import NavigationSlideout from "components/core-layout/navigation/NavigationSlideout";
import logo from "logo.svg";

export class Navigation extends React.Component {

  render() {
    var navItems = [
      {
        'itemLabel' : 'Home',
        'itemURL' : '#',
        'openInNewTab' : false,
        'isButton' : false,
      },
      {
        'itemLabel' : 'About',
        'itemURL' : '/about',
        'openInNewTab' : false,
        'isButton' : false,
      },
      {
        'itemLabel' : 'We are cool!',
        'itemURL' : '/wac',
        'openInNewTab' : false,
        'isButton' : false,
      },
      {
        'itemLabel' : 'Login',
        'itemURL' : '#',
        'openInNewTab' : false,
        'isButton' : true,
      },
    ]

    return (
      <nav className={`container d-flex ${styles["nav-container"]}`}>
        <div className={`d-flex mr-auto ${styles["nav-left"]}`}>
          {this.props.viewingCourse ? (
            <div className={`${styles["course-info-wrapper"]}`}>
              <a href="#"><img src={this.props.navSettings.navLogoIcon} className={`${styles["header-icon"]}`} alt="Header Logo" role="presentation" /></a>
              <div className={`${styles["course-info"]}`}>
                <span className={`${styles["course-number"]}`}>{this.props.courseInfo.courseNumber}</span>
                <span className={`${styles["course-name"]}`}>{this.props.courseInfo.courseName}</span>
              </div>
            </div>
          ) : (
            <a href="#"><img src={this.props.navSettings.navLogo} className={`${styles["header-logo"]}`} alt="Header Logo" role="presentation" /></a>
          )}
        </div>
        <div className={`d-flex ml-auto ${styles["nav-right"]}`}>
          <div className={`d-flex ${styles["nav-menu"]}`}>
            { (navItems.length <= this.props.navSettings.maxExpandedNavItems) && (
              navItems.map(function(item){
                return <NavigationItem item={item} />
              })
            )}
          </div>
          {this.props.userAuthenticated && (
            <div className={`d-flex ${styles["nav-user"]}`}>
              <img className={`${styles["nav-user__avatar"]}`} src={this.props.userData.userImage} alt={`${this.props.userData.firstName} ${this.props.userData.lastName}`} role="presentation" />
              <span className={`${styles["nav-user__name"]}`}>Welcome, {this.props.userData.firstName}!</span>
            </div>
          )}
          {(this.props.userAuthenticated || (navItems.length > this.props.navSettings.maxExpandedNavItems)) && (
            <NavigationSlideout
              navItems={navItems}
              userData={this.props.userData}
              maxExpandedNavItems={this.props.navSettings.maxExpandedNavItems}
            />
          )}
        </div>
      </nav>
    );
  }
}

Navigation.propTypes = {
  navSettings: PropTypes.object,
  userAuthenticated: PropTypes.bool,
  viewingCourse: PropTypes.bool,
  userData: PropTypes.object,
}
Navigation.defaultProps = {
  navSettings: {
    navLogo: 'https://www.appsembler.com/wp-content/themes/appsembler-2017/images/branding/appsembler-logo-positive.svg',
    navLogoIcon: 'https://www.appsembler.com/wp-content/themes/appsembler-2017/images/branding/appsembler-icon-positive.svg',
    maxExpandedNavItems: 5,
  },
  userAuthenticated: false,
  userData: {
    firstName: 'Bob',
    lastName: 'Loblaw',
    userID: '13014515019',
    userImage: 'https://randomuser.me/api/portraits/men/79.jpg',
  },
  viewingCourse: false,
  courseInfo: {
    courseNumber: 'A101',
    courseName: 'This is a test course name',
  }
}

export default Navigation;
