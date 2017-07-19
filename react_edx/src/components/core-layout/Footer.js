import React, { PropTypes } from "react";
import styles from "sass/core-layout/footer.css";

export class Footer extends React.Component {
  render() {

    return (
      <footer className={`container ${styles["footer-container"]}`}>
        <a href={this.props.footerSettings.logoTarget} className={styles["footer-logo__container"]}>
          <img src={this.props.footerSettings.footerLogo} className={`${styles["footer-logo__image"]}`} alt="Footer Logo" role="presentation" />
        </a>
        <div>
          <span className={`${styles["footer-copyright"]}`}>
            {this.props.footerSettings.copyrightText}
          </span>
          <div className={`d-flex ${styles["footer-nav"]}`}>
            { this.props.footerItems.map(function(item){
              return (
                <a
                  href={item.itemURL}
                  target={ item.openInNewTab ? '_blank' : '_self' }
                >
                  {item.itemLabel}
                </a>
              )
            })}
          </div>
        </div>
      </footer>
    );
  }
}

Footer.propTypes = {
  footerSettings: PropTypes.object,
  footerItems: PropTypes.array,
}
Footer.defaultProps = {
  footerSettings: {
    footerLogo: 'https://www.appsembler.com/wp-content/themes/appsembler-2017/images/branding/appsembler-icon-positive.svg',
    logoTarget: '#',
    copyrightText: '© Appsembler 2017. All rights reserved.',
  },
  footerItems: [
    {
      'itemLabel' : 'Home',
      'itemURL' : '#',
      'openInNewTab' : false,
    },
    {
      'itemLabel' : 'About',
      'itemURL' : '/about',
      'openInNewTab' : false,
    },
    {
      'itemLabel' : 'Terms of Service',
      'itemURL' : '/about',
      'openInNewTab' : false,
    },
    {
      'itemLabel' : 'Privacy Policy',
      'itemURL' : '#',
      'openInNewTab' : false,
    },
  ]
}

export default Footer;
