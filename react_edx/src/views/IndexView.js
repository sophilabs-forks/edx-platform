import React from 'react';
import styles from "sass/pages/index.css";
import CoursesListing from "components/course-listing/CoursesListing";

export default function IndexView() {
  return (
    <div className={styles["index-container"]}>
      <section className={`container ${styles["index-intro"]}`}>
        <h1>This is an proof-of-concept of ReactJS powered Open edX LMS.</h1>
        <p>All components are self-contained, which is pretty neat!</p>
      </section>
      <CoursesListing />
    </div>
  );
}
