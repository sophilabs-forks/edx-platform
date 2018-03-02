;(function (define, undefined) {
    'use strict';
    define([
        'gettext', 'underscore', 'backbone'
    ], function (gettext, _, Backbone) {

        var StudentStudyLocationModel = Backbone.Model.extend({
            idAttribute: 'studyLocation',
            defaults: {
                id: null,
                user: null,
                studylocation: null,
                created_date: ''
            }
        });

        return StudentStudyLocationModel;
    });
}).call(this, define || RequireJS.define);
