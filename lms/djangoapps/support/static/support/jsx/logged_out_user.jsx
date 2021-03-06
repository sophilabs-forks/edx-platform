/* global gettext */

import React from 'react';
import PropTypes from 'prop-types';

function LoggedOutUser({ platformName, loginQuery, supportEmail }) {
  return (
    <div>
      <div className="row">
        <div className="col-sm-12">
          <p>{gettext(`Sign in to ${platformName} so we can help you better.`)}</p>
        </div>
      </div>

      <div className="row">
        <div className="col-sm-12">
          <a href={`/login${loginQuery}`} className="btn btn-primary btn-signin">{gettext('Sign in')}</a>
        </div>
      </div>

      <div className="row">
        <div className="col-sm-12">
          <a className="create-account" href={`/register${loginQuery}`}>{gettext(`Create an ${platformName} account`)}</a>
          <p className="create-account-note">
            {gettext(`If you are unable to access your account contact us via email using ${supportEmail}.`)}
          </p>
        </div>
      </div>
    </div>
  );
}

LoggedOutUser.propTypes = {
  platformName: PropTypes.string.isRequired,
  loginQuery: PropTypes.string.isRequired,
  supportEmail: PropTypes.string.isRequired,
};

export default LoggedOutUser;
