const response = {
  facets: {
    org: {
      total: 5,
      terms: { djedova: 1, igorova: 2, eduardova: 1, edX: 1 },
      other: 0
    },
    modes: { total: 5, terms: { audit: 5 }, other: 0 },
    language: { total: 4, terms: { en: 4 }, other: 0 }
  },
  total: 5,
  max_score: 1.0,
  took: 11,
  results: [
    {
      _type: "course_info",
      score: 1.0,
      _index: "courseware_index",
      _score: 1.0,
      _id: "course-v1:igorova+IG101+2017",
      data: {
        modes: ["audit"],
        language: "en",
        course: "course-v1:igorova+IG101+2017",
        number: "IG101",
        content: {
          overview:
            " About This Course Include your long course description here. The long course description should contain 150-400 words. This is paragraph 2 of the long course description. Add more paragraphs as needed. Make sure to enclose them in paragraph tags. Requirements Add information about the skills and knowledge students need to take this course. Course Staff Staff Member #1 Biography of instructor/staff member #1 Staff Member #2 Biography of instructor/staff member #2 Frequently Asked Questions What web browser should I use? The Open edX platform works best with current versions of Chrome, Firefox or Safari, or with Internet Explorer version 9 and above. See our list of supported browsers for the most up-to-date information. Question #2 Your answer would be displayed here. ",
          display_name: "Igorova",
          number: "IG101"
        },
        start: "2030-01-01T00:00:00+00:00",
        image_url:
          "/asset-v1:igorova+IG101+2017+type@asset+block@images_course_image.jpg",
        catalog_visibility: "both",
        org: "igorova",
        id: "course-v1:igorova+IG101+2017"
      }
    },
    {
      _type: "course_info",
      score: 1.0,
      _index: "courseware_index",
      _score: 1.0,
      _id: "course-v1:igorova+Ig102+2017",
      data: {
        modes: ["audit"],
        language: "en",
        course: "course-v1:igorova+Ig102+2017",
        number: "Ig102",
        content: {
          overview:
            " About This Course Include your long course description here. The long course description should contain 150-400 words. This is paragraph 2 of the long course description. Add more paragraphs as needed. Make sure to enclose them in paragraph tags. Requirements Add information about the skills and knowledge students need to take this course. Course Staff Staff Member #1 Biography of instructor/staff member #1 Staff Member #2 Biography of instructor/staff member #2 Frequently Asked Questions What web browser should I use? The Open edX platform works best with current versions of Chrome, Firefox or Safari, or with Internet Explorer version 9 and above. See our list of supported browsers for the most up-to-date information. Question #2 Your answer would be displayed here. ",
          display_name: "Igorova 2",
          number: "Ig102"
        },
        start: "2030-01-01T00:00:00+00:00",
        image_url:
          "/asset-v1:igorova+Ig102+2017+type@asset+block@images_course_image.jpg",
        catalog_visibility: "both",
        org: "igorova",
        id: "course-v1:igorova+Ig102+2017"
      }
    },
    {
      _type: "course_info",
      score: 1.0,
      _index: "courseware_index",
      _score: 1.0,
      _id: "course-v1:edX+DemoX+Demo_Course",
      data: {
        modes: ["audit"],
        course: "course-v1:edX+DemoX+Demo_Course",
        number: "DemoX",
        content: {
          overview:
            " About This Course Include your long course description here. The long course description should contain 150-400 words. This is paragraph 2 of the long course description. Add more paragraphs as needed. Make sure to enclose them in paragraph tags. Prerequisites Add information about course prerequisites here. Course Staff Staff Member #1 Biography of instructor/staff member #1 Staff Member #2 Biography of instructor/staff member #2 Frequently Asked Questions What web browser should I use? The Open edX platform works best with current versions of Chrome, Firefox or Safari, or with Internet Explorer version 9 and above. See our list of supported browsers for the most up-to-date information. Question #2 Your answer would be displayed here. ",
          display_name: "edX Demonstration Course",
          number: "DemoX"
        },
        start: "2013-02-05T05:00:00+00:00",
        image_url:
          "/asset-v1:edX+DemoX+Demo_Course+type@asset+block@images_course_image.jpg",
        org: "edX",
        id: "course-v1:edX+DemoX+Demo_Course"
      }
    },
    {
      _type: "course_info",
      score: 1.0,
      _index: "courseware_index",
      _score: 1.0,
      _id: "course-v1:eduardova+ED101+2017",
      data: {
        modes: ["audit"],
        language: "en",
        course: "course-v1:eduardova+ED101+2017",
        number: "ED101",
        content: {
          overview:
            " About This Course Include your long course description here. The long course description should contain 150-400 words. This is paragraph 2 of the long course description. Add more paragraphs as needed. Make sure to enclose them in paragraph tags. Requirements Add information about the skills and knowledge students need to take this course. Course Staff Staff Member #1 Biography of instructor/staff member #1 Staff Member #2 Biography of instructor/staff member #2 Frequently Asked Questions What web browser should I use? The Open edX platform works best with current versions of Chrome, Firefox or Safari, or with Internet Explorer version 9 and above. See our list of supported browsers for the most up-to-date information. Question #2 Your answer would be displayed here. ",
          display_name: "Eduardova",
          number: "ED101"
        },
        start: "2030-01-01T00:00:00+00:00",
        image_url:
          "/asset-v1:eduardova+ED101+2017+type@asset+block@images_course_image.jpg",
        catalog_visibility: "both",
        org: "eduardova",
        id: "course-v1:eduardova+ED101+2017"
      }
    },
    {
      _type: "course_info",
      score: 1.0,
      _index: "courseware_index",
      _score: 1.0,
      _id: "course-v1:djedova+D101+2017",
      data: {
        modes: ["audit"],
        language: "en",
        course: "course-v1:djedova+D101+2017",
        number: "D101",
        content: {
          overview:
            " About This Course Include your long course description here. The long course description should contain 150-400 words. This is paragraph 2 of the long course description. Add more paragraphs as needed. Make sure to enclose them in paragraph tags. Requirements Add information about the skills and knowledge students need to take this course. Course Staff Staff Member #1 Biography of instructor/staff member #1 Staff Member #2 Biography of instructor/staff member #2 Frequently Asked Questions What web browser should I use? The Open edX platform works best with current versions of Chrome, Firefox or Safari, or with Internet Explorer version 9 and above. See our list of supported browsers for the most up-to-date information. Question #2 Your answer would be displayed here. ",
          display_name: "Djedova",
          number: "D101"
        },
        start: "2030-01-01T00:00:00+00:00",
        image_url:
          "/asset-v1:djedova+D101+2017+type@asset+block@images_course_image.jpg",
        org: "djedova",
        id: "course-v1:djedova+D101+2017"
      }
    }
  ]
};

export default response;
