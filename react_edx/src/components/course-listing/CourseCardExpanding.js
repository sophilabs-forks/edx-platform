import React, { PropTypes } from "react";
import FontAwesome from "react-fontawesome";
import Time from "react-time-format";
import UIButton from "components/ui-elements/UIButton";
import styles from "sass/course-listing/course-card-expanding.css";

export class CourseCardExpanding extends React.Component {
  constructor(props: Props) {
    super(props);
    this.state = {
      infoExpanded: false,
    };
    this.onClick = this.onClick.bind(this);
  }

  onClick(_event) {
    this.setState({
      infoExpanded: !(this.state.infoExpanded),
    } );
  }

  render() {

    return (
      <article
        key={this.props.cardIndex}
        className={`col-12 col-sm-6 col-md-3 col-lg-3 ${styles["course-card-expanding-container"]} ${this.state.infoExpanded ? styles["info-expanded"] : '' }`}
      >
        <div className={`container ${styles["course-card-expanding"]} ${this.state.infoExpanded ? 'container' : '' }`}>
          <div className={`${styles["main-image-container"]}`}>
            <div className={`${styles["course-card-image-decorative__container"]}`}>
              <div
                className={styles["course-card-image-decorative"]}
                style={{
                  backgroundImage: "url(" + this.props.courseData.image_url + ")"
                }}
              ></div>
            </div>
            {this.state.infoExpanded && (
              <div className={`${styles["course-card-info-left"]}`}>
                <img src={this.props.courseData.image_url} className={styles["course-image-original"]} alt={this.props.courseData.content.display_name} role="presentation" />
                <div className={`${styles["info-container"]}`}>
                  <div className={styles["course-org-number"]}>
                    <span className={styles["course-organisation"]}>
                      {this.props.courseData.org}
                    </span>
                    <span className={styles["course-number"]}>
                      {this.props.courseData.number}
                    </span>
                  </div>
                  <h2 className={styles["course-name-overlayed"]}>{this.props.courseData.content.display_name}</h2>
                  <div className={styles["start-date"]}>
                    Starts on: <span><Time value={this.props.courseData.start} format="MM/DD/YYYY" /></span>
                  </div>
                </div>
              </div>
            )}
          </div>
          <div className={styles["course-card-info"]}>
            {!(this.state.infoExpanded) && (
              <div className={`${styles["info-container"]}`}>
                <div className={styles["course-org-number"]}>
                  <span className={styles["course-organisation"]}>
                    {this.props.courseData.org}
                  </span>
                  <span className={styles["course-number"]}>
                    {this.props.courseData.number}
                  </span>
                </div>
                <h2 className={styles["course-name-normal"]}>{this.props.courseData.content.display_name}</h2>
              </div>
            )}
            {this.state.infoExpanded && (
              <div className={styles["course-description"]}>
                {this.props.courseData.content.overview}
              </div>
            )}
            <div className={styles["course-actions"]}>
              {!(this.state.infoExpanded) ? (
                <UIButton
                  buttonSize= "button-small"
                  buttonAlignment= "align-bottom-left"
                  buttonStyle= "button-positive"
                  buttonIcon= "arrow-circle-o-right"
                  buttonLabel= "More info"
                  onClick={this.onClick}
                />
              ) : (
                <UIButton
                  buttonSize= "button-medium"
                  buttonAlignment= "align-bottom-right"
                  buttonIcon= "bolt"
                  buttonLabel= "Enroll"
                />
              )}
            </div>
          </div>
          {this.state.infoExpanded && (
            <button className={styles["close-button"]} onClick={this.onClick}>
              <FontAwesome
                className={styles["close-button__icon"]}
                name="remove"
              />
            </button>
          )}
        </div>
      </article>
    );
  }
}

CourseCardExpanding.propTypes = {
  courseData: PropTypes.object,
  cardIndex: PropTypes.integer
}

CourseCardExpanding.defaultProps = {
  courseData: {
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
      "https://www.codeproject.com/KB/GDI-plus/ImageProcessing2/flip.jpg",
    catalog_visibility: "both",
    org: "igorova",
    id: "course-v1:igorova+IG101+2017"
  }
}

export default CourseCardExpanding;
