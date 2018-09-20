(function() {
  'use strict';
  var SegmentProxy = {
    identify: function () {
      let userId = arguments[0][0];
      let info = arguments[0][1];
      let options = arguments[0][2];

      let postBody = {
        userId: userId,
        info: info,
        options: options
      };
      $.ajax({
        url: '/event/identify',
        type: 'POST',
        contentType: 'application/json',
        dataType: 'json',
        data: JSON.stringify(postBody),
        async: true,
        processData: false,
      });
    },
    page: function (properties) {
      let postBody = {
        info: properties,
      };
      $.ajax({
        url: '/event/page',
        type: 'POST',
        contentType: 'application/json',
        dataType: 'json',
        data: JSON.stringify(postBody),
        async: true,
        processData: false,
      });
    },
    track: function (name, properties) {
      let postBody = {
        name: name,
        info: properties,
      };
      $.ajax({
        url: '/event/track',
        type: 'POST',
        contentType: 'application/json',
        dataType: 'json',
        data: JSON.stringify(postBody),
        async: true,
        processData: false,
      });
    }
  }
  this.SegmentProxy = SegmentProxy;
}).call(this);
