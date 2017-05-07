;(function (define, undefined) {
    'use strict';

    define('extension_deps', ['underscore'], function(_) {
        return function(extensionFieldsData) {
            var ext_deps = {};
            _.each(extensionFieldsData, function(extfield) {
                ext_deps[extfield.id] = extfield.js_model;
            });
            return ext_deps;
        }
    });

    define([
        'gettext', 'jquery', 'underscore', 'backbone', 'logger',
        'js/views/fields',
        'js/student_account/models/user_account_model',
        'js/student_account/models/user_preferences_model',
        'js/student_account/views/account_settings_fields',
        'js/student_account/views/account_settings_view',
        'extension_deps'
    ], function (gettext, $, _, Backbone, Logger, FieldViews, UserAccountModel, UserPreferencesModel,
                 AccountSettingsFieldViews, AccountSettingsView, extension_deps) {

        return function (fieldsData, extensionFieldsData, authData, userAccountsApiUrl, userPreferencesApiUrl, accountUserId, platformName) {

            var accountSettingsElement = $('.wrapper-account-settings');

            var userAccountModel = new UserAccountModel();
            userAccountModel.url = userAccountsApiUrl;

            var userPreferencesModel = new UserPreferencesModel();
            userPreferencesModel.url = userPreferencesApiUrl;

            var sectionsData = [
                 {
                    title: gettext('Basic Account Information (required)'),
                    fields: [
                        {
                            view: new FieldViews.ReadonlyFieldView({
                                model: userAccountModel,
                                title: gettext('Username'),
                                valueAttribute: 'username',
                                helpMessage: interpolate_text(
                                    gettext('The name that identifies you throughout {platform_name}. You cannot change your username.'), {platform_name: platformName}
                                )
                            })
                        },
                        {
                            view: new FieldViews.TextFieldView({
                                model: userAccountModel,
                                title: gettext('Full Name'),
                                valueAttribute: 'name',
                                helpMessage: gettext('The name that appears on your certificates. Other learners never see your full name.'),
                                persistChanges: true
                            })
                        },
                        {
                            view: new AccountSettingsFieldViews.EmailFieldView({
                                model: userAccountModel,
                                title: gettext('Email Address'),
                                valueAttribute: 'email',
                                helpMessage: interpolate_text(
                                    gettext('The email address you use to sign in. Communications from {platform_name} and your courses are sent to this address.'), {platform_name: platformName}
                                ),
                                persistChanges: true
                            })
                        },
                        {
                            view: new AccountSettingsFieldViews.PasswordFieldView({
                                model: userAccountModel,
                                title: gettext('Password'),
                                screenReaderTitle: gettext('Reset your Password'),
                                valueAttribute: 'password',
                                emailAttribute: 'email',
                                linkTitle: gettext('Reset Password'),
                                linkHref: fieldsData.password.url,
                                helpMessage: gettext('When you click "Reset Password", a message will be sent to your email address. Click the link in the message to reset your password.')
                            })
                        },
                        {
                            view: new AccountSettingsFieldViews.LanguagePreferenceFieldView({
                                model: userPreferencesModel,
                                title: gettext('Language'),
                                valueAttribute: 'pref-lang',
                                required: true,
                                refreshPageOnSave: true,
                                helpMessage: interpolate_text(
                                    gettext('The language used throughout this site. This site is currently available in a limited number of languages.'), {platform_name: platformName}
                                ),
                                options: fieldsData.language.options,
                                persistChanges: true
                            })
                        },
                        {
                            view: new FieldViews.DropdownFieldView({
                                model: userAccountModel,
                                required: true,
                                title: gettext('Country or Region'),
                                valueAttribute: 'country',
                                options: fieldsData['country']['options'],
                                persistChanges: true
                            })
                        }
                    ]
                },
                {
                    title: gettext('Additional Information (optional)'),
                    fields: [
                        {
                            view: new FieldViews.DropdownFieldView({
                                model: userAccountModel,
                                title: gettext('Education Completed'),
                                valueAttribute: 'level_of_education',
                                options: fieldsData.level_of_education.options,
                                persistChanges: true
                            })
                        },
                        {
                            view: new FieldViews.DropdownFieldView({
                                model: userAccountModel,
                                title: gettext('Gender'),
                                valueAttribute: 'gender',
                                options: fieldsData.gender.options,
                                persistChanges: true
                            })
                        },
                        {
                            view: new FieldViews.DropdownFieldView({
                                model: userAccountModel,
                                title: gettext('Year of Birth'),
                                valueAttribute: 'year_of_birth',
                                options: fieldsData['year_of_birth']['options'],
                                persistChanges: true
                            })
                        },
                        {
                            view: new AccountSettingsFieldViews.LanguageProficienciesFieldView({
                                model: userAccountModel,
                                title: gettext('Preferred Language'),
                                valueAttribute: 'language_proficiencies',
                                options: fieldsData.preferred_language.options,
                                persistChanges: true
                            })
                        }
                    ]
                }
            ];

            if (_.isArray(authData.providers)) {
                var accountsSectionData = {
                    title: gettext('Connected Accounts'),
                    fields: _.map(authData.providers, function(provider) {
                        return {
                            'view': new AccountSettingsFieldViews.AuthFieldView({
                                title: provider.name,
                                screenReaderTitle: interpolate_text(
                                    gettext("Connect your {accountName} account"), {accountName: provider['name']}
                                ),
                                valueAttribute: 'auth-' + provider.id,
                                helpMessage: '',
                                connected: provider.connected,
                                connectUrl: provider.connect_url,
                                acceptsLogins: provider.accepts_logins,
                                disconnectUrl: provider.disconnect_url
                            })
                        };
                    })
                };
                sectionsData.push(accountsSectionData);
            }

            // extension fields
            var deps, ext_fields;
            var ext_deps_config = extension_deps(extensionFieldsData);

            // http://stackoverflow.com/a/17448869
            RequireJS.require(_.values(ext_deps_config), function() {
                // TODO: some defensive type checking
                deps = _.object(_.keys(ext_deps_config), arguments);
                ext_fields = _.map(extensionFieldsData, function(extfield) {
                    var model_inst, field_view;
                    model_inst = new deps[extfield.id]();
                    model_inst.url = extfield.api_url;
                    return {
                        'view': new FieldViews.DropdownFieldView({ // TODO: determine which view
                            model: model_inst,
                            api_url: model_inst.url,
                            title: extfield.title,
                            valueAttribute: extfield.valueAttribute,
                            options: extfield.options,
                            persistChanges: extfield.persistChanges,
                            helpMessage: extfield.helpMessage
                            // TODO: screenReaderTitle
                        })
                    };
                });
                _.each(ext_fields, function(field) { 
                    sectionsData[0].fields.push(field); // add to basic information
                });

                    // var accountSettingsView = new AccountSettingsView({
                    //     model: userAccountModel,
                    //     accountUserId: accountUserId,
                    //     el: accountSettingsElement,
                    //     sectionsData: sectionsData
                    // });

                    // accountSettingsView.render();
                    // userAccountModel.fetch({
                    //     success: function () {
                    //         // Fetch the user preferences model
                    //         userPreferencesModel.fetch({
                    //             success: function() {
                    //                 showAccountFields();
                    //                 fetchAccountExtensionModels();
                    //             },
                    //             error: showLoadingError
                    //         });
                    //     },
                    //     error: showLoadingError
                    // });

            });

            var accountSettingsView = new AccountSettingsView({
                model: userAccountModel,
                accountUserId: accountUserId,
                el: accountSettingsElement,
                sectionsData: sectionsData
            });

            accountSettingsView.render();

            userAccountModel.fetch({
                success: function () {
                    // Fetch the user preferences model
                    userPreferencesModel.fetch({
                        success: function() {
                            showAccountFields();
                            fetchAccountExtensionModels();
                        },
                        error: showLoadingError
                    });
                },
                error: showLoadingError
            });


            var showLoadingError = function () {
                accountSettingsView.showLoadingError();
            };

            var showAccountFields = function () {
                // Record that the account settings page was viewed.
                Logger.log('edx.user.settings.viewed', {
                    page: "account",
                    visibility: null,
                    user_id: accountUserId
                });

                // Render the fields
                accountSettingsView.renderFields();
            };

            var fetchAccountExtensionModels = function () {
                //fetch each of the extension field models
                // TODO: is it important to chain these as on success callbacks?
                _.each(ext_fields, function (el, index, list) {
                    el.model.fetch({error: showLoadingError});
                });
            };

            return {
                userAccountModel: userAccountModel,
                userPreferencesModel: userPreferencesModel,
                accountSettingsView: accountSettingsView
            };
        };
    });
}).call(this, define || RequireJS.define);
