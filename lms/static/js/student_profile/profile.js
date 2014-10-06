var edx = edx || {};

(function($, _, Backbone, gettext) {
    'use strict';

    edx.student = edx.student || {};
    edx.student.profile = {};

    var errorMessage = gettext("The data could not be saved.");

    edx.student.profile.ProfileModel = Backbone.Model.extend({
        defaults: {
            fullName: ''
        },

        urlRoot: '',

        sync: function(method, model) {
            var headers = {
                'X-CSRFToken': $.cookie('csrftoken')
            };

            $.ajax({
                url: model.urlRoot,
                type: 'PUT',
                data: model.attributes,
                headers: headers
            })
            .done(function() {
                model.trigger('sync');
            })
            .fail(function() {
                model.trigger('error', errorMessage);
            });
        },

        validate: function(attrs) {
            var errors = {};
            if (attrs.fullName.length < 1) {
                errors.fullName = gettext("Full name cannot be blank");
            }

            if (!$.isEmptyObject(errors)) {
                return errors;
            }
        }
    });

    edx.student.profile.PreferencesModel = Backbone.Model.extend({
        defaults: {
            language: 'en'
        },

        urlRoot: 'preferences',

        sync: function(method, model) {
            var headers = {
                'X-CSRFToken': $.cookie('csrftoken')
            };

            $.ajax({
                url: model.urlRoot,
                type: 'PUT',
                data: model.attributes,
                headers: headers
            })
            .done(function() {
                model.trigger('sync');
                location.reload();
            })
            .fail(function() {
                model.trigger('error', errorMessage);
            });
        },

        validate: function(attrs) {
            var errors = {};
            if (attrs.language.length < 1) {
                errors.language = gettext("Language cannot be blank");
            }

            if (!$.isEmptyObject(errors)) {
                return errors;
            }
        }
    });

    edx.student.profile.ProfileView = Backbone.View.extend({

        events: {
            'submit': 'submit',
            'change': 'change'
        },

        initialize: function() {
            _.bindAll(this, 'render', 'change', 'submit', 'invalidProfile', 'invalidPreference', 'error', 'sync', 'clearStatus');
            
            this.profileModel = new edx.student.profile.ProfileModel();
            this.profileModel.on('invalid', this.invalidProfile);
            this.profileModel.on('error', this.error);
            this.profileModel.on('sync', this.sync);

            this.preferencesModel = new edx.student.profile.PreferencesModel();
            this.preferencesModel.on('invalid', this.invalidPreference);
            this.preferencesModel.on('error', this.error);
            this.preferencesModel.on('sync', this.sync);
        },

        render: function() {
            self = this;
            $.getJSON( 'preferences/languages' )
                .done( function( json ) {
                    self.$el.html( _.template( $( '#profile-tpl' ).html(), {languageInfo: json} ) );

                    self.$nameStatus = $('#profile-name-status', self.$el);
                    self.$nameField = $('#profile-name', self.$el);
                    
                    self.$languageStatus = $('#preference-language-status', self.$el);
                    self.$languageChoice = $('#preference-language', self.$el);

                    self.$submitStatus = $('#submit-status', self.$el);

                    return self;
                })
                .fail( function() {
                    console.log("Request for language information failed.")
                });
        },

        change: function() {
            this.profileModel.set({
                fullName: this.$nameField.val()
            });

            this.preferencesModel.set({
                language: this.$languageChoice.val()
            });
        },

        submit: function(event) {
            event.preventDefault();
            this.clearStatus();
            this.profileModel.save();            
            this.preferencesModel.save();
        },

        invalidProfile: function(model) {
            var errors = model.validationError;
            if (errors.hasOwnProperty('fullName')) {
                this.$nameStatus
                    .addClass('validation-error')
                    .text(errors.fullName);
            }
        },

        invalidPreference: function(model) {
            var errors = model.validationError;
            if (errors.hasOwnProperty('language')) {
                this.$languageStatus
                    .addClass('validation-error')
                    .text(errors.language);
            }
        },

        error: function(error) {
            this.$submitStatus
                .addClass('error')
                .text(error);
        },

        sync: function() {
            this.$submitStatus
                .addClass('success')
                .text(gettext("Saved"));
        },

        clearStatus: function() {
            this.$nameStatus
                .removeClass('validation-error')
                .text("");

            this.$languageStatus
                .removeClass('validation-error')
                .text("");

            this.$submitStatus
                .removeClass('error')
                .text("");
        }
    });

    return new edx.student.profile.ProfileView({
        el: $('#profile-container')
    }).render();

})(jQuery, _, Backbone, gettext);
