;(function (define) {

define(['backbone'], function (Backbone) {
    'use strict';

    return Backbone.Model.extend({
        defaults: {
            modes: [],
            course: '',
            enrollment_start: '',
            number: '',
            content: {
                overview: '',
                display_name: '',
                number: ''
            },
            start: '',
            image_url: '',
            org: '',
            display_org_with_default: '',
            id: ''
        }
    });

});

})(define || RequireJS.define);
