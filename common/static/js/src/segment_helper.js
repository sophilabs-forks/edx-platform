(function() {
  'use strict';
  var eventAjaxRequest = function (eventName, postBody) {
    $.ajax({
      url: '/event/' + eventName,
      type: 'POST',
      contentType: 'application/json',
      dataType: 'json',
      data: JSON.stringify(postBody),
      async: true,
      processData: false,
    });
  };

  var SegmentProxy = {
    identify: function () {
      var userId = arguments[0][0];
      var info = arguments[0][1];
      var options = arguments[0][2];

      var postBody = {
        userId: userId,
        info: info,
        options: options
      };
      eventAjaxRequest('identify', postBody);
    },
    page: function (properties) {
      var postBody = {
        info: properties,
      };
      eventAjaxRequest('page', postBody);
    },
    track: function (name, properties) {
      var postBody = {
        name: name,
        info: properties,
      };
      eventAjaxRequest('track', postBody);
    }
  }
  this.SegmentProxy = SegmentProxy;
}).call(this);
