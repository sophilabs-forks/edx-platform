import React, { PropTypes } from "react";
import styles from "sass/course-listing/courses-listing.css";
import CourseCardExpanding from "components/course-listing/CourseCardExpanding";

export class CoursesListing extends React.Component {

  render() {

    return (
      <div className={`d-flex container`}>
        <div className={`d-flex row ${styles["courses-listing-container"]}`}>
          { this.props.coursesData.map(function(item, key){
            return <CourseCardExpanding courseData={item.data} cardIndex={key} />
          })}
        </div>
      </div>
    );
  }
}

CoursesListing.propTypes = {
  numberOfCourses: PropTypes.integer,
  displayKey: PropTypes.string,
  coursesData: PropTypes.object,
}

CoursesListing.defaultProps = {
  numberOfCourses: 3,
  displayKey: 'newest',
  coursesData: [
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
            " About This Course Include your long course description here. The long course description should contain 150-400 words. This is paragraph 2 of the long course description. Add more paragraphs as needed. Make sure to enclose them in paragraph tags. Requirements Add information about the skills and knowledge students need to take this course. Course Staff Staff Member #1 Biography of instructor/staff member #1 Staff Member #2 Biography of instructor/staff member #2 Frequently Asked Questions What web browser should I use? The Open edX platform works best with current versions of Chrome, Firefox or Safari, or with Internet Explorer version 9 and above. See our list of supported browsers for the most up-to-date information. Question #2 Your answer would be displayed here. About This Course Include your long course description here. About This Course Include your long course description here. About This Course Include your long course description here. About This Course Include your long course description here. About This Course Include your long course description here. About This Course Include your long course description here. About This Course Include your long course description here. About This Course Include your long course description here. About This Course Include your long course description here. About This Course Include your long course description here. About This Course Include your long course description here. About This Course Include your long course description here. About This Course Include your long course description here. About This Course Include your long course description here. About This Course Include your long course description here. About This Course Include your long course description here. About This Course Include your long course description here. About This Course Include your long course description here. About This Course Include your long course description here. About This Course Include your long course description here. About This Course Include your long course description here. About This Course Include your long course description here. About This Course Include your long course description here.",
          display_name: "Igorova",
          number: "IG101"
        },
        start: "2030-01-01T00:00:00+00:00",
        image_url:
          "http://lorempixel.com/output/city-q-c-640-480-10.jpg",
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
          "http://lorempixel.com/output/nature-q-c-640-480-3.jpg",
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
          "http://lorempixel.com/output/nightlife-q-c-640-480-3.jpg",
        org: "edX",
        id: "course-v1:edX+DemoX+Demo_Course"
      }
    },
  ],
}

export default CoursesListing;
